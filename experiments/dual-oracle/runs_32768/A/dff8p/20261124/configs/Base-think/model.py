def reference(vectors):
    q=0
    d=0
    reset=0
    out=[]
    for row in vectors:
        if 'd' in row: d=row['d']
        if 'reset' in row: reset=row['reset']
        q=0x34 if reset else d&0xFF
        out.append({'q':q&0xFF})
        if 'mid' in row:
            mid=row['mid']
            if 'd' in mid: d=mid['d']
            if 'reset' in mid: reset=mid['reset']
    return out
