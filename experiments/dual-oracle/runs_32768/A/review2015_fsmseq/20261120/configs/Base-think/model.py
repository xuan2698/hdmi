def reference(vectors):
    r=[]; s=0; o=0; reset=0; data=0
    for row in vectors:
        reset=row.get('reset',reset)
        data=row.get('data',data)
        if reset:
            s=0; o=0
        elif not o:
            if s==0:
                s=1 if data else 0
            elif s==1:
                s=2 if data else 0
            elif s==2:
                s=2 if data else 3
            else:
                if data: o=1
                s=0
        r.append({'start_shifting':o})
        mid=row.get('mid',{})
        reset=mid.get('reset',reset)
        data=mid.get('data',data)
    return r
