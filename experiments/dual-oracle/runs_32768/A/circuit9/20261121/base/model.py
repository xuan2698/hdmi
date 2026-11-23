def reference(vectors):
    q=0
    prev_a=0
    clk=0
    a=0
    out=[]
    for v in vectors:
        nc=v.get('clk',clk)
        na=v.get('a',a)
        if clk==0 and nc==1:
            if na==1:
                q=4
            elif prev_a==0:
                q=(q+1)%7
            prev_a=na
        out.append({'q':q&7})
        a=na
        if 'mid' in v and 'a' in v['mid']:
            a=v['mid']['a']
        clk=nc
    return out
