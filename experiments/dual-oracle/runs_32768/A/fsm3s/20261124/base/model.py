def reference(vectors):
    trans = {
        'A': {'0': 'A', '1': 'B'},
        'B': {'0': 'C', '1': 'B'},
        'C': {'0': 'A', '1': 'D'},
        'D': {'0': 'C', '1': 'B'}
    }
    out = {'A': 0, 'B': 0, 'C': 0, 'D': 1}
    state = 'A'
    cur = {'in': 0, 'reset': 0}
    result = []
    for row in vectors:
        for k in cur:
            if k in row:
                cur[k] = int(row[k])
        if cur['reset']:
            state = 'A'
        else:
            state = trans[state][str(cur['in'])]
        result.append({'out': out[state]})
        mid = row.get('mid')
        if mid:
            for k in cur:
                if k in mid:
                    cur[k] = int(mid[k])
    return result
