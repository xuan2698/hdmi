def reference(vectors):
    mode=0
    d=0
    cnt=0
    cur={'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k=='mid':
                continue
            old=cur.get(k,0)
            cur[k]=v
            if k=='areset' and old==0 and v==1:
                mode=0; d=0; cnt=0
        if cur['areset']:
            mode=0; d=0; cnt=0
        elif mode==0:
            if cur['ground']==0:
                mode=1; cnt=1
            elif cur['dig']:
                mode=2
            else:
                bl=cur['bump_left']; br=cur['bump_right']
                if bl and br:
                    d=1-d
                elif bl:
                    d=1
                elif br:
                    d=0
        elif mode==1:
            if cur['ground']:
                if cnt>20:
                    mode=3; cnt=0
                else:
                    mode=0; cnt=0
            else:
                cnt+=1
        elif mode==2:
            if cur['ground']==0:
                mode=1; cnt=1
        if mode==0:
            o={'walk_left':1 if d==0 else 0,'walk_right':1 if d==1 else 0,'aaah':0,'digging':0}
        elif mode==1:
            o={'walk_left':0,'walk_right':0,'aaah':1,'digging':0}
        elif mode==2:
            o={'walk_left':0,'walk_right':0,'aaah':0,'digging':1}
        else:
            o={'walk_left':0,'walk_right':0,'aaah':0,'digging':0}
        out.append(o)
        mid=row.get('mid')
        if mid:
            for k,v in mid.items():
                old=cur.get(k,0)
                cur[k]=v
                if k=='areset' and old==0 and v==1:
                    mode=0; d=0; cnt=0
    return out
