def reference(vectors):
    d=0
    reset=0
    q=0
    out=[]
    for v in vectors:
        if 'd' in v:
            d=v['d']
        if 'reset' in v:
            reset=v['reset']
        q=0x34 if reset else d
        q &= 0xFF
        out.append({'q':q})
        m=v.get('mid')
        if m is not None:
            if 'd' in m:
                d=m['d']
            if 'reset' in m:
                reset=m['reset']
    return out
