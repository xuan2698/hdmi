def reference(vectors):
    state = 'S0'
    out = []
    for v in vectors:
        reset = v['reset']
        data = v['data']
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
                if state == 'S0':
                    state = 'S1' if data == 1 else 'S0'
                elif state == 'S1':
                    state = 'S2' if data == 1 else 'S0'
                elif state == 'S2':
                    state = 'S3' if data == 0 else 'S2'
                elif state == 'S3':
                    state = 'S1' if data == 1 else 'S0'
                out.append({'start_shifting': 0})
    return out
