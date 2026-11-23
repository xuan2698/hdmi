def reference(vectors):
    cur={'x':0,'y':0}
    out=[]
    for r in vectors:
        for k in ('x','y'):
            if k in r: cur[k]=r[k]
        x=cur['x']&1
        y=cur['y']&7
        a=(y>>2)&1
        b=(y>>1)&1
        c=y&1
        Y0=(((a^1)&(c^x))|(a&(x^1)))&1
        z=(a|(b&c))&1
        out.append({'Y0':Y0,'z':z})
        if 'mid' in r:
            for k,v in r['mid'].items():
                if k in cur: cur[k]=v
    return out
