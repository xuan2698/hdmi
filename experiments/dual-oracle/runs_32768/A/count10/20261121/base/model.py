def reference(vectors):
    q=0
    r=0
    o=[]
    for v in vectors:
        if 'reset' in v:
            r=v['reset']
        if r:
            q=0
        else:
            q=0 if q==9 else q+1
        o.append({'q':q&15})
        m=v.get('mid')
        if m and 'reset' in m:
            r=m['reset']
    return o
