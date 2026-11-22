def reference(vectors):
    state = 0
    cur = {'reset': 0, 'data': 0}
    result = []
    for row in vectors:
        for key in row:
            if key != 'mid':
                cur[key] = row[key]
        if cur.get('reset', 0):
            state = 0
        elif state != 4:
            data = cur.get('data', 0)
            if state == 0:
                state = 1 if data else 0
            elif state == 1:
                state = 2 if data else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                state = 4 if data else 0
        result.append({'start_shifting': 1 if state == 4 else 0})
        if 'mid' in row:
            for key, value in row['mid'].items():
                cur[key] = value
    return result
