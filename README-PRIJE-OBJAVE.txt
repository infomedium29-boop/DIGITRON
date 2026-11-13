DIGITRON D.O.O. BUJE — PRVI FUNKCIONALNI REDIZAJN
Medium29 · radna verzija · 13. studenoga 2026.

ŠTO JE PRIPREMLJENO
• 18 HTML datoteka (17 sadržajnih stranica i zasebna 404 stranica)
• Moderna responsivna navigacija, interaktivni katalog vaga, kontaktni obrazac
• Dizajn hero sekcije, servisni sadržaji, FAQ, povijest, kontakt, mapa
• SEO title/description, canonical, schema.org, sitemap, robots, 404
• Datoteke za Cloudflare Pages: _redirects i _headers
• Poseban manifest 22 potvrđena URL-a originalnih fotografija i 2 arhivska PDF-a
• JSON s provjerenim kontakt podacima i glavnim kategorijama
• Skripta za arhiviranje svih javnih stranica, fotografija i javnih dokumenata

VAŽNA NAPOMENA: FOTOGRAFIJE
Zbog nedostupnosti vanjskog internetskog pristupa iz radnog okruženja,
originalne fotografske datoteke nisu fizički spremljene u ovaj ZIP.
U HTML-u se koriste potvrđene direktne URL adrese s originalne domene digitron.hr.
Ove fotografije trebale bi se prikazivati kad otvorite web uz internetsku vezu,
ali privremeno ovise o dostupnosti stare domene i dopuštenju izvornog poslužitelja.

POSTUPAK PREUZIMANJA ORIGINALNIH MATERIJALA I PRETVORBE U AVIF
1. Raspakirajte ZIP na računalo koje ima pristup internetu.
2. Instalirajte Python 3.11+.
3. U terminalu pokrenite:
   python -m pip install requests beautifulsoup4 pillow
   python preuzmi_materijale.py --pages 300 --assets 2500
4. Skripta čuva source HTML u materijali/arhiva_stranica, fotografije u
   assets/originali, optimizirane verzije u assets/images, PDF-ove u
   materijali/pdf_i_dokumenti.
5. URL-ovi slika u pripremljenim HTML stranicama bit će zamijenjeni lokalnim.
6. Generira se materijali/izvrsena_arhiva.csv s popisom što je uspjelo preuzeti.
7. Nakon preuzimanja koristite sadržaj mape digitron-redizajn za deploy.

Napomena: Skripta čita javne stranice i poštuje robots.txt; sadržaj
zaštićen lozinkom, zastario ili uklonjen s poslužitelja ne može pribaviti.
Prije javne objave potrebno je odobrenje nositelja prava za ponovno korištenje
fotografija, logotipa i ostalih materijala na novoj web stranici.

ŠTO JE TRENUTNO FUNKCIONALNO
• Navigacija desktop/mobitel
• Traka s kontaktom na mobilnim uređajima
• Katalog s tražilicom i filtriranjem
• Telefonske i e-mail poveznice
• Obrazac koji otvara e-mail program s unaprijed napisanim podacima.
  NEMA skrivenog slanja, jer još nije dostavljen Web3Forms/Resend API ključ.
• Lokalno spremanje izbora o kolačićima, bez marketinškog praćenja

PRIJEVODI / DODATNE FUNKCIJE
• Izrađena je hrvatska verzija.
• Multi-jezik, CMS, webshop, specifične tehničke kartice svih uređaja,
  lokalno pohranjene slike i potpuna migracija starih kataloških URL-ova
  trebaju dodatni rad / pristup sadržaju.

PRAVNE I POSLOVNE PROVJERE PRIJE SLUŽBENE OBJAVE
1. Od vlasnika potvrditi aktualne proizvode, cijene i raspoloživost.
2. Potvrditi trenutačno važenje statusa ovlaštenja za ovjeru vaga.
3. Zamijeniti privremeni stilizirani tekstualni znak službenim LOGOTIPOM.
4. Potvrditi autorska prava na stare fotografije i pravo njihove uporabe.
5. Uskladiti privacy/cookie/terms tekstove sa stvarnim sustavima.
6. Povezati kontaktne obrasce s provjerenom dostavom i antispam zaštitom.
7. Prije migracije napraviti popis SVIH indeksiranih starih URL-ova i 301
   preusmjerenja (osobito produktnih URL-ova) da se ne izgubi SEO promet.
8. Testirati mobitele, Chrome, Safari, Firefox i PageSpeed.
9. Provjeriti prava i konfiguraciju domene te MX/TXT DNS zapise prije promjena.
10. Nakon suglasnosti objaviti sitemap u Google Search Console.
    OBAVEZNO ukloniti privremeni noindex/nofollow iz HTML meta robots oznaka
    i X-Robots-Tag u datoteci _headers tek kada se objavi konačni web.
11. Ako se generirane stranice ponovo stvaraju kroz generate_site.py,
    treba nakon toga ponovno pokrenuti preuzmi_materijale.py kako bi se
    ponovno lokalizirale fotografije.

KAKO PREGLEDATI WEB
• Otvorite index.html (navigacija funkcionira i bez lokalnog servera).
• Za naprednije testiranje: python -m http.server 8000
  pa u pregledniku otvorite http://localhost:8000
• Za Cloudflare Pages: upload cjelokupnog sadržaja mape digitron-redizajn.

Materijal je radni demo i nije namijenjen objavi preko postojeće domene
prije dogovora s vlasnikom i svih navedenih provjera.


VERZIJA V2 – LOGOTIP I UVODNA ANIMACIJA
- Novi logo: assets/graphics/digitron-logo.svg (vektorski PRECRTAN prema originalu
  vidljivom na službenom Digitron PDF cjeniku; nije izvorni originalni SVG).
- Za 100 % izvorni logo zamijeniti tu datoteku originalom iz tvrtke,
  zadržati isti naziv i SVG format ili uskladiti putanje i MIME tip.
- Intro traje približno 2,6 s i prikazuje se jednom po kartici/sesiji.
- Preskoči intro: desni donji kut ili tipka Escape.
- Za posjetitelje s reduciranim animacijama intro je isključen.
- Header i footer koriste isti SVG; zamjena jedne datoteke mijenja sve stranice.
- Ne objavljivati javno bez suglasnosti tvrtke, provjere obrazaca i slika.
