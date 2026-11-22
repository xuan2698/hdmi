def reference(vectors):
    q=0
    inp={'L':0,'q_in':0,'r_in':0}
    out=[]
    for row in vectors:
        for k in inp:
            if k in row:
                inp[k]=row[k]&1
        q=(inp['r_in'] if inp['L'] else inp['q_in'])&1
        out.append({'Q':q})
        if 'mid' in row:
            for k in inp:
                if k in row['mid']:
                    inp[k]=row['mid'][k]&1
    return out
