def reference(vectors):
    st=0
    cur={'areset':0,'x':0}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                cur[k]=v
        if cur.get('areset',0):
            st=0
        else:
            x=cur.get('x',0)
            if st==0:
                st=1 if x else 0
            else:
                st=2 if x else 1
        out.append({'z':1 if st==1 else 0})
        if 'mid' in row:
            cur.update(row['mid'])
            if cur.get('areset',0):
                st=0
    return out
