def reference(vectors):
    state = 0  # 0: no 1 yet, 1: seen and z=1, 2: seen and z=0
    result = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)
        if areset:
            state = 0
            z = 0
        else:
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
        result.append({'z': z})
    return result
