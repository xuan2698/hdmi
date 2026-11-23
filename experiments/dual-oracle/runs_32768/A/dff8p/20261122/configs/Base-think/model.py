def reference(vectors):
    q=0
    d=0
    reset=0
    out=[]
    for row in vectors:
        if 'd' in row: d=row['d']&0xff
        if 'reset' in row: reset=row['reset']&1
        if reset: q=0x34
        else: q=d&0xff
        out.append({'q':q})
        mid=row.get('mid')
        if mid:
            if 'd' in mid: d=mid['d']&0xff
            if 'reset' in mid: reset=mid['reset']&1
    return out
