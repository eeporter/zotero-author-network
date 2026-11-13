import sqlite3, json, itertools, collections, sys, unicodedata, re
# usage: python3 extract.py /path/to/zotero.sqlite OUTDIR   (copy zotero.sqlite first if Zotero is open)
DB, S = sys.argv[1], sys.argv[2]
db=sqlite3.connect(DB)
q='''
select i.itemID, c.firstName, c.lastName, c.fieldMode, ic.orderIndex,
  (select v.value from itemData d join itemDataValues v using(valueID) join fields f using(fieldID) where d.itemID=i.itemID and f.fieldName='title') title,
  (select v.value from itemData d join itemDataValues v using(valueID) join fields f using(fieldID) where d.itemID=i.itemID and f.fieldName='date') date
from items i
join itemCreators ic on ic.itemID=i.itemID
join creators c on c.creatorID=ic.creatorID
join creatorTypes ct on ct.creatorTypeID=ic.creatorTypeID
where i.libraryID=1 and ct.creatorType='author'
  and i.itemID not in (select itemID from deletedItems)
order by i.itemID, ic.orderIndex'''
items=collections.defaultdict(list); meta={}
def norm(s): return unicodedata.normalize('NFC',(s or '').strip())
for iid,fn,ln,mode,oi,title,date in db.execute(q):
    fn,ln=norm(fn),norm(ln)
    name = ln if mode==1 else (f"{fn} {ln}".strip())
    # dedupe key: last name + first initial (merges "J. Smith" / "John Smith")
    fl=re.sub(r'[^a-z ]','',unicodedata.normalize('NFKD',fn).encode('ascii','ignore').decode().lower()).split()
    key = ln.lower() if mode==1 else (ln.lower(), fl[0] if fl else '')
    items[iid].append((key,name)); meta[iid]=(title, (re.search(r'\d{4}',date or '') or [None])[0] if date else None)
total_items=db.execute("select count(*) from items i join itemTypes t using(itemTypeID) where libraryID=1 and t.typeName not in ('attachment','note','annotation') and itemID not in (select itemID from deletedItems)").fetchone()[0]
full=collections.defaultdict(set)
for a in items.values():
    for k,_ in a:
        if isinstance(k,tuple) and len(k[1])>1: full[k[0]].add(k[1])
def res(k):
    if not isinstance(k,tuple): return k
    ln,f=k
    if len(f)<=1:
        c=[x for x in full[ln] if x.startswith(f)] if f else list(full[ln])
        if len(c)==1: f=c[0]
    return ln+'|'+f
items={i:[(res(k),n) for k,n in a] for i,a in items.items()}
display={}; counts=collections.Counter(); papers=collections.defaultdict(list)
for iid,auths in items.items():
    seen=set()
    for k,n in auths:
        if k in seen: continue
        seen.add(k); counts[k]+=1; papers[k].append(meta[iid][0])
        if k not in display or len(n)>len(display[k]): display[k]=n
edges=collections.Counter()
big=0
for iid,auths in items.items():
    ks=sorted({k for k,_ in auths})
    if len(ks)>25: big+=1; continue   # skip huge consortium papers for edges
    for a,b in itertools.combinations(ks,2): edges[(a,b)]+=1
print('items with authors',len(items),'of',total_items,'authors',len(counts),'edges',len(edges),'skipped >25-author items',big)
print(counts.most_common(15))
deg=collections.Counter()
for (a,b) in edges: deg[a]+=1; deg[b]+=1
json.dump({'nodes':[{'id':k,'name':display[k],'papers':counts[k],'titles':papers[k][:8]} for k in counts],
 'links':[{'source':a,'target':b,'w':w} for (a,b),w in edges.items()],
 'stats':{'items':len(items),'total':total_items,'big':big}}, open(S+'/graph.json','w'))
