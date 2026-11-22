def reference(vectors):
    s={'d':0,'reset':0}
    q=0
    out=[]
    for v in vectors:
        for k in s:
            if k in v:
                s[k]=v[k]
        q=0x34 if s['reset'] else (s['d']&255)
        out.append({'q':q})
        if 'mid' in v:
            for k,x in v['mid'].items():
                if k in s:
                    s[k]=x
    return out
