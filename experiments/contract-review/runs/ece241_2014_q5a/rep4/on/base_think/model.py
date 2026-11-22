def reference(vectors):
    s=0
    a=0
    xv=0
    out=[]
    for row in vectors:
        if 'areset' in row:
            a=row['areset']
        if 'x' in row:
            xv=row['x']
        if a:
            s=0
        else:
            if s==0:
                s=1 if xv else 0
            else:
                s=1 if not xv else 2
        out.append({'z':1 if s==1 else 0})
        m=row.get('mid',{})
        if 'areset' in m:
            a=m['areset']
            if a:
                s=0
        if 'x' in m:
            xv=m['x']
    return out
