def reference(vectors):
    st=0
    cur={'areset':0,'x':0}
    res=[]
    for row in vectors:
        for k in ('areset','x'):
            if k in row:
                cur[k]=int(row[k])
        if cur['areset']:
            st=0
        else:
            x=cur['x']
            if st==0:
                st=1 if x else 0
            elif st==1:
                st=2 if x else 1
            else:
                st=2 if x else 1
        res.append({'z':1 if st==1 else 0})
        mid=row.get('mid')
        if mid:
            for k,v in mid.items():
                if k in ('areset','x'):
                    cur[k]=int(v)
                    if k=='areset' and cur[k]:
                        st=0
    return res
