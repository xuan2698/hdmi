def reference(vectors):
    q=0x34
    st={'d':0,'reset':0}
    out=[]
    for row in vectors:
        for k in st:
            if k in row:
                st[k]=row[k]
        if st['reset']&1:
            q=0x34
        else:
            q=st['d']&0xFF
        out.append({'q':q})
        mid=row.get('mid',{})
        for k,v in mid.items():
            if k in st:
                st[k]=v
    return out
