def reference(vectors):
    state=0
    a=0
    b=0
    result=[]
    for v in vectors:
        if 'a' in v: a=v['a']
        if 'b' in v: b=v['b']
        state=(a&b)|(state&(a|b))
        q=state^a^b
        result.append({'q':q,'state':state})
        if 'mid' in v:
            m=v['mid']
            if 'a' in m: a=m['a']
            if 'b' in m: b=m['b']
    return result
