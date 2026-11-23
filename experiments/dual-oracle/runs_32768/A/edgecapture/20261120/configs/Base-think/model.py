def reference(vectors):
    M=(1<<32)-1
    out=0
    prev=0
    reset=0
    inp=0
    ans=[]
    for row in vectors:
        if 'reset' in row:
            reset=row['reset']&1
        if 'in' in row:
            inp=row['in']&M
        if reset:
            out=0
        else:
            out=(out|(prev&~inp))&M
        prev=inp
        ans.append({'out':out})
        if 'mid' in row:
            mid=row['mid']
            if 'reset' in mid:
                reset=mid['reset']&1
            if 'in' in mid:
                inp=mid['in']&M
    return ans
