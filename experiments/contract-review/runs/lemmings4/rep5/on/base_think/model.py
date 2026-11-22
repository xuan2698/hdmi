def reference(vectors):
    keys=('areset','bump_left','bump_right','ground','dig')
    cur={k:0 for k in keys}
    st=0
    cnt=0
    res=[]
    outs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,0),(0,0,0,1),(0,0,0,1),(0,0,0,0)]
    names=('walk_left','walk_right','aaah','digging')
    for r in vectors:
        for k in keys:
            if k in r:
                cur[k]=r[k]
        if cur['areset']:
            st=0
            cnt=0
        elif st==6:
            pass
        elif st<2:
            if not cur['ground']:
                st=2 if st==0 else 3
                cnt=0
            elif cur['dig']:
                st=4 if st==0 else 5
                cnt=0
            else:
                if st==0 and cur['bump_left']:
                    st=1
                elif st==1 and cur['bump_right']:
                    st=0
                cnt=0
        elif st<4:
            if cur['ground']:
                if cnt>=20:
                    st=6
                else:
                    st=0 if st==2 else 1
                cnt=0
            else:
                cnt+=1
        else:
            if not cur['ground']:
                st=2 if st==4 else 3
                cnt=0
            else:
                cnt=0
        vals=outs[st]
        res.append({names[i]:vals[i] for i in range(4)})
        m=r.get('mid') or {}
        for k in keys:
            if k in m:
                cur[k]=m[k]
        if m.get('areset',0):
            st=0
            cnt=0
    return res
