def reference(vectors):
    trans={0:{0:0,1:1},1:{0:2,1:1},2:{0:0,1:3},3:{0:2,1:1}}
    out=[0,0,0,1]
    state=0
    inp={'in':0,'reset':0}
    res=[]
    for row in vectors:
        for k in ('in','reset'):
            if k in row:
                inp[k]=row[k]
        if inp['reset']:
            state=0
        else:
            state=trans[state][inp['in']]
        res.append({'out':out[state]})
        if 'mid' in row:
            for k,v in row['mid'].items():
                inp[k]=v
    return res
