def reference(vectors):
    state=0
    cnt=0
    cur={'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
    out=[]
    for r in vectors:
        for k in cur:
            if k in r:
                cur[k]=r[k]
        if cur['areset']:
            state=0
            cnt=0
        else:
            g=cur['ground']
            d=cur['dig']
            bl=cur['bump_left']
            br=cur['bump_right']
            if state==6:
                pass
            elif state in (2,3):
                if g:
                    if cnt>20:
                        state=6
                    else:
                        state=0 if state==2 else 1
                    cnt=0
                else:
                    cnt+=1
            elif state in (4,5):
                if not g:
                    state=2 if state==4 else 3
                    cnt=1
            else:
                if not g:
                    state=2 if state==0 else 3
                    cnt=1
                elif d:
                    state=4 if state==0 else 5
                elif state==0:
                    if bl:
                        state=1
                else:
                    if br:
                        state=0
        out.append({'walk_left':1 if state==0 else 0,
                    'walk_right':1 if state==1 else 0,
                    'aaah':1 if state in (2,3) else 0,
                    'digging':1 if state in (4,5) else 0})
        if 'mid' in r:
            m=r['mid']
            for k in cur:
                if k in m:
                    cur[k]=m[k]
            if m.get('areset',0):
                state=0
                cnt=0
    return out
