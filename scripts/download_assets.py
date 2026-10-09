"""Download only URLs observed in official Wiki HTML; record provenance and failures."""
import concurrent.futures, hashlib, json, pathlib, urllib.request, urllib.parse
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='https://wiki.hoodedhorse.com'
class Images(HTMLParser):
 def __init__(self): super().__init__(); self.images=[];self.links=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='img':self.images.append(d.get('src',''))
  if t=='a':self.links.append(d.get('href',''))
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NineKingsBuilds/1.0 (official wiki asset download)'}),timeout=40).read()
def collect():
 entries={}
 for page in ['Cards','Kings']:
  p=Images();p.feed(get(BASE+'/9_Kings/'+page).decode())
  for src in p.images:
   if not src.startswith('/images/mbhh_9k/'):continue
   parts=src.split('/'); name=urllib.parse.unquote(parts[-2] if '/thumb/' in src else parts[-1])
   if page=='Cards' and (name.startswith('Card_type_') or name=='PlotLevelIcon.png'):continue
   if page=='Kings' and not name.startswith('King_of_'):continue
   entries[name]={'name':name,'category':'kings' if page=='Kings' else 'cards','source_page':BASE+'/9_Kings/'+page,'observed_src':BASE+src}
 return list(entries.values())
def download(e):
 try:
  url=e['observed_src']
  if '/thumb/' in url:
   # Ask the real file-description page for its original; never calculate a hash path.
   p=Images();p.feed(get(BASE+'/9_Kings/File:'+urllib.parse.quote(e['name'])).decode())
   urls=[urllib.parse.urljoin(BASE,x) for x in p.links if '/images/mbhh_9k/' in x and '/thumb/' not in x and urllib.parse.unquote(urllib.parse.urlsplit(x).path.split('/')[-1])==e['name']]
   if not urls:raise ValueError('Original link not found on File page')
   url=urls[0]
  data=get(url)
  if not (data.startswith(b'\x89PNG\r\n\x1a\n') or data.startswith(b'\xff\xd8\xff')):raise ValueError('Response is not PNG/JPEG')
  path='assets/'+e['category']+'/'+e['name'];target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  e.update(status='downloaded',url=url,path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as ex:e.update(status='missing',error=str(ex))
 return e
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: result=list(pool.map(download,collect()))
 (ROOT/'assets/manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'downloaded':sum(e['status']=='downloaded' for e in result),'missing':[e for e in result if e['status']=='missing']},ensure_ascii=False))
