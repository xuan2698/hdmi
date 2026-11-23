def reference(vectors):
    state=0
    fc=0
    i={'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
    r=[]
    for row in vectors:
        for k in i:
            if k in row:
                i[k]=row[k]
        if i['areset']:
            state=0
            fc=0
        else:
            g=i['ground']
            d=i['dig']
            bl=i['bump_left']
            br=i['bump_right']
            if state==0:
                if not g:
                    state=2
                    fc=0
                elif d:
                    state=4
                elif bl:
                    state=1
            elif state==1:
                if not g:
                    state=3
                    fc=0
                elif d:
                    state=5
                elif br:
                    state=0
            elif state==2:
                if g:
                    if fc>=20:
                        state=6
                    else:
                        state=0
                    fc=0
                else:
                    fc+=1
            elif state==3:
                if g:
                    if fc>=20:
                        state=6
                    else:
                        state=1
                    fc=0
                else:
                    fc+=1
            elif state==4:
                if not g:
                    state=2
                    fc=0
            elif state==5:
                if not g:
                    state=3
                    fc=0
        r.append({
            'walk_left':1 if state==0 else 0,
            'walk_right':1 if state==1 else 0,
            'aaah':1 if state in (2,3) else 0,
            'digging':1 if state in (4,5) else 0
        })
        if 'mid' in row and isinstance(row['mid'],dict):
            for k,v in row['mid'].items():
                if k in i:
                    if k=='areset' and v==1 and i[k]==0:
                        i[k]=v
                        state=0
                        fc=0
                    else:
                        i[k]=v
    return r
