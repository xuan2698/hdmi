def reference(vectors):
    state = 'S0'
    out = []
    for row in vectors:
        if row['reset']:
            state = 'S0'
        else:
            data = row['data'] & 1
            if state == 'S0':
                if data:
                    state = 'S1'
            elif state == 'S1':
                if data:
                    state = 'S2'
                else:
                    state = 'S0'
            elif state == 'S2':
                if data:
                    state = 'S2'
                else:
                    state = 'S3'
            elif state == 'S3':
                if data:
                    state = 'DONE'
                else:
                    state = 'S0'
        out.append({'start_shifting': 1 if state == 'DONE' else 0})
    return out
