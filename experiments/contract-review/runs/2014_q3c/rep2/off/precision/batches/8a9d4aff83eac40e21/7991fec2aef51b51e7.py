def reference(vectors):
    out=[]
    for v in vectors:
        x=v['x']; y=v['y']
        if y==0: Y=0 if x==0 else 1
        elif y==1: Y=1 if x==0 else 4
        elif y==2: Y=2 if x==0 else 1
        elif y==3: Y=1 if x==0 else 2
        elif y==4: Y=3 if x==0 else 4
        else: Y=0
        z=1 if (y==3 or y==4) else 0
        out.append({'Y0':Y&1,'z':z})
    return out