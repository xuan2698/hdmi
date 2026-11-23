def reference(vectors):
    state = 0  # 0: no first 1 yet; 1: after first 1, output 1; 2: after first 1, output 0
    result = []
    for row in vectors:
        if row.get('areset', 0):
            state = 0
        else:
            x = row.get('x', 0)
            if state == 0:
                if x:
                    state = 1
            elif state == 1:
                if x:
                    state = 2
            else:
                if not x:
                    state = 1
        result.append({'z': 1 if state == 1 else 0})
        mid = row.get('mid')
        if isinstance(mid, dict) and mid.get('areset', 0):
            state = 0
    return result
