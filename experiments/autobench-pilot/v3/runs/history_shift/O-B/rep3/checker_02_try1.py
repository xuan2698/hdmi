def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        if row.get('areset', 0):
            state = 0
        else:
            if row.get('train_mispredicted', 0):
                state = ((row.get('train_history', 0) << 1) | row.get('train_taken', 0)) & 0xFFFFFFFF
            elif row.get('predict_valid', 0):
                state = ((state << 1) | row.get('predict_taken', 0)) & 0xFFFFFFFF
        out.append({'predict_history': state})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset', 0):
                state = 0
            else:
                if m.get('train_mispredicted', 0):
                    state = ((m.get('train_history', row.get('train_history', 0)) << 1) | m.get('train_taken', row.get('train_taken', 0))) & 0xFFFFFFFF
                elif m.get('predict_valid', 0):
                    state = ((state << 1) | m.get('predict_taken', row.get('predict_taken', 0))) & 0xFFFFFFFF
    return out
