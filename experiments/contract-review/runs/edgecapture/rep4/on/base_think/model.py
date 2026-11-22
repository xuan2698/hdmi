def reference(vectors):
    m=0xffffffff
    out=0
    prev=0
    rst=0
    inp=0
    ans=[]
    for r in vectors:
        rst=r.get('reset',rst)
        inp=r.get('in',inp)&m
        if rst:
            out=0
        else:
            out=(out|(prev&(inp^m)))&m
        prev=inp
        ans.append({'out':out})
        mid=r.get('mid')
        if mid:
            rst=mid.get('reset',rst)
            inp=mid.get('in',inp)&m
    return ans
