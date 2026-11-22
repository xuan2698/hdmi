def reference(vectors):
    q=0
    s={'d':0,'r':0}
    o=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                s[k]=v&1 if k in ('d','r') else v
        q=0 if s.get('r',0) else (s.get('d',0)&1)
        o.append({'q':q&1})
        m=row.get('mid')
        if m:
            for k,v in m.items():
                if k in ('d','r'):
                    s[k]=v&1
                else:
                    s[k]=v
    return o
