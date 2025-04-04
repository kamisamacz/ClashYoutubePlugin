from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event
from tipovani.models import Tip, Kolo
from django.views.decorators.http import require_POST
from django.db.models import F

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def event_management(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.participants.add(request.user)  # <<< TADY ho rovnou přidáme
            return redirect("poradatel:event_list")
    else:
        form = EventForm()
    return render(request, "poradatel/event_management.html", {"form": form})


@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.free_slots > 0:
        event.participants.add(request.user)
    return redirect("login:dashboard")


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.remove(request.user)
    return redirect("login:dashboard")

@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, "poradatel/event_list.html", {"events": events})

@login_required
@user_passes_test(is_admin)
def event_management(request):
    events = Event.objects.all()
    return render(request, "poradatel/event_management.html", {"events": events})

@login_required
@user_passes_test(is_admin)
def manage_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    kola = Kolo.objects.filter(event=event)

    tipy_per_kolo = {}
    for kolo in kola:
        tipy = Tip.objects.filter(kolo=kolo)
        rozhodnuti = []
        nerozhodnuti = []

        for participant in event.participants.all():
            tip = tipy.filter(user=participant).first()
            if tip:
                rozhodnuti.append({
                    "username": participant.username,
                    "team": kolo.zapasnik_a if tip.vybrany_team == "A" else kolo.zapasnik_b
                })
            else:
                nerozhodnuti.append(participant.username)

        tipy_per_kolo[kolo.id] = {
            "rozhodnuti": rozhodnuti,
            "nerozhodnuti": nerozhodnuti
        }

    # 🏆 Výpočet Highscore
    participants = event.participants.all()
    participant_scores = []

    for participant in participants:
        tipy_participant = Tip.objects.filter(user=participant, kolo__event=event, kolo__vitez__isnull=False)
        score = tipy_participant.filter(vybrany_team=F('kolo__vitez')).count()
        participant_scores.append((participant.username, score))

    participant_scores.sort(key=lambda x: x[1], reverse=True)

    return render(request, "poradatel/manage_event.html", {
        "event": event,
        "kola": kola,
        "tipy_per_kolo": tipy_per_kolo,
        "highscore": participant_scores
    })

@login_required
@user_passes_test(is_admin)
@require_POST
def vyhodnotit_kolo(request, kolo_id):
    kolo = get_object_or_404(Kolo, id=kolo_id)
    vitez = request.POST.get("vitez")
    if vitez in ["A", "B"]:
        kolo.vitez = vitez
        kolo.save()
    return redirect("poradatel:manage_event", event_id=kolo.event.id)

@login_required
@user_passes_test(is_admin)
def event_highscore(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Najdi všechna kola a tipy s vítězem
    kola = Kolo.objects.filter(event=event, vitez__isnull=False)
    tipy = Tip.objects.filter(kolo__in=kola)

    # Výpočet skóre
    scores = {}
    for participant in event.participants.all():
        spravne = tipy.filter(user=participant, vybrany_team=F('kolo__vitez')).count()
        scores[participant.username] = spravne

    # Seřadíme sestupně podle skóre
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return render(request, "poradatel/highscore.html", {
        "event": event,
        "scores": sorted_scores,
    })