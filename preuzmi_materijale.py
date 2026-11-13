#!/usr/bin/env python3
"""Preuzimanje javno dostupnih stranica/slika/PDF-ova s digitron.hr.

Pokrenuti lokalno kada imate mrežni pristup:
  python -m pip install requests beautifulsoup4 pillow
  python preuzmi_materijale.py --pages 300 --assets 2500

Uz dobar razlog i izričito dopuštenje nositelja sadržaja. Skripta ne pokušava
pristupiti zaključanim dijelovima niti zaobilazi ograničenja poslužitelja.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, re, sys, time
from collections import deque
from pathlib import Path
from urllib.parse import urlparse,urljoin,urldefrag,unquote
from urllib.robotparser import RobotFileParser

try:
 import requests
 from bs4 import BeautifulSoup
 from PIL import Image
except ImportError:
 print('Instalirajte potrebne biblioteke: python -m pip install requests beautifulsoup4 pillow')
 raise SystemExit(2)

ROOT=Path(__file__).resolve().parent
HOST='digitron.hr'
DOMAIN='https://digitron.hr'
UA='Medium29-Digitron-Client-Asset-Migration/1.0 (+human-reviewed project)'
IMAGE_EXT={'.jpg','.jpeg','.png','.webp','.gif','.avif','.bmp','.svg'}
DOC_EXT={'.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.zip'}
HTML_EXT={'','.html','.htm','/'}


def canonical(url,base=DOMAIN):
 url,_=urldefrag(urljoin(base,url))
 p=urlparse(url)
 if p.scheme not in ('http','https') or p.netloc.lower().removeprefix('www.')!=HOST:return ''
 if not p.path or p.path=='/':return DOMAIN+'/index.html'
 return DOMAIN+p.path

def safe_file_path(url,folder):
 p=urlparse(url)
 parts=[re.sub(r'[^\w.\-]+','_',unquote(seg),flags=re.UNICODE).strip(' .') for seg in p.path.split('/') if seg not in ('','.','..')]
 if not parts:parts=['index.html']
 parts=[seg[:110] for seg in parts]
 dest=folder.joinpath(*parts)
 if len(str(dest))>220:dest=folder/(hashlib.sha256(url.encode()).hexdigest()[:18]+Path(p.path).suffix)
 return dest

def is_html(url):
 return Path(urlparse(url).path).suffix.lower() in ('','.html','.htm')

def classify(url):
 ext=Path(urlparse(url).path).suffix.lower()
 if ext in IMAGE_EXT:return 'image'
 if ext in DOC_EXT:return 'document'
 return None

def img_sources(soup,base):
 found=set()
 for tag in soup.select('img, source'):
  for attr in ('src','data-src','data-original','data-lazy-src'):
   val=tag.get(attr)
   if val:
    u=canonical(val,base)
    if u and classify(u)=='image':found.add(u)
  for attr in ('srcset','data-srcset'):
   val=tag.get(attr,'')
   for src in val.split(','):
    u=canonical(src.strip().split()[0],base) if src.strip() else ''
    if u and classify(u)=='image':found.add(u)
 for t in soup.select('[style]'):
  for match in re.findall(r'url\([\'"]?([^\)\'"]+)',t.get('style','')):
   u=canonical(match,base)
   if u and classify(u)=='image':found.add(u)
 for t in soup.select('a[href],link[href]'):
  u=canonical(t.get('href',''),base)
  if u and classify(u):found.add(u)
 return found

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--pages',type=int,default=300,help='Najviše HTML stranica')
 ap.add_argument('--assets',type=int,default=2500,help='Najviše slika i dokumenata')
 ap.add_argument('--pause',type=float,default=.32,help='Pauza između zahtjeva u sekundama')
 ap.add_argument('--no-avif',action='store_true')
 args=ap.parse_args()
 session=requests.Session();session.headers.update({'User-Agent':UA,'Accept-Language':'hr-HR,hr;q=.9'})
 rp=RobotFileParser()
 try:
  robot=session.get(DOMAIN+'/robots.txt',timeout=15)
  if robot.ok:
   rp.parse(robot.text.splitlines())
  else:
   rp.parse([])
 except requests.RequestException as err:
  print('Robots nije dostupan:',err,'\nPrekinuto – provjerite dopuštenje za arhiviranje.');return 1
 def allowed(url): return rp.can_fetch(UA,url)
 queue=deque([DOMAIN+'/index.html',DOMAIN+'/digitron.html',DOMAIN+'/proizvodi-digitron.html',DOMAIN+'/kontakt.html'])
 seen=set();found_assets=set();rows=[]
 srcdir=ROOT/'materijali'/'arhiva_stranica';srcdir.mkdir(parents=True,exist_ok=True)
 def note(kind,url,status,dest=''):
  rows.append({'vrsta':kind,'izvor':url,'status':status,'lokalna_datoteka':str(dest)})
 print('Početak arhiviranja',DOMAIN)
 while queue and len(seen)<args.pages:
  url=queue.popleft()
  if url in seen or not allowed(url):continue
  seen.add(url)
  try:
   response=session.get(url,timeout=22)
   response.raise_for_status()
   if 'text/html' not in response.headers.get('content-type',''):
    note('page',url,'nije HTML');continue
   soup=BeautifulSoup(response.content,'html.parser')
   path=safe_file_path(url,srcdir);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(response.content)
   note('page',url,'preuzeto',path.relative_to(ROOT))
   found_assets.update(img_sources(soup,url))
   for tag in soup.select('a[href]'):
    other=canonical(tag.get('href',''),url)
    if other and is_html(other) and other not in seen and other not in queue and not any(x in other.lower() for x in ['login','admin','logout']):queue.append(other)
   print('Stranica',len(seen),url,'| slika/dokumenata',len(found_assets))
  except requests.RequestException as ex:
   note('page',url,'pogreška: '+str(ex)[:110]);print('Preskočeno',url,str(ex)[:100])
  time.sleep(args.pause)
 # U arhivu ubaci i materijale potvrđene tijekom ručnog pregleda.
 import csv as csvmod
 inventory=ROOT/'materijali'/'izvori_i_fotografije.csv'
 if inventory.exists():
  with inventory.open(encoding='utf-8-sig') as f:
   for row in csvmod.DictReader(f):
    u=canonical(row.get('url',''))
    if u and classify(u):found_assets.add(u)
 originals=ROOT/'assets'/'originali';optim=ROOT/'assets'/'images';docs=ROOT/'materijali'/'pdf_i_dokumenti'
 mapping={}
 for i,url in enumerate(sorted(found_assets)):
  if i>=args.assets:break
  if not allowed(url):note('asset',url,'robots zabranjuje');continue
  kind=classify(url)
  base=docs if kind=='document' else originals
  path=safe_file_path(url,base)
  try:
   res=session.get(url,timeout=30,stream=True)
   res.raise_for_status()
   max_size=20*1024*1024 if kind=='document' else 12*1024*1024
   if int(res.headers.get('content-length','0') or 0)>max_size:note(kind,url,'preveliko');continue
   buf=bytearray()
   for chunk in res.iter_content(65536):
    buf.extend(chunk)
    if len(buf)>max_size:raise ValueError('preveliko')
   path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(buf)
   target=path
   if kind=='image' and not args.no_avif and path.suffix.lower()!='.svg':
    try:
     im=Image.open(io.BytesIO(buf));im.seek(0)
     if im.mode not in ('RGB','RGBA'):im=im.convert('RGB')
     # Velike slike unaprijed optimizirati; max širina 1800 za web.
     if im.width>1800:im.thumbnail((1800,1800))
     optim.mkdir(parents=True,exist_ok=True)
     avif_name=hashlib.sha1(url.encode()).hexdigest()[:8]+'-'+path.stem[:55]+'.avif'
     avif=optim/avif_name;im.save(avif,format='AVIF',quality=72)
     target=avif
    except Exception as ex:print('AVIF preskočen:',url,str(ex)[:80])
   note(kind,url,'preuzeto',target.relative_to(ROOT))
   if kind=='image':mapping[url]=target.relative_to(ROOT).as_posix()
   print('Materijal',i+1,'/',min(len(found_assets),args.assets),url)
  except (requests.RequestException,ValueError,OSError) as ex:
   note(kind,url,'pogreška: '+str(ex)[:110]);print('Preskočeno',url,str(ex)[:100])
  time.sleep(args.pause)
 # Zamijeni udaljene URL-ove lokalnim putanjama samo u generiranim stranicama.
 # Izvorne arhive unutar materijali/arhiva_stranica ostaju netaknute.
 n=0
 for page in ROOT.glob('*.html'):
  html=page.read_text(encoding='utf-8');initial=html
  for url,local in mapping.items():
   html=html.replace(url,local)
   html=html.replace(url.replace('https://digitron.hr/','https://www.digitron.hr/'),local)
  if html!=initial:page.write_text(html,encoding='utf-8');n+=1
 # Spremanje inventara
 archive=ROOT/'materijali'/'izvrsena_arhiva.csv'
 with archive.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['vrsta','izvor','status','lokalna_datoteka']);w.writeheader();w.writerows(rows)
 print('Završeno: HTML',len(seen),'preuzeti materijali',sum(r['status']=='preuzeto' and r['vrsta']!='page' for r in rows),'lokalizirane stranice',n)
 print('Inventar:',archive)
 return 0

if __name__=='__main__':raise SystemExit(main())
