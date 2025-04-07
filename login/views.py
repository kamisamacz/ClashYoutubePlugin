from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from poradatel.models import Event
from tipovani.models import Kolo, Tip
import json  # ➕ potřebné pro serializaci seznamu ID

def login_view(request):
    all_events = Event.objects.all()  # přidáme všechny eventy

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("login:dashboard")
        else:
            # Uživatele nenalezen -> vytvoříme ho
            if username and password:
                user = User.objects.create_user(username=username, password=password)
                for event in all_events:
                    event.participants.add(user)
                login(request, user)
                return redirect("login:dashboard")
            else:
                error_message = "Zadej jméno a heslo."
                return render(request, "login/login.html", {"error": error_message, "events": all_events})

    return render(request, "login/login.html", {"events": all_events})


@login_required
def dashboard_view(request):
    all_events = Event.objects.all()
    joined_events = Event.objects.filter(participants=request.user)
    kola = Kolo.objects.filter(event__in=all_events)
    tipy = Tip.objects.filter(user=request.user)
    tip_dict = {tip.kolo_id: tip.vybrany_team for tip in tipy}

    highscore_data = []
    for event in all_events:
        participants = event.participants.all()
        participant_scores = []

        for participant in participants:
            tipy_participant = Tip.objects.filter(user=participant, kolo__event=event, kolo__vitez__isnull=False)
            score = tipy_participant.filter(vybrany_team=F('kolo__vitez')).count()
            participant_scores.append((participant.username, score))

        participant_scores.sort(key=lambda x: x[1], reverse=True)

        user_score = 0
        user_rank = 0
        for index, (username, score) in enumerate(participant_scores, start=1):
            if username == request.user.username:
                user_score = score
                user_rank = index
                break

        highscore_data.append({
            "event": event,
            "score": user_score,
            "rank": user_rank if user_rank else "—",
            "total": len(participants)
        })

    # ✅ TADY byla chyba
    event_ids = [event.id for event in joined_events]
    event_ids_json = json.dumps(event_ids)

    # Debug
    print(f"[DEBUG] Uživatel {request.user.username} otevřel dashboard.")
    print(f"[DEBUG] event_ids = {event_ids}")
    print(f"[DEBUG] JSON = {event_ids_json}")

    return render(request, "login/dashboard.html", {
        "events": all_events,
        "joined_events": joined_events,
        "kola": kola,
        "tip_dict": tip_dict,
        "highscore_data": highscore_data,
        "event_ids_json": event_ids_json,
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect("login:login")
