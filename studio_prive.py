"""NOCTRA local editor. Binds ONLY to 127.0.0.1. No public admin pages."""
import json, os, re, subprocess, sys, threading, webbrowser
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, unquote
from html import escape

ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
ARTICLES=SITE/'articles'
INDEX=SITE/'data/articles.json'
DRAFTS=ROOT/'brouillons'
DRAFTS.mkdir(exist_ok=True)
PORT=8765

def slug_ok(x): return bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',x or ''))
def git(*args):
 p=subprocess.run(['git',*args],cwd=SITE,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
 if p.returncode: raise RuntimeError((p.stderr or p.stdout).strip() or 'Erreur Git')
 return p.stdout.strip()

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args): pass
 def send(self,data,status=200,mime='application/json'):
  if isinstance(data,(dict,list)):data=json.dumps(data,ensure_ascii=False).encode()
  elif isinstance(data,str):data=data.encode('utf-8')
  self.send_response(status);self.send_header('Content-Type',mime+'; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self' 'unsafe-inline'; img-src 'self' https: data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'");self.end_headers();self.wfile.write(data)
 def do_GET(self):
  path=urlsplit(self.path).path
  if path=='/':return self.send((ROOT/'editeur.html').read_bytes(),mime='text/html')
  if path=='/api/list':return self.send(json.loads(INDEX.read_text(encoding='utf-8')))
  if path.startswith('/api/article/'):
   slug=unquote(path.rsplit('/',1)[-1]);
   if not slug_ok(slug):return self.send({'error':'Identifiant invalide'},400)
   entries=json.loads(INDEX.read_text(encoding='utf-8'));item=next((x for x in entries if x['slug']==slug),None)
   if not item:return self.send({'error':'Introuvable'},404)
   f=ARTICLES/(slug+'.html');return self.send({'meta':item,'html':f.read_text(encoding='utf-8') if f.exists() else ''})
  if path=='/api/status':
   try:return self.send({'git':git('status','--short'),'branch':git('branch','--show-current')})
   except Exception as e:return self.send({'git_error':str(e)})
  return self.send({'error':'Introuvable'},404)
 def do_POST(self):
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>3_000_000:raise ValueError('Fichier trop volumineux')
   obj=json.loads(self.rfile.read(length))
   path=urlsplit(self.path).path
   if path=='/api/save':
    meta=obj['meta'];slug=meta.get('slug','');body=obj.get('html','')
    if not slug_ok(slug):raise ValueError('Identifiant invalide')
    if not meta.get('title') or not meta.get('excerpt') or not meta.get('date'):raise ValueError('Titre, date et résumé obligatoires')
    if len(body)>2_000_000:raise ValueError('Article trop long')
    allowed={'slug','title','category','date','excerpt','tags','readingMinutes','published'}
    meta={k:v for k,v in meta.items() if k in allowed}
    rows=json.loads(INDEX.read_text(encoding='utf-8'))
    rows=[x for x in rows if x['slug']!=slug]+[meta]
    ARTICLES.mkdir(exist_ok=True);(ARTICLES/(slug+'.html')).write_text(body,encoding='utf-8')
    INDEX.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return self.send({'ok':True,'message':'Article enregistré localement. Clique sur Publier pour envoyer sur GitHub.'})
   if path=='/api/delete':
    slug=obj.get('slug','')
    if not slug_ok(slug):raise ValueError('Identifiant invalide')
    rows=json.loads(INDEX.read_text(encoding='utf-8'));rows=[x for x in rows if x['slug']!=slug]
    INDEX.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ARTICLES/(slug+'.html')).unlink(missing_ok=True)
    return self.send({'ok':True,'message':'Article supprimé localement. Clique sur Publier pour mettre à jour le site.'})
   if path=='/api/publish':
    if not (SITE/'.git').exists():raise RuntimeError('Dépôt Git non connecté. Lis INSTALLATION.md pour cloner le dépôt.')
    git('add','-A');status=git('status','--porcelain')
    if not status:return self.send({'ok':True,'message':'Aucun changement à publier.'})
    git('commit','-m','Mise à jour des articles NOCTRA')
    git('push','origin','HEAD')
    return self.send({'ok':True,'message':'Modifications envoyées sur GitHub. GitHub Pages actualisera le site.'})
   if path=='/api/draft':
    slug=obj.get('slug','brouillon');slug=slug if slug_ok(slug) else 'brouillon'
    (DRAFTS/(slug+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    return self.send({'ok':True,'message':'Brouillon sauvegardé sur ton PC.'})
   return self.send({'error':'Action inconnue'},404)
  except Exception as e:return self.send({'error':str(e)},400)

if __name__=='__main__':
 try:
  server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
 except OSError as e:sys.exit('Impossible de lancer le studio : '+str(e))
 print('NOCTRA Studio privé : http://127.0.0.1:%d'%PORT)
 print('Accessible uniquement depuis cet ordinateur. Ctrl+C pour fermer.')
 threading.Timer(0.7,lambda:webbrowser.open('http://127.0.0.1:%d'%PORT)).start()
 try:server.serve_forever()
 except KeyboardInterrupt:pass
