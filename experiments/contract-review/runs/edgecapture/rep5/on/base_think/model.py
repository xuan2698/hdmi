def reference(vectors):
    mask=(1<<32)-1
    out=0
    prev=0
    cur={'reset':0,'in':0}
    res=[]
    for row in vectors:
        for k,v in row.items():
            if k not in ('mid','clk'):
                cur[k]=v
        r=cur.get('reset',0)
        i=cur.get('in',0)&mask
        if r:
            out=0
        else:
            out=(out | (prev & (~i & mask)))&mask
        prev=i
        res.append({'out':out})
        if 'mid' in row:
            for k,v in row['mid'].items():
                if k!='clk':
                    cur[k]=v
    return res
