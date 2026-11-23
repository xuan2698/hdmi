def reference(vectors):
    s={'L':0,'q_in':0,'r_in':0}
    o=[]
    for row in vectors:
        for k in ('L','q_in','r_in'):
            if k in row:
                s[k]=row[k]&1
        q=(s['r_in'] if (s['L']&1) else s['q_in'])&1
        o.append({'Q':q})
        m=row.get('mid')
        if isinstance(m,dict):
            for k,v in m.items():
                if k in s:
                    s[k]=v&1
    return o
