from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Kolo, Tip
from poradatel.models import Event
from .forms import KoloForm, TipForm
from poradatel.views import is_admin
from tipovani.models import Tip



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

    # Pokud je kolo uzavřené, rovnou přesměruj na stránku "kolo_uzavreno"
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
            tip, created = Tip.objects.update_or_create(
                user=request.user, kolo=kolo, defaults={"vybrany_team": vybrany_team}
            )
            return redirect("tipovani:kolo_detail", kolo_id=kolo.id)
    else:
        form = TipForm(initial={"vybrany_team": tip.vybrany_team if tip else None})
        form.fields["vybrany_team"].choices = choices

    return render(request, "tipovani/kolo_detail.html", {
        "kolo": kolo,
        "form": form,
        "existing_tip": tip
    })



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

from django.contrib.auth.decorators import user_passes_test
from poradatel.views import is_admin

@login_required
@user_passes_test(is_admin)
def vyhodnotit_kolo(request, kolo_id):
    kolo = get_object_or_404(Kolo, id=kolo_id)

    if request.method == "POST":
        vitez = request.POST.get("vitez")
        if vitez in ["A", "B"]:
            kolo.vitez = vitez
            kolo.save()
        return redirect("poradatel:manage_event", event_id=kolo.event.id)

    return render(request, "tipovani/vyhodnotit_kolo.html", {"kolo": kolo})


@login_required
@user_passes_test(is_admin)
def vyhodnotit_kolo(request, kolo_id, team):
    kolo = get_object_or_404(Kolo, id=kolo_id)
    if kolo.uzavreno:
        kolo.vitez = team
        kolo.save()
    return redirect("poradatel:manage_event", event_id=kolo.event.id)