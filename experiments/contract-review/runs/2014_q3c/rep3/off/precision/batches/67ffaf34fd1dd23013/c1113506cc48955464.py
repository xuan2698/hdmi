def reference(vectors):
    out=[]
    for v in vectors:
        x=v['x']; y=v['y']
        if y==0: Y0=0 if x==0 else 1
        elif y==1: Y0=1 if x==0 else 0
        elif y==2: Y0=0 if x==0 else 1
        elif y==3: Y0=1 if x==0 else 0
        elif y==4: Y0=1 if x==0 else 0
        else: Y0=0
        z=1 if (y==3 or y==4) else 0
        out.append({'Y0':Y0,'z':z})
    return out