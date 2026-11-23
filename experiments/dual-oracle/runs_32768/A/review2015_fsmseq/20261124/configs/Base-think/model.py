def reference(vectors):
    s=0
    start=0
    reset=0
    data=0
    out=[]
    for row in vectors:
        if 'reset' in row: reset=row['reset']
        if 'data' in row: data=row['data']
        if reset:
            s=0
            start=0
        elif not start:
            if s==0:
                s=1 if data else 0
            elif s==1:
                if data: s=2
                else: s=0
            elif s==2:
                if data: s=2
                else: s=3
            else:
                if data:
                    start=1
                    s=0
                else:
                    s=0
        out.append({'start_shifting':start})
        mid=row.get('mid')
        if mid:
            if 'reset' in mid: reset=mid['reset']
            if 'data' in mid: data=mid['data']
    return out
