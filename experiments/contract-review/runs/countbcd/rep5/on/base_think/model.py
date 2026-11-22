def reference(vectors):
    q=0
    r=0
    out=[]
    for row in vectors:
        if 'reset' in row:
            r=int(row['reset'])&1
        if r:
            q=0
        else:
            d=[(q>>(4*i))&15 for i in range(4)]
            i=0
            while i<4:
                d[i]+=1
                if d[i]<10:
                    break
                d[i]=0
                i+=1
            q=0
            for i in range(4):
                q|=(d[i]&15)<<(4*i)
        e0=(q&15)==9
        e1=e0 and ((q>>4)&15)==9
        e2=e1 and ((q>>8)&15)==9
        ena=int(e0)+2*int(e1)+4*int(e2)
        out.append({'ena':ena,'q':q})
        if 'mid' in row:
            m=row['mid']
            if 'reset' in m:
                r=int(m['reset'])&1
    return out
