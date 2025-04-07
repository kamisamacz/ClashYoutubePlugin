from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tipovani.models import Kolo, Tip
from collections import defaultdict

# Stav overlayu
current_overlay = {
    "visible": False,
    "type": None,  # "tipy" nebo "highscore"
    "event_id": None
}


def overlay_view(request):
    return render(request, "overlay/overlay.html")


def get_overlay_content(request):
    """
    Vrací aktuální stav overlay + data pro tipování nebo highscore.
    """
    if not current_overlay["visible"]:
        return JsonResponse({"visible": False})

    data = {"visible": True, "type": current_overlay["type"]}

    if current_overlay["type"] == "tipy":
        # Zjistit první otevřené kolo z daného eventu
        kolo = Kolo.objects.filter(event_id=current_overlay["event_id"], uzavreno=False).order_by("id").first()
        if kolo:
            tipy = Tip.objects.filter(kolo=kolo)
            team_a = [tip.user.username for tip in tipy if tip.vybrany_team == "A"]
            team_b = [tip.user.username for tip in tipy if tip.vybrany_team == "B"]
            data.update({
                "zapasnik_a": kolo.zapasnik_a,
                "zapasnik_b": kolo.zapasnik_b,
                "team_a": team_a,
                "team_b": team_b
            })
        else:
            data.update({"type": None})

    elif current_overlay["type"] == "highscore":
        event_id = current_overlay["event_id"]
        kola = Kolo.objects.filter(event_id=event_id, uzavreno=True)

        score = defaultdict(int)
        tipujici = set()

        for kolo in kola:
            tipy = Tip.objects.filter(kolo=kolo)
            for tip in tipy:
                tipujici.add(tip.user.username)

            if not kolo.vitez or kolo.vitez == "X":
                continue

            for tip in tipy:
                if tip.vybrany_team == kolo.vitez:
                    score[tip.user.username] += 1

        for username in tipujici:
            score.setdefault(username, 0)

        highscore = sorted(score.items(), key=lambda x: x[1], reverse=True)

        data.update({
            "highscore": [{"username": user, "points": points} for user, points in highscore]
        })

    return JsonResponse(data)


@csrf_exempt
def update_overlay(request, event_id):
    """
    Přepínání obsahu overlay přes tlačítka v manage_event.
    """
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "show_tipy":
            current_overlay["visible"] = True
            current_overlay["type"] = "tipy"
            current_overlay["event_id"] = event_id
        elif action == "show_highscore":
            current_overlay["visible"] = True
            current_overlay["type"] = "highscore"
            current_overlay["event_id"] = event_id
        elif action == "hide":
            current_overlay["visible"] = False
            current_overlay["type"] = None
            current_overlay["event_id"] = None

    return redirect("poradatel:manage_event", event_id=event_id)
