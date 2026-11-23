def reference(vectors):
    s=0
    x=0
    a=0
    zs=[0,1,0]
    tr=[[0,1],[1,2],[1,2]]
    r=[]
    for v in vectors:
        if 'x' in v:x=v['x']
        if 'areset' in v:a=v['areset']
        if a:s=0
        else:s=tr[s][x]
        r.append({'z':zs[s]})
        m=v.get('mid')
        if m:
            if 'x' in m:x=m['x']
            if 'areset' in m:
                a=m['areset']
                if a:s=0
    return r
