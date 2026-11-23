def reference(vectors):
    q=0
    reset=0
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid' and k=='reset':
                reset=v
        if reset:
            q=0
        else:
            d=[(q>>(4*i))&15 for i in range(4)]
            nd=[0,0,0,0]
            carry=1
            for i in range(4):
                if carry and d[i]==9:
                    nd[i]=0
                elif carry:
                    nd[i]=d[i]+1
                    carry=0
                else:
                    nd[i]=d[i]
            q=sum(nd[i]<<(4*i) for i in range(4))
        d=[(q>>(4*i))&15 for i in range(4)]
        e=0
        p=1
        for i in range(3):
            p=p and d[i]==9
            if p:
                e=e|(1<<i)
        out.append({'ena':e&7,'q':q&65535})
        for k,v in row.get('mid',{}).items():
            if k=='reset':
                reset=v
    return out
