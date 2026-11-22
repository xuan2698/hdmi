def reference(vectors):
    h=12
    m=0
    s=0
    pm=0
    cur={'reset':0,'ena':0}
    out=[]
    for row in vectors:
        for k in ('reset','ena'):
            if k in row:
                cur[k]=row[k]
        reset=cur.get('reset',0)
        ena=cur.get('ena',0)
        if reset:
            h=12
            m=0
            s=0
            pm=0
        elif ena:
            s+=1
            if s==60:
                s=0
                m+=1
                if m==60:
                    m=0
                    if h==11:
                        pm^=1
                        h=12
                    elif h==12:
                        h=1
                    else:
                        h+=1
        out.append({'pm':pm,'hh':h//10*16+h%10,'mm':m//10*16+m%10,'ss':s//10*16+s%10})
        if 'mid' in row:
            for k,v in row['mid'].items():
                cur[k]=v
    return out
