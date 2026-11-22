def reference(vectors):
    s={'x':0,'y':0}
    r=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                s[k]=v
        x=s.get('x',0)&1
        y=s.get('y',0)&7
        y2=(y>>2)&1
        y1=(y>>1)&1
        y0=y&1
        Y0=(x^((y2|y0)&1))&1
        z=(y2|(y1&y0))&1
        r.append({'Y0':Y0,'z':z})
        m=row.get('mid')
        if m:
            for k,v in m.items():
                s[k]=v
    return r
