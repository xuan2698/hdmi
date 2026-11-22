def reference(vectors):
    state = 'S0'
    out = []
    for v in vectors:
        reset = v['reset']
        data = v['data']
        if reset == 1:
            start_shifting = 0
            state = 'S0'
        else:
            if state == 'S4':
                start_shifting = 1
            elif state == 'S3' and data == 1:
                start_shifting = 1
                state = 'S4'
            else:
                start_shifting = 0
                if state == 'S0':
                    if data == 1:
                        state = 'S1'
                elif state == 'S1':
                    if data == 1:
                        state = 'S2'
                    else:
                        state = 'S0'
                elif state == 'S2':
                    if data == 0:
                        state = 'S3'
                    else:
                        state = 'S2'
                elif state == 'S3':
                    if data == 1:
                        state = 'S4'
                    else:
                        state = 'S0'
        out.append({'start_shifting': start_shifting})
    return out
