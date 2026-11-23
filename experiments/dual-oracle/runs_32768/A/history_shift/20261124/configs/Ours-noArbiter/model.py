def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        if row.get('areset', 0):
            state = 0
        else:
            if row.get('train_mispredicted', 0):
                train_taken = row.get('train_taken', 0) & 1
                train_history = row.get('train_history', 0) & 0xffffffff
                state = ((train_history << 1) | train_taken) & 0xffffffff
            elif row.get('predict_valid', 0):
                predict_taken = row.get('predict_taken', 0) & 1
                state = ((state << 1) | predict_taken) & 0xffffffff
        outputs.append({'predict_history': state & 0xffffffff})
    return outputs
