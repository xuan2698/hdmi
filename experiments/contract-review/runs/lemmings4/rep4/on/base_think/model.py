def reference(vectors):
    L,R,FL,FR,DL,DR,DEAD=range(7)
    st=L; fc=0; ins={'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}; out=[]
    for row in vectors:
        for k in ins:
            if k in row: ins[k]=row[k]
        if ins['areset']:
            st=L; fc=0
        else:
            if st==L:
                if not ins['ground']: st=FL; fc=1
                elif ins['dig']: st=DL
                elif ins['bump_left']: st=R
            elif st==R:
                if not ins['ground']: st=FR; fc=1
                elif ins['dig']: st=DR
                elif ins['bump_right']: st=L
            elif st==FL:
                if ins['ground']:
                    if fc>20: st=DEAD
                    else: st=L
                else: fc+=1; st=FL
            elif st==FR:
                if ins['ground']:
                    if fc>20: st=DEAD
                    else: st=R
                else: fc+=1; st=FR
            elif st==DL:
                if not ins['ground']: st=FL; fc=1
            elif st==DR:
                if not ins['ground']: st=FR; fc=1
        out.append({'walk_left':1 if st==L else 0,'walk_right':1 if st==R else 0,'aaah':1 if st in (FL,FR) else 0,'digging':1 if st in (DL,DR) else 0})
        mid=row.get('mid',{})
        for k,v in mid.items(): ins[k]=v
        if mid.get('areset',0)==1:
            st=L; fc=0
    return out
