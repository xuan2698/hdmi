def reference(vectors):
    p=0
    start=0
    inp={'reset':0,'data':0}
    out=[]
    for row in vectors:
        for k in ('reset','data'):
            if k in row:
                inp[k]=row[k]
        if inp['reset']:
            p=0
            start=0
        elif not start:
            b=inp['data']
            if p==0:
                p=1 if b else 0
            elif p==1:
                p=2 if b else 0
            elif p==2:
                p=2 if b else 3
            else:
                if b:
                    start=1
                p=0
        out.append({'start_shifting':start})
        if 'mid' in row:
            for k,v in row['mid'].items():
                if k in inp:
                    inp[k]=v
    return out
