"""Builds docs/*.html for HB City Byggprojekt AB.

Run:  python3 scripts/build.py docs

Texts come from hbcitybygg.se and the Google Maps listing; the photos are HB City's own, from the references on
hbcitybygg.se (scripts/projects.json). Things that disagree between the two sources are marked KONTROLLERA.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
ROOT = pathlib.Path(__file__).resolve().parent

# --- Company details ------------------------------------------------------------------------------------------------
NAME = "HB City Byggprojekt AB"
SHORT = "HB City"
# KONTROLLERA: Google Maps and the top of hbcitybygg.se give 070-826 54 87; the other pages of hbcitybygg.se give
# 0723-99 39 06. Both are shown until HB City says which is the main number.
PHONE, TEL = "070-826 54 87", "+46708265487"
PHONE2, TEL2 = "072-399 39 06", "+46723993906"
EMAIL = "info@hbcitybygg.se"
# KONTROLLERA: Google Maps says Marieholmsgatan 50, 416 63 Göteborg; hbcitybygg.se says Utlandagatan 8B, 412 61.
STREET, POSTAL, CITY = "Marieholmsgatan 50", "416 63", "Göteborg"
ADDR = f"{STREET}, {POSTAL} {CITY}"
RATING, REVIEW_COUNT = "5,0", 5
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {ADDR}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(ADDR) + "&z=14&hl=sv&output=embed"
HOURS = "Till kl. 18"  # Google Maps: "Stänger kl. 18"
ORG_NR = ""

# The quote form e-mails through FormSubmit. Elevate Studio receives the requests during the preview; at launch this
# becomes info@hbcitybygg.se. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/HB-preview/"

# --- Reference projects (hbcitybygg.se/referenser) -------------------------------------------------------------------
PROJECTS = {p["slug"]: p for p in json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))}
# Titles tidied (capitals, spacing); place and size kept exactly as on hbcitybygg.se.
TITLES = {
    "altan-ucklum": "Altan 43 kvm i Ucklum, Stenungsund",
    "badrum-guldheden": "Badrumsrenovering 5 kvm i Guldheden, Göteborg",
    "badrum-majorna": "Badrumsrenovering 4 kvm i Majorna",
    "jacuzzi-vanersborg": "Bygge av jacuzzi i Vänersborg",
    "badrum-karra": "Badrumsrenovering i Kärra, Hisingen",
    "kok-karra": "Köksrenovering i Kärra, Hisingen",
    "kok-kortedala": "Köksrenovering i Kortedala",
    "balkong-orgryte": "Balkongrenovering åt BRF i Örgryte",
    "kok-smogen": "Köksmontering i Smögen",
    "badrum-boras": "Badrumsrenovering i Borås",
    "kok-johanneberg": "Köksrenovering i Johanneberg",
    "uterum-vanersborg": "Bygge av uterum i Vänersborg",
    "fiskben-goteborg": "Fiskbensparkett i Göteborg",
    "golv-ek-laminat": "Golvläggning i ek och laminat",
    "fiskben-falkenberg": "Fiskbensparkett i Falkenberg",
    "sten-goteborg": "Trädgårdsarbete, stenläggning i Göteborg",
    "golv-hovas": "Golvläggning, parkett och klinker 40 kvm i Hovås",
}
# The one reference with its own description on hbcitybygg.se.
TEXTS = {
    "altan-ucklum": "Ett riktigt fint arbete och en nöjd kund där vi byggde en altan ute i det fina Stenungsund. Altanen var på ca 43 kvm, två höjder, ett staket och en trappa.",
}
# Cover photo for each project (index into its photos, 1-based).
COVER = {"kok-karra": 5, "badrum-boras": 3, "fiskben-falkenberg": 3, "uterum-vanersborg": 4, "balkong-orgryte": 1,
         "badrum-guldheden": 3, "kok-kortedala": 3, "golv-hovas": 5, "kok-johanneberg": 3, "badrum-karra": 1}


def cover(slug):
    return f'{slug}-{COVER.get(slug, 1)}'


# --- Services --------------------------------------------------------------------------------------------------------
# Main services with a page each, backed by references. Everything else HB City lists is in OTHER.
SERVICES = [
    dict(slug="badrum", title="Badrumsrenovering", photo=cover("badrum-boras"),
         short="Hela badrum, från rivning till färdigt rum.",
         body=["Vi renoverar badrum i Göteborg med omnejd, stora som små. Bland våra referenser finns badrum i Guldheden, Majorna, Kärra och Borås.",
               "Berätta om ditt badrum, så återkommer vi med en kostnadsfri offert."],
         projects=["badrum-guldheden", "badrum-majorna", "badrum-karra", "badrum-boras"]),
    dict(slug="kok", title="Köksrenovering och köksmontering", photo=cover("kok-karra"),
         short="Nya kök, renovering och montering av köksinredning.",
         body=["Vi renoverar kök och monterar köksinredning – från ett helt nytt kök till byte av luckor och bänkskivor. Bland våra referenser finns kök i Kärra, Kortedala, Johanneberg och Smögen."],
         projects=["kok-karra", "kok-kortedala", "kok-johanneberg", "kok-smogen"]),
    dict(slug="golv", title="Golvläggning", photo=cover("fiskben-falkenberg"),
         short="Parkett, fiskben, ek, laminat och klinker.",
         body=["Vi lägger golv i alla former: fiskbensparkett, ekgolv, laminat och klinker. Bland våra referenser finns fiskbensparkett i Göteborg och Falkenberg och 40 kvm parkett och klinker i Hovås."],
         projects=["fiskben-goteborg", "fiskben-falkenberg", "golv-hovas", "golv-ek-laminat"]),
    dict(slug="altan-balkong", title="Altan, balkong och uterum", photo=cover("uterum-vanersborg"),
         short="Altaner, balkonger, uterum och trädäck.",
         body=["Vi bygger altaner och uterum och renoverar balkonger, både åt privatpersoner och bostadsrättsföreningar. Bland våra referenser finns en altan på 43 kvm i Ucklum, ett uterum i Vänersborg och balkongrenovering åt en BRF i Örgryte."],
         projects=["altan-ucklum", "uterum-vanersborg", "balkong-orgryte", "jacuzzi-vanersborg"]),
    dict(slug="renovering", title="Renovering och ombyggnation", photo="altan-ucklum-1",
         short="Renoveringar, ombyggnationer, reparationer och projektering.",
         body=["Vi arbetar med alla typer av byggnationer, renoveringar och reparationer, från mindre servicejobb till hela entreprenader. Det kan bland annat handla om snickerier, målning, fönsterbyten, putsning, fasadrenovering, ombyggnationer och projektering."],
         projects=["kok-karra", "badrum-karra", "sten-goteborg"]),
]
OTHER = ["Snickeri", "Måleri", "Fönsterbyten", "Putsning och fasad", "Dekoration", "Service och montering", "Trädgård och stenläggning"]
WORK_TYPES = [s["title"] for s in SERVICES] + OTHER + ["Annat"]
REF_ORDER = ["kok-karra", "badrum-karra", "badrum-guldheden", "badrum-majorna", "badrum-boras", "kok-kortedala",
             "kok-johanneberg", "kok-smogen", "balkong-orgryte", "altan-ucklum", "uterum-vanersborg", "jacuzzi-vanersborg",
             "fiskben-goteborg", "fiskben-falkenberg", "golv-hovas", "golv-ek-laminat", "sten-goteborg"]
FEATURED = ["kok-karra", "badrum-boras", "balkong-orgryte", "fiskben-falkenberg", "uterum-vanersborg", "badrum-guldheden"]

# --- Reviews (Google; copied exactly, only those with text) ----------------------------------------------------------
REVIEWS = [dict(name="Jamal. al", stars=5, text="Proffsiga,trevliga och jag rekommenderar de varmt!!")]

FAQ = [
    ("Vad kostar en offert?", f"Offerten är kostnadsfri. Fyll i <a href=\"#offert\">formuläret</a> eller ring <a href=\"tel:{TEL}\">{PHONE}</a>."),
    ("Har ni F-skatt och försäkring?", "Ja. Vi har F-skatt och ansvarsförsäkring."),
    ("Tar ni både små och stora jobb?", "Ja. Vi gör allt från mindre servicejobb till hela entreprenader."),
    ("Var jobbar ni?", "Vi utgår från Göteborg. Vi har gjort jobb i bland annat Stenungsund, Vänersborg, Borås, Falkenberg och Smögen."),
    ("Gäller ROT-avdrag?", "ROT-avdraget gäller arbetskostnaden för många renoveringar och ombyggnader i bostäder. Vi går igenom vad som gäller för ditt jobb i offerten."),
]

# --- Markup helpers ---------------------------------------------------------------------------------------------------
E = html.escape
PHONE_ICON = ('<svg class="pi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
              '<path d="M15 2.5a6.5 6.5 0 0 1 6.5 6.5M15 6a3 3 0 0 1 3 3"/></svg>')
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'


def stars(n=5):
    return f'<span class="stars" role="img" aria-label="{n} av 5 stjärnor">{STAR * n}</span>'


def img(src, alt="", sizes="100vw", lazy=True, pos="50% 50%"):
    return (f'<img src="img/{src}.jpg" srcset="img/{src}-s.jpg 800w, img/{src}.jpg 1600w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def photo(src, alt, sizes="(min-width: 960px) 50vw, 100vw"):
    return f'<figure class="ph">{img(src, alt, sizes)}</figure>'


# HB City's logo, traced to a vector from assets-src/hb-city-logo-original.png and set with the name on two lines for
# the dark header and footer. Black versions for light backgrounds are in assets-src/.
def logo():
    return '<img class="logo-img" src="img/hb-city-logo.svg" alt="HB City Byggprojekt AB" width="783" height="193">'


def call_btn(label=None):
    return f'<a class="pill pill-gold" href="tel:{TEL}">{PHONE_ICON}<span>{label or "Ring " + PHONE}</span></a>'


NAV = [("index.html#tjanster", "Tjänster"), ("referenser.html", "Referenser"), ("index.html#om-oss", "Om oss"),
       ("index.html#kontakt", "Kontakt")]


def header(name):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    rows = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="{NAME}, till startsidan">{logo()}</a>
    <nav class="nav" aria-label="Huvudmeny">{links}</nav>
    <a class="pill pill-gold head-call" href="tel:{TEL}">{PHONE_ICON}<span>{PHONE}</span></a>
    <a class="round round-gold head-round" href="tel:{TEL}" aria-label="Ring {PHONE}">{PHONE_ICON}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul class="menu-main">{rows}<li><a href="index.html#offert">Begär offert</a></li></ul>
      <p class="menu-h">Tjänster</p><ul class="menu-svc">{svc}</ul>
      {call_btn()}
    </div>
  </nav>
</header>'''


def footer():
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    org = f"<p>Org.nr {ORG_NR}</p>" if ORG_NR else ""
    return f'''<footer class="foot">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="{NAME}, till startsidan">{logo()}</a>
    <div class="foot-grid">
      <div>
        <p class="foot-h">{NAME}</p>
        <p>{STREET},<br>{POSTAL} {CITY}</p>
        <p><a href="tel:{TEL}">{PHONE}</a><br><a href="tel:{TEL2}">{PHONE2}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>F-skatt och ansvarsförsäkring</p>{org}
      </div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div><p class="foot-h">HB City</p><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}<li><a href="index.html#offert">Begär offert</a></li></ul></div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME}</span>
      <a href="https://elevatestudio.nu" target="_blank" rel="noopener">Byggd av Elevate Studio</a>
    </div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": NAME, "url": SITE_URL,
        "telephone": TEL, "email": EMAIL, "image": SITE_URL + "img/" + cover("kok-karra") + ".jpg",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTAL.replace(" ", ""),
                    "addressLocality": CITY, "addressCountry": "SE"},
        "areaServed": {"@type": "City", "name": "Göteborg"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(name, title, desc, main, image=None, home=False):
    url = SITE_URL + ("" if name == "index.html" else name)
    image = image or cover("kok-karra")
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE_URL}img/{image}.jpg">
<meta name="theme-color" content="#111111">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
{jsonld() if home else ''}
</head>
<body>
{header(name)}
<main id="main">
{main}
</main>
{footer()}'''
    (OUT / name).write_text(doc, encoding="utf-8")


def service_card(s):
    return (f'<li class="card"><a href="tjanst-{s["slug"]}.html">{photo(s["photo"], s["title"], "(min-width: 960px) 33vw, 100vw")}'
            f'<h3>{s["title"]}</h3><p>{s["short"]}</p><span class="more">Läs mer</span></a></li>')


def project_card(slug):
    p = PROJECTS[slug]
    n = len(p["photos"])
    return (f'<li class="card"><a href="referenser.html#{slug}">{photo(cover(slug), TITLES[slug], "(min-width: 960px) 33vw, 100vw")}'
            f'<h3>{TITLES[slug]}</h3><p>{n} bilder</p><span class="more">Se bilderna</span></a></li>')


ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def service_tile(s, i):
    """Start page: the photo fills the tile, the name and a line sit on it. The first two are large."""
    big = i < 2
    return (f'<li class="tile{" big" if big else ""}"><a href="tjanst-{s["slug"]}.html">'
            f'{img(s["photo"], "", "(min-width: 1100px) 50vw, 100vw" if big else "(min-width: 1100px) 33vw, 100vw")}'
            f'<span class="tile-txt"><b>{s["title"]}</b><span>{s["short"]}</span></span><span class="tile-go">{ARROW}</span></a></li>')


def project_slide(slug):
    n = len(PROJECTS[slug]["photos"])
    return (f'<li class="slide"><a href="referenser.html#{slug}">{img(cover(slug), "", "(min-width: 760px) 360px, 80vw")}'
            f'<span class="slide-n">{n} bilder</span><span class="slide-t">{TITLES[slug]}</span></a></li>')


def other_pills():
    return "".join(f'<a class="pill pill-dark" href="index.html?typ={quote_plus(t)}#offert">{t}</a>' for t in OTHER)


def review_block():
    out = []
    for r in REVIEWS:
        out.append(f'<figure class="review center">{stars(r["stars"])}<blockquote><p>”{E(r["text"])}”</p></blockquote>'
                   f'<figcaption><b>{E(r["name"])}</b>, omdöme på Google</figcaption></figure>')
    return "".join(out)


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    req = '<span class="req" aria-hidden="true">*</span>'
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
  <p class="field"><label for="f-typ">Välj tjänst</label><select id="f-typ" name="Tjänst"><option value="">– Välj ett alternativ –</option>{opts}</select></p>
  <p class="field"><label for="f-namn">För- och efternamn{req}</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
  <p class="field"><label for="f-tel">Telefonnummer{req}</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefonnummer eller e-post.</span></p>
  <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
  <div class="f2">
    <p class="field"><label for="f-kvm">Kvm</label><input id="f-kvm" name="Kvm" inputmode="decimal"></p>
    <p class="field"><label for="f-start">Önskat startdatum</label><input id="f-start" name="Önskat startdatum" type="date"></p>
  </div>
  <p class="field"><label for="f-besk">Arbetsbeskrivning</label><textarea id="f-besk" name="Arbetsbeskrivning" rows="5" placeholder="Vad ska göras och var?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="small">{req} Telefonnummer eller e-post räcker. Genom att skicka formuläret godkänner du att {NAME} behandlar dina uppgifter för att svara dig.</p>
  <p><button class="pill pill-dark" type="submit">Begär offert</button></p>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, eller ring <a href="tel:{TEL}">{PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="done-h">Tack! Vi har fått din förfrågan.</p>
  <p>Vi återkommer med en offert så snart vi kan. Brådskar det, ring <a href="tel:{TEL}">{PHONE}</a>.</p>
  <p><button class="link" type="button" id="qagain">Skicka en ny förfrågan</button></p>
</div>'''


# --- Start page -------------------------------------------------------------------------------------------------------
def index():
    tiles = "".join(service_tile(s, i) for i, s in enumerate(SERVICES))
    slides = "".join(project_slide(s) for s in FEATURED + [p for p in REF_ORDER if p not in FEATURED])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    svc_links = " ".join(f'<a class="pill pill-dark" href="tjanst-{s["slug"]}.html">{s["title"]}</a>' for s in SERVICES[:4])
    main = f'''<section class="hero" aria-labelledby="hero-h">
  <div class="hero-ph"><video class="hero-video" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" poster="img/hero-poster.jpg" tabindex="-1" aria-hidden="true"><source src="video/hero-mobil.mp4" type="video/mp4" media="(max-width: 767px)"><source src="video/hero.mp4" type="video/mp4"></video></div>
  <div class="wrap hero-in">
    <h1 id="hero-h">Byggfirma i Göteborg</h1>
    <p>Renovering, snickeri och ombyggnation – badrum, kök, golv, altaner och balkonger. Kostnadsfri offert, F-skatt och ansvarsförsäkring.</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="#offert">Begär offert</a></div>
  </div>
</section>

<section class="sec tint" aria-labelledby="intro-h">
  <div class="wrap split">
    {photo(cover("badrum-guldheden"), "Renoverat badrum i Guldheden, Göteborg")}
    <div>
      <h2 id="intro-h">Ambition, kvalitet och innovation</h2>
      <p class="lead">Vi på {NAME} brinner för att lyfta kvaliteten inom bygg- och underhållsarbeten. Hållbarhet och långsiktighet är våra viktigaste ledord – i kundrelationen, i materialens livslängd och ur miljösynpunkt.</p>
      <p>Vi arbetar med en personlig och transparent dialog genom hela arbetsprocessen.</p>
      <div class="btns">{svc_links}</div>
    </div>
  </div>
</section>

<section class="sec" id="tjanster" aria-labelledby="tj-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="tj-h">Våra tjänster</h2><p>Från badrum och kök till golv, altaner och balkonger – små servicejobb och hela entreprenader.</p></div>
    <ul class="tiles">{tiles}</ul>
    <div class="also"><h3>Vi gör också</h3><div class="btns">{other_pills()}</div></div>
  </div>
</section>

<section class="sec dark" id="referenser" aria-labelledby="ref-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="ref-h">Vad vi gjort tidigare</h2><p>{len(PROJECTS)} projekt i Göteborg med omnejd. Alla bilder är från våra egna jobb.</p></div>
    <div class="slider">
      <ul class="slides" id="slides" tabindex="0" aria-label="Referensprojekt">{slides}</ul>
      <div class="slider-nav"><button class="round round-line" type="button" data-slide="-1" aria-label="Föregående projekt">{ARROW}</button><button class="round round-line" type="button" data-slide="1" aria-label="Nästa projekt">{ARROW}</button></div>
    </div>
    <div class="btns"><a class="pill pill-gold" href="referenser.html">Se alla referenser</a><a class="pill pill-outline" href="#offert">Begär offert</a></div>
  </div>
</section>

<section class="sec" aria-labelledby="rv-h">
  <div class="wrap narrow center">
    <h2 id="rv-h">Vad kunderna säger</h2>
    <p class="rating">{stars()} <span>{RATING} av 5 på Google ({REVIEW_COUNT} omdömen)</span></p>
    {review_block()}
    <div class="btns"><a class="pill pill-dark" href="{MAPS_LINK}" target="_blank" rel="noopener">Läs omdömena på Google</a></div>
  </div>
</section>

<section class="sec tint" id="om-oss" aria-labelledby="om-h">
  <div class="wrap split">
    {photo(cover("balkong-orgryte"), "Renoverade balkonger åt en BRF i Örgryte")}
    <div>
      <h2 id="om-h">Om HB City Byggprojekt</h2>
      <p class="lead">{NAME} är ett relativt ungt bolag men med lång erfarenhet i branschen – vi har utfört byggprojekt sedan 2010.</p>
      <p>Vi jobbar både med mindre servicejobb och hela entreprenader, åt privatpersoner och bostadsrättsföreningar. Vårt mål är att alltid leverera mer än vad våra kunder förväntar sig.</p>
      <ul class="facts">
        <li><b>Sedan 2010</b><span>i byggbranschen</span></li>
        <li><b>F-skatt</b><span>och ansvarsförsäkring</span></li>
        <li><b>Kostnadsfri</b><span>offert</span></li>
      </ul>
      <div class="btns">{call_btn()}</div>
    </div>
  </div>
</section>

<section class="sec" id="kontakt" aria-labelledby="kt-h">
  <div class="wrap narrow">
    <h2 id="kt-h">Få en kostnadsfri offert</h2>
    <p class="lead">Fyll i formuläret och berätta vad du behöver hjälp med, så återkommer vi med en offert så snart vi kan. Vill du hellre ringa går det bra.</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div id="offert">{quote_form()}</div>
  </div>
</section>

<section class="sec tint" id="fragor" aria-labelledby="fq-h">
  <div class="wrap narrow">
    <h2 id="fq-h">Vanliga frågor</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec seo" aria-labelledby="seo-h">
  <div class="wrap narrow">
    <h2 id="seo-h">Byggfirma i Göteborg</h2>
    <p>{NAME} är en byggfirma i Göteborg som gör <a href="tjanst-badrum.html">badrumsrenoveringar</a>, <a href="tjanst-kok.html">köksrenoveringar och köksmontering</a>, <a href="tjanst-golv.html">golvläggning</a> och bygger <a href="tjanst-altan-balkong.html">altaner, balkonger och uterum</a>. Vi tar också <a href="tjanst-renovering.html">renoveringar och ombyggnationer</a>, snickeri, måleri, fönsterbyten, putsning och fasadrenovering.</p>
    <p>Se våra <a href="referenser.html">referenser</a> eller <a href="#offert">begär en kostnadsfri offert</a>.</p>
    <h3>Hitta hit</h3>
    <p>{NAME}, {ADDR}. Telefon <a href="tel:{TEL}">{PHONE}</a>. {HOURS}.</p>
  </div>
</section>

<section class="map" aria-label="Karta">
  <iframe src="{MAP_EMBED}" title="Karta: {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>'''
    page("index.html", "Byggfirma i Göteborg – renovering, badrum, kök, golv | HB City Byggprojekt AB",
         "HB City Byggprojekt AB är en byggfirma i Göteborg: badrumsrenovering, köksrenovering, golvläggning, altaner och balkonger. F-skatt, ansvarsförsäkring och kostnadsfri offert.",
         main, home=True)


# --- References page --------------------------------------------------------------------------------------------------
def gallery(slug):
    p = PROJECTS[slug]
    items = "".join(f'<li><a href="img/{n}.jpg" data-full>{img(n, f"{TITLES[slug]}, bild {i}", "(min-width: 960px) 25vw, 50vw")}</a></li>'
                    for i, (n, w, h) in enumerate(p["photos"], 1))
    text = f'<p>{TEXTS[slug]}</p>' if slug in TEXTS else ""
    return f'<article class="proj" id="{slug}"><h2>{TITLES[slug]}</h2>{text}<ul class="gal">{items}</ul></article>'


def referenser():
    order = REF_ORDER
    assert sorted(order) == sorted(PROJECTS)
    toc = "".join(f'<a class="pill pill-light" href="#{s}">{TITLES[s]}</a>' for s in order)
    main = f'''<section class="hero hero-small" aria-labelledby="ph-h">
  <div class="hero-ph">{img(cover("badrum-guldheden"), "", lazy=False, pos="50% 60%")}</div>
  <div class="wrap hero-in">
    <h1 id="ph-h">Referenser</h1>
    <p>Här hittar du ett urval av våra tidigare projekt. Alla bilder är från våra egna jobb.</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="index.html#offert">Begär offert</a></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <nav class="btns toc" aria-label="Projekt">{toc}</nav>
    {"".join(gallery(s) for s in order)}
  </div>
</section>'''
    page("referenser.html", "Referenser – badrum, kök, golv och altaner i Göteborg | HB City Byggprojekt AB",
         "Se HB City Byggprojekts tidigare projekt: badrumsrenoveringar, köksrenoveringar, golv, altaner, balkonger och uterum i Göteborg med omnejd.",
         main, image=cover("badrum-guldheden"))


# --- Service pages ----------------------------------------------------------------------------------------------------
def service_page(s):
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    projects = "".join(project_card(p) for p in s["projects"])
    others = "".join(service_card(o) for o in SERVICES if o["slug"] != s["slug"])
    main = f'''<section class="hero hero-small" aria-labelledby="ph-h">
  <div class="hero-ph">{img(s["photo"], s["title"], lazy=False)}</div>
  <div class="wrap hero-in">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a> / <a href="index.html#tjanster">Tjänster</a> / <span aria-current="page">{s["title"]}</span></nav>
    <h1 id="ph-h">{s["title"]} i Göteborg</h1>
    <p>{s["short"]}</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="index.html?typ={quote_plus(s["title"])}#offert">Begär offert</a></div>
  </div>
</section>
<section class="sec">
  <div class="wrap narrow prose">
    <h2>{s["title"]} med HB City</h2>
    {body}
    <p>Vi har F-skatt och ansvarsförsäkring, och offerten är kostnadsfri.</p>
  </div>
</section>
<section class="sec tint">
  <div class="wrap">
    <h2>Referenser</h2>
    <ul class="cards">{projects}</ul>
    <div class="btns"><a class="pill pill-dark" href="referenser.html">Alla referenser</a></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>Fler tjänster</h2>
    <ul class="cards">{others}</ul>
  </div>
</section>'''
    desc = f'{s["title"]} i Göteborg. {s["short"]} HB City Byggprojekt AB – F-skatt, ansvarsförsäkring och kostnadsfri offert.'
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Göteborg | HB City Byggprojekt AB', desc, main, image=s["photo"])


def not_found():
    main = f'<section class="sec"><div class="wrap narrow"><h1>Sidan finns inte</h1><div class="btns"><a class="pill pill-dark" href="index.html">Till startsidan</a>{call_btn()}</div></div></section>'
    page("404.html", "Sidan finns inte | HB City Byggprojekt AB", "Sidan kunde inte hittas.", main)


def seo_files():
    urls = ["index.html", "referenser.html"] + [f'tjanst-{s["slug"]}.html' for s in SERVICES]
    locs = "".join(f"<url><loc>{SITE_URL}{'' if u == 'index.html' else u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    index()
    referenser()
    for s in SERVICES:
        service_page(s)
    not_found()
    seo_files()
    print("Byggde", len(list(OUT.glob("*.html"))), "sidor i", OUT)
