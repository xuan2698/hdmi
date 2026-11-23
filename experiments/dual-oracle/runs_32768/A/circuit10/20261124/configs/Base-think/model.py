def reference(vectors):
    s=0
    a=0
    b=0
    r=[]
    for v in vectors:
        if "a" in v:
            a=int(v["a"])&1
        if "b" in v:
            b=int(v["b"])&1
        old=s
        s=(a&b)|(old&(a|b))
        q=s^a^b
        r.append({"q":q&1,"state":s&1})
        if "mid" in v and v["mid"] is not None:
            m=v["mid"]
            if "a" in m:
                a=int(m["a"])&1
            if "b" in m:
                b=int(m["b"])&1
    return r
