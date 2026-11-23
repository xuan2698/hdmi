def reference(vectors):
    s=0
    o=[0,0,0,1]
    t=[[0,1],[2,1],[0,3],[2,1]]
    i={'in':0,'reset':0}
    r=[]
    for row in vectors:
        for k in ('in','reset'):
            if k in row:i[k]=row[k]
        if i['reset']:
            s=0
        else:
            s=t[s][i['in']]
        r.append({'out':o[s]})
        if 'mid' in row:
            for k in ('in','reset'):
                if k in row['mid']:
                    i[k]=row['mid'][k]
    return r
