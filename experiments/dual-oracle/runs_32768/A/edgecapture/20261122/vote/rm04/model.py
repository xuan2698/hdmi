def reference(vectors):
    out = 0
    prev = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            rst = row.get('reset', 0)
            cur = row.get('in', 0)
        else:
            if len(row) >= 2:
                rst, cur = row[0], row[1]
            else:
                rst, cur = 0, row[0]
        rst = int(rst) & 1
        cur = int(cur) & 0xFFFFFFFF
        if rst:
            out = 0
        else:
            out = (out | (prev & (~cur & 0xFFFFFFFF))) & 0xFFFFFFFF
        prev = cur
        result.append({'out': out})
    return result
