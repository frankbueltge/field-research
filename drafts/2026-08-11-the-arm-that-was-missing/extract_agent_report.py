import json,sys
path,out=sys.argv[1],sys.argv[2]
last=None
for line in open(path,encoding="utf-8"):
    line=line.strip()
    if not line: continue
    try: o=json.loads(line)
    except Exception: continue
    def texts(msg):
        c=msg.get("content")
        if isinstance(c,str): return c
        if isinstance(c,list):
            return "".join(b.get("text","") for b in c if isinstance(b,dict) and b.get("type")=="text")
        return ""
    m=o.get("message") or (o if o.get("role") else None)
    if isinstance(m,dict) and m.get("role")=="assistant":
        t=texts(m)
        if t.strip(): last=t
open(out,"w",encoding="utf-8").write(last or "")
print(out, len(last or ""), "chars")
