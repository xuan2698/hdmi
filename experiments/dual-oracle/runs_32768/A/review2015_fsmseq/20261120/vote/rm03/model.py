def reference(vectors):
    s0, s1, s11, s110, found = 0, 1, 2, 3, 4
    state = s0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row['reset']
        data = row['data']

        if reset:
            state = s0
            start_shifting = 0
        else:
            if state == found:
                state = found
            elif state == s0:
                state = s1 if data else s0
            elif state == s1:
                state = s11 if data else s0
            elif state == s11:
                state = s11 if data else s110
            elif state == s110:
                if data:
                    state = found
                    start_shifting = 1
                else:
                    state = s0

        out.append({'start_shifting': start_shifting})

    return out
