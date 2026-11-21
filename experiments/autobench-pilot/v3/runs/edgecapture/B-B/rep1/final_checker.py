def reference(vectors):
    out = 0
    prev = 0
    res = []
    for row in vectors:
        if row.get('reset'):
            out = 0
        else:
            out |= prev & ~row['in']
        prev = row['in']
        res.append({'out': out & 0xFFFFFFFF})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset'):
                out = 0
            else:
                if 'in' in m:
                    out |= prev & ~m['in']
                    prev = m['in']
            res[-1]['out'] = out & 0xFFFFFFFF
    return res
