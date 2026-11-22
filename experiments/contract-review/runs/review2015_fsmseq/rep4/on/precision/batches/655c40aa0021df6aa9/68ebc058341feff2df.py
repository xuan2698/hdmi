def reference(vectors):
    state = 0
    cur = {'reset': 0, 'data': 0}
    out_list = []
    for v in vectors:
        rst = cur.get('reset', 0)
        dat = cur.get('data', 0)
        if 'reset' in v:
            rst = v['reset']
        if 'data' in v:
            dat = v['data']
        if rst == 1:
            start_shifting = 0
            nxt = 0
        else:
            if state == 4 or (state == 3 and dat == 1):
                start_shifting = 1
            else:
                start_shifting = 0
            if state == 0:
                nxt = 1 if dat == 1 else 0
            elif state == 1:
                nxt = 2 if dat == 1 else 0
            elif state == 2:
                nxt = 3 if dat == 0 else 2
            elif state == 3:
                nxt = 4 if dat == 1 else 0
            elif state == 4:
                nxt = 4
            else:
                nxt = 0
        out_list.append({'start_shifting': start_shifting})
        state = nxt
        cur['reset'] = rst
        cur['data'] = dat
        mid = v.get('mid')
        if mid:
            if 'reset' in mid:
                cur['reset'] = mid['reset']
            if 'data' in mid:
                cur['data'] = mid['data']
    return out_list