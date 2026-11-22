def reference(vectors):
    s='A'
    h={}
    r=[]
    o={'A':0,'B':0,'C':0,'D':1}
    n={('A',0):'A',('A',1):'B',('B',0):'C',('B',1):'B',('C',0):'A',('C',1):'D',('D',0):'C',('D',1):'B'}
    for v in vectors:
        i=h.copy()
        for k in v:
            if k!='mid':
                i[k]=v[k]
        if i.get('reset',0):
            s='A'
        else:
            s=n.get((s,i.get('in',0)),s)
        r.append({'out':o[s]})
        if 'mid' in v:
            for k in v['mid']:
                i[k]=v['mid'][k]
        h=i
    return r
