
# Clash Plugin – Tipovací systém s overlayem

## 🧠 O projektu

Tento projekt je webová aplikace pro správu a zobrazování sportovních tipů a výsledků během živého streamu. Obsahuje:

- ✅ Přihlašování a správa uživatelů
- 📊 Tipování zápasů mezi dvěma stranami (A vs B)
- 🏆 Vyhodnocování výsledků a zobrazení highscore
- 🎮 Overlay pro YouTube stream (zobrazovaný pomocí pluginu do prohlížeče)
- 📱 Optimalizovaný vzhled pro mobilní zařízení

---

## 📚 Obsah

- [🧠 O projektu](#-o-projektu)
- [⚙️ Technologie](#️-technologie)
- [📁 Struktura projektu](#-struktura-projektu)
- [🚀 Spuštění](#-spuštění)
- [🧩 Plugin do prohlížeče](#-plugin-do-prohlížeče)
- [✨ Vychytávky](#-vychytávky)
- [📸 Autor](#-autor)

---

## ⚙️ Technologie

- **Python 3.12**
- **Django 5.1**
- **HTML/CSS (s neon efekty)** – styling optimalizován pro tmavé pozadí a přehlednost
- **JavaScript** – polling pro overlay aktualizaci
- **SQLite** – výchozí databáze
- **Rozšíření pro Chrome/Firefox** – zobrazuje overlay přímo nad YouTube videem

---

## 📁 Struktura projektu

```
Clash plugin/
│
├── login/                  # Přihlašování a správa uživatelů
├── poradatel/             # Správa eventů a jejich kol
├── tipovani/              # Modely tipování a vyhodnocení
├── overlay/               # Zobrazení overlay a jeho řízení
├── static/                # Stylování (jen přes jednotlivé HTML)
├── templates/             # Stylizované HTML šablony
│   ├── login/
│   │   └── login.html
│   │   └── dashboard.html
│   ├── tipovani/
│   │   └── create_kolo.html, kolo_detail.html
│   ├── poradatel/
│   │   └── manage_event.html, event_management.html
│   ├── overlay/
│   │   └── overlay.html
│
├── chrome_extension/      # Rozšíření do prohlížeče
│   ├── manifest.json
│   ├── content.js
│   └── styles.css
│
├── manage.py              # Django entry point
└── README.md              # Tento soubor
```

---

## 🚀 Spuštění

### Lokálně
```bash
git clone https://github.com/tvoje-jmeno/clash-plugin.git
cd clash-plugin
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Aplikace poběží na `http://127.0.0.1:8000`

---

## 🧩 Plugin do prohlížeče

1. Otevři `chrome://extensions/`
2. Zapni **Developer mode**
3. Klikni na **Load unpacked** a vyber složku `chrome_extension`
4. V pluginu nastav správnou IP adresu nebo hostname pro overlay (`http://<yourIP/website>:8000/overlay/`)

---

## ✨ Vychytávky

- Neonové efekty, dýchající texty, moderní vzhled
- Kompaktní rozhraní optimalizované pro mobilní telefon
- Automatická synchronizace overlay s backendem
- Přepínání mezi zobrazením **tipů** a **highscore**
- Vyhodnocení zápasu a živé zobrazování výsledků přes overlay

---

## 📸 Autor

Projekt vytvořen s láskou a neonem 💚  
**[kamisamacz](https://instagram.com/kamisamacz)**

---

> Pokud chceš přispět nebo nahlásit chybu, otevři issue nebo PR.
