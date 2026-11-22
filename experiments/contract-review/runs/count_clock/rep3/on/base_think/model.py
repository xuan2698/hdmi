def reference(vectors):
    t=0
    reset=0
    ena=0
    out=[]
    for row in vectors:
        for k in ('reset','ena'):
            if k in row:
                if k=='reset':
                    reset=row[k]&1
                else:
                    ena=row[k]&1
        if reset:
            t=0
        elif ena:
            t=(t+1)%86400
        h24=(t//3600)%24
        h12=h24%12
        if h12==0:
            h12=12
        m=(t//60)%60
        s=t%60
        out.append({'pm':1 if h24>=12 else 0,'hh':((h12//10)<<4)|(h12%10),'mm':((m//10)<<4)|(m%10),'ss':((s//10)<<4)|(s%10)})
        if 'mid' in row:
            mid=row['mid']
            for k in ('reset','ena'):
                if k in mid:
                    if k=='reset':
                        reset=mid[k]&1
                    else:
                        ena=mid[k]&1
    return out
