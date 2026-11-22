def reference(vectors):
    q=0
    r=0
    out=[]
    for row in vectors:
        for k in row:
            if k!='mid' and k=='reset':
                r=row[k]
        if r:
            q=0
        else:
            q=(q+1)%10
        out.append({'q':q})
        m=row.get('mid')
        if m:
            if 'reset' in m:
                r=m['reset']
    return out
