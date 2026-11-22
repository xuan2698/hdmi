def reference(vectors):
    out=[]
    for v in vectors:
        L=v.get('L',0)
        q_in=v.get('q_in',0)
        r_in=v.get('r_in',0)
        Q=(r_in if L else q_in) & 1
        out.append({'Q': Q})
    return out
