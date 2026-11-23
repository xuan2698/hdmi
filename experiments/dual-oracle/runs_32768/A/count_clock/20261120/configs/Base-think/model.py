def reference(vectors):
    def bcd(n):
        return (n//10)*16+n%10
    t=0
    pm=0
    cur={'reset':0,'ena':0}
    out=[]
    for r in vectors:
        for k,v in r.items():
            if k!='mid':
                cur[k]=v
        if cur.get('reset',0):
            t=0
            pm=0
        elif cur.get('ena',0):
            if t==43199:
                t=0
                pm^=1
            else:
                t+=1
        h=t//3600
        if h==0:
            h=12
        m=(t%3600)//60
        s=t%60
        out.append({'pm':pm,'hh':bcd(h),'mm':bcd(m),'ss':bcd(s)})
        if 'mid' in r:
            for k,v in r['mid'].items():
                cur[k]=v
    return out
