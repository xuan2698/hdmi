def reference(vectors):
    out = []
    state = 'S0'
    for v in vectors:
        reset = v['reset']
        data = v['data']
        if reset == 1:
            state = 'S0'
            out.append({'start_shifting': 0})
        else:
            if state == 'S4':
                out.append({'start_shifting': 1})
            else:
                if state == 'S0':
                    ns = 'S1' if data == 1 else 'S0'
                elif state == 'S1':
                    ns = 'S2' if data == 1 else 'S0'
                elif state == 'S2':
                    ns = 'S3' if data == 0 else 'S2'
                elif state == 'S3':
                    ns = 'S4' if data == 1 else 'S0'
                else:
                    ns = 'S4'
                if ns == 'S4':
                    out.append({'start_shifting': 1})
                else:
                    out.append({'start_shifting': 0})
                state = ns
    return out
