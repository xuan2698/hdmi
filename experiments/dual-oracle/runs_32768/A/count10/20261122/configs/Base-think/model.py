def reference(vectors):
    q=0
    inp={}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                inp[k]=v
        if inp.get('reset',0):
            q=0
        else:
            q=(q+1)%10
        out.append({'q':q})
        mid=row.get('mid')
        if isinstance(mid,dict):
            for k,v in mid.items():
                inp[k]=v
    return out
