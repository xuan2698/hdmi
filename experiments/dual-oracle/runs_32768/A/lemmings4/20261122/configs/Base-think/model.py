def reference(vectors):
    state=0
    c=0
    inp={'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
    res=[]
    for r in vectors:
        for k in ('areset','bump_left','bump_right','ground','dig'):
            if k in r:
                inp[k]=r[k]
        if inp['areset']:
            state=0
            c=0
        else:
            g=inp['ground']
            bl=inp['bump_left']
            br=inp['bump_right']
            d=inp['dig']
            if state==0:
                if not g:
                    state=4
                    c=1
                elif d:
                    state=2
                elif bl:
                    state=1
            elif state==1:
                if not g:
                    state=5
                    c=1
                elif d:
                    state=3
                elif br:
                    state=0
            elif state==2:
                if not g:
                    state=4
                    c=1
            elif state==3:
                if not g:
                    state=5
                    c=1
            elif state==4:
                if g:
                    if c>20:
                        state=6
                        c=0
                    else:
                        state=0
                        c=0
                else:
                    c+=1
            elif state==5:
                if g:
                    if c>20:
                        state=6
                        c=0
                    else:
                        state=1
                        c=0
                else:
                    c+=1
        o={'walk_left':0,'walk_right':0,'aaah':0,'digging':0}
        if state==0:
            o['walk_left']=1
        elif state==1:
            o['walk_right']=1
        elif state==2 or state==3:
            o['digging']=1
        elif state==4 or state==5:
            o['aaah']=1
        res.append(o)
        m=r.get('mid')
        if m:
            for k,v in m.items():
                inp[k]=v
                if k=='areset' and v==1:
                    state=0
                    c=0
    return res
