# HB City Byggprojekt AB – webbplats

Ny webbplats för HB City Byggprojekt AB (byggfirma i Göteborg), i samma stil som S-Bygg-sidan: svart, guld
(`#CEA766`, från HB Citys nuvarande sida) och vitt, runda ”Ring”-knappar, piller-knappar, stor text (Plus Jakarta Sans),
foton med rundade hörn och enkla staplade sektioner.

## Sidor

Allt ligger i [`docs/`](docs/) och kräver inga verktyg.

- `index.html` – startsidan: tjänster, referenser i urval, omdöme, om oss, offertformulär, vanliga frågor, karta
- `referenser.html` – alla 17 referensprojekt med HB Citys egna bilder (klicka för full storlek)
- fem tjänstesidor: badrum, kök, golv, altan/balkong/uterum, renovering/ombyggnation – var och en med sina referenser

## Ändra text

All text, kontaktuppgifter och tjänster ligger i `scripts/build.py`; referensprojekten i `scripts/projects.json`. Kör:

```bash
python3 scripts/build.py docs
```

## Källor och sådant som ska kontrolleras

Texter, tjänster, referenser och bilder kommer från hbcitybygg.se; betyg, omdöme, telefon, adress och öppettid från
Google Maps.

**KONTROLLERA med HB City:**

- **Telefon:** Google Maps och toppen av hbcitybygg.se har 070-826 54 87, övriga sidor 0723-99 39 06. Båda visas.
- **Adress:** Google Maps har Marieholmsgatan 50, 416 63 Göteborg; hbcitybygg.se har Utlandagatan 8B, 412 61 Göteborg.
  Sidan använder Google Maps-adressen.
- **Tider:** Google Maps säger bara ”Stänger kl. 18”.
- Vanliga frågor och kortare tjänstetexter är skrivna utifrån hbcitybygg.se och bör läsas igenom.

Av fem omdömen på Google visas det enda med text (Jamal. al). Ett består bara av emojis och ett saknar text.

## Logga

Den sexkantiga HL-loggan är vektoriserad från `assets-src/hb-city-logo-original.png`:

- `docs/img/hb-city-logo.svg` – vit, med namnet på två rader (sidhuvud och sidfot)
- `assets-src/hb-city-logo-svart.svg`, `assets-src/hb-city-logo-staende-svart.svg` – svarta versioner för ljus bakgrund
- `docs/img/favicon.svg` – märket i guld

## Video i toppen

Startsidans hero spelar en tyst film i loop (`docs/video/hero.mp4`, 1920×1080, ca 5 MB; `hero-mobil.mp4`, 1280×720,
ca 2 MB, under 768 px). `docs/img/hero-poster.jpg` visas innan filmen laddat och för den som har valt reducerad
rörelse. Originalets första halvsekund (intoning från svart) är bortklippt så att loopen inte blinkar. Byta film:

```bash
ffmpeg -ss 0.5 -i ny.mp4 -an -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart docs/video/hero.mp4
ffmpeg -ss 0.5 -i ny.mp4 -an -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart -vf scale=1280:-2 docs/video/hero-mobil.mp4
ffmpeg -ss 0.5 -i ny.mp4 -frames:v 1 -vf scale=1600:-2 -q:v 4 docs/img/hero-poster.jpg
```

## Offertformuläret

Skickar e-post via [FormSubmit](https://formsubmit.co). Under förhandsvisningen går förfrågningarna till Elevate
Studio; byt `FORM_EMAIL` i `scripts/build.py` till info@hbcitybygg.se vid lansering.

## Publicera

`.github/workflows/deploy-pages.yml` publicerar `docs/` på GitHub Pages vid varje push till `main`. Slå på Pages med
källan *GitHub Actions* i repots inställningar.
