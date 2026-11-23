def reference(vectors):
    state = 0  # 0: before first 1; 1: after first 1, last output 1; 2: after first 1, last output 0
    out = []
    for row in vectors:
        if row.get('areset', 0):
            state = 0
            z = 0
        else:
            x = row['x']
            if state == 0:
                if x:
                    state = 1
                    z = 1
                else:
                    state = 0
                    z = 0
            else:
                if x:
                    state = 2
                    z = 0
                else:
                    state = 1
                    z = 1
        out.append({'z': z})
    return out
