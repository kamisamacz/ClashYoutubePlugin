from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from poradatel.models import Kolo, Event
from .models import Tip, Kolo
from .forms import KoloForm, TipForm
from poradatel.views import is_admin
from django.http import JsonResponse
from tipovani.models import Kolo, Tip


@login_required
def otevrena_kola_json(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    kola = Kolo.objects.filter(event=event, uzavreno=False)

    data = []
    for kolo in kola:
        tip = Tip.objects.filter(user=request.user, kolo=kolo).first()
        data.append({
            "id": kolo.id,
            "zapasnik_a": kolo.zapasnik_a,
            "zapasnik_b": kolo.zapasnik_b,
            "tipoval": bool(tip),
            "vybrany_team": tip.vybrany_team if tip else None
        })

    return JsonResponse({"kola": data})

@login_required
@user_passes_test(is_admin)
def kola_tipovani_api(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    kola = Kolo.objects.filter(event=event, vitez__isnull=True)

    data = []
    for kolo in kola:
        rozhodnuti = []
        nerozhodnuti = []
        for user in event.participants.all():
            tip = Tip.objects.filter(user=user, kolo=kolo).first()
            if tip:
                jmeno_teamu = kolo.zapasnik_a if tip.vybrany_team == "A" else kolo.zapasnik_b
                rozhodnuti.append({
                    "username": user.username,
                    "team": jmeno_teamu
                })
            else:
                nerozhodnuti.append(user.username)

        data.append({
            "id": kolo.id,
            "rozhodnuti": rozhodnuti,
            "nerozhodnuti": nerozhodnuti,
        })

    return JsonResponse({"kola": data})




# === Uživatelské view ===

@login_required
def create_kolo(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = KoloForm(request.POST)
        if form.is_valid():
            kolo = form.save(commit=False)
            kolo.event = event
            kolo.save()
            return redirect("poradatel:manage_event", event_id=event.id)
    else:
        form = KoloForm()
    return render(request, "tipovani/create_kolo.html", {"form": form, "event": event})


@login_required
def user_tipovani(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    kola = Kolo.objects.filter(event=event, uzavreno=False)

    tipy = {}
    for kolo in kola:
        tip = Tip.objects.filter(user=request.user, kolo=kolo).first()
        tipy[kolo.id] = tip

    return render(request, "tipovani/user_tipovani.html", {
        "event": event,
        "kola": kola,
        "tipy": tipy
    })


@login_required
def kolo_detail(request, kolo_id):
    kolo = get_object_or_404(Kolo, id=kolo_id)

    if kolo.uzavreno:
        return render(request, "tipovani/kolo_uzavreno.html", {"kolo": kolo})

    tip = Tip.objects.filter(user=request.user, kolo=kolo).first()

    choices = [
        ("A", kolo.zapasnik_a),
        ("B", kolo.zapasnik_b)
    ]

    if request.method == "POST":
        form = TipForm(request.POST)
        form.fields["vybrany_team"].choices = choices
        if form.is_valid():
            vybrany_team = form.cleaned_data["vybrany_team"]
            Tip.objects.update_or_create(
                user=request.user, kolo=kolo, defaults={"vybrany_team": vybrany_team}
            )
            return redirect("login:dashboard")
    else:
        form = TipForm(initial={"vybrany_team": tip.vybrany_team if tip else None})
        form.fields["vybrany_team"].choices = choices

    return render(request, "tipovani/kolo_detail.html", {
        "kolo": kolo,
        "form": form,
        "existing_tip": tip
    })


# === Admin view ===

@login_required
@user_passes_test(is_admin)
def uzavrit_kolo(request, kolo_id):
    kolo = get_object_or_404(Kolo, id=kolo_id)
    kolo.uzavreno = True
    kolo.save()
    return redirect("poradatel:manage_event", event_id=kolo.event.id)


@login_required
@user_passes_test(is_admin)
def otevrit_kolo(request, kolo_id):
    kolo = get_object_or_404(Kolo, id=kolo_id)
    kolo.uzavreno = False
    kolo.save()
    return redirect("poradatel:manage_event", event_id=kolo.event.id)


@login_required
@user_passes_test(is_admin)
def vyhodnotit_kolo(request, kolo_id, team):
    kolo = get_object_or_404(Kolo, id=kolo_id)
    if kolo.uzavreno:
        kolo.vitez = team
        kolo.save()
    return redirect("poradatel:manage_event", event_id=kolo.event.id)
