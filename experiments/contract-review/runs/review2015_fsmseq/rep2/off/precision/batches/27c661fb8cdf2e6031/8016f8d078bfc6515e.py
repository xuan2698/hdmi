def reference(vectors):
    out = []
    state = 'S0'
    for v in vectors:
        reset = v.get('reset', 0)
        data = v.get('data', 0)
        if reset == 1:
            state = 'S0'
            out.append({'start_shifting': 0})
        else:
            if state == 'S4':
                out.append({'start_shifting': 1})
            elif state == 'S3' and data == 1:
                state = 'S4'
                out.append({'start_shifting': 1})
            else:
                out.append({'start_shifting': 0})
                if state == 'S0':
                    state = 'S1' if data == 1 else 'S0'
                elif state == 'S1':
                    state = 'S2' if data == 1 else 'S0'
                elif state == 'S2':
                    state = 'S3' if data == 0 else 'S2'
                elif state == 'S3':
                    state = 'S1' if data == 1 else 'S0'
    return out
