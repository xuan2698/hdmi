def reference(vectors):
    s=0
    ah=0
    bh=0
    pc=0
    out=[]
    for v in vectors:
        clk=v.get('clk',0)
        if clk==1 and pc==0:
            s=(ah&bh)|(ah&s)|(bh&s)
        a=v.get('a',ah)
        b=v.get('b',bh)
        ah=a
        bh=b
        q=a^b^s
        out.append({'q':q,'state':s})
        mid=v.get('mid')
        if mid:
            if 'a' in mid:
                ah=mid['a']
            if 'b' in mid:
                bh=mid['b']
        pc=clk
    return out
