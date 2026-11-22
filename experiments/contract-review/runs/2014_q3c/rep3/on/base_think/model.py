def reference(vectors):
    st={'x':0,'y':0}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid': st[k]=v
        x=st.get('x',0)&1
        y=st.get('y',0)&7
        y0=y&1; y1=(y>>1)&1; y2=(y>>2)&1
        Y0=(x^((y0|y2)&1))&1
        z=(y2|(y1&y0))&1
        out.append({'Y0':Y0,'z':z})
        if 'mid' in row:
            for k,v in row['mid'].items(): st[k]=v
    return out
