def reference(vectors):
    state = 0  # 0: no 1 yet, 1: seen 1 output 1, 2: seen 1 output 0
    out = []
    for row in vectors:
        if int(row['areset']):
            state = 0
        else:
            x = int(row['x'])
            if state == 0:
                state = 1 if x else 0
            elif state == 1:
                state = 2 if x else 1
            else:
                state = 2 if x else 1
        out.append({'z': 1 if state == 1 else 0})
    return out
