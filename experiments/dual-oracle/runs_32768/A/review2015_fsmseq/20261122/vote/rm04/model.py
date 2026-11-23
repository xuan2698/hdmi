def reference(vectors):
    state = 0
    out = 0
    result = []
    for row in vectors:
        reset = row.get('reset', 0)
        data = row.get('data', 0)
        if reset:
            state = 0
            out = 0
        elif not out:
            if state == 0:
                state = 1 if data else 0
            elif state == 1:
                state = 2 if data else 0
            elif state == 2:
                state = 2 if data else 3
            else:
                if data:
                    out = 1
                    state = 0
                else:
                    state = 0
        result.append({'start_shifting': out})
    return result
