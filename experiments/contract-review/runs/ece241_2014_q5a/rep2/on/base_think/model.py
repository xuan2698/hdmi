def reference(vectors):
    s=0
    held={}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid' and k!='clk':
                held[k]=v
        a=held.get('areset',0)
        if a:
            s=0
        if a:
            s=0
        else:
            x=held.get('x',0)
            if s==0:
                s=1 if x else 0
            elif s==1:
                s=2 if x else 1
            else:
                s=1 if not x else 2
        out.append({'z':1 if s==1 else 0})
        mid=row.get('mid',{})
        for k,v in mid.items():
            if k!='clk':
                held[k]=v
        if held.get('areset',0):
            s=0
    return out
