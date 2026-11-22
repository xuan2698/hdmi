def reference(vectors):
    # Initial state (power-up unspecified, use concrete zero)
    history = 0
    cur_areset = 0
    cur_predict_valid = 0
    cur_predict_taken = 0
    cur_train_mispredicted = 0
    cur_train_taken = 0
    cur_train_history = 0

    result = []

    for row in vectors:
        # Drive inputs before the sampled edge.
        if 'areset' in row:
            cur_areset = row['areset'] & 1
        if 'predict_valid' in row:
            cur_predict_valid = row['predict_valid'] & 1
        if 'predict_taken' in row:
            cur_predict_taken = row['predict_taken'] & 1
        if 'train_mispredicted' in row:
            cur_train_mispredicted = row['train_mispredicted'] & 1
        if 'train_taken' in row:
            cur_train_taken = row['train_taken'] & 1
        if 'train_history' in row:
            cur_train_history = row['train_history'] & 0xFFFFFFFF

        # async_reset (priority 0): areset == 1 clears history asynchronously.
        if cur_areset:
            history = 0
        else:
            # mispredict_load (priority 1)
            if cur_train_mispredicted:
                history = (((cur_train_history << 1) & 0xFFFFFFFF) | cur_train_taken) & 0xFFFFFFFF
            # predict_shift (priority 2)
            elif cur_predict_valid:
                history = (((history << 1) & 0xFFFFFFFF) | cur_predict_taken) & 0xFFFFFFFF
            # hold (priority 3): no update event, retain history.
            else:
                history = history & 0xFFFFFFFF

        # Sample output after the posedge settles.
        result.append({'predict_history': history & 0xFFFFFFFF})

        # Process optional mid-cycle changes AFTER sampling.
        if 'mid' in row and isinstance(row['mid'], dict):
            mid = row['mid']
            for k in mid:
                v = mid[k]
                if k == 'areset':
                    cur_areset = v & 1
                    if cur_areset:
                        history = 0  # asynchronous reset during mid-cycle
                elif k == 'predict_valid':
                    cur_predict_valid = v & 1
                elif k == 'predict_taken':
                    cur_predict_taken = v & 1
                elif k == 'train_mispredicted':
                    cur_train_mispredicted = v & 1
                elif k == 'train_taken':
                    cur_train_taken = v & 1
                elif k == 'train_history':
                    cur_train_history = v & 0xFFFFFFFF

        # Also support mid_<signal> representation if present.
        for k in row:
            if k.startswith('mid_'):
                name = k[4:]
                v = row[k]
                if name == 'areset':
                    cur_areset = v & 1
                    if cur_areset:
                        history = 0
                elif name == 'predict_valid':
                    cur_predict_valid = v & 1
                elif name == 'predict_taken':
                    cur_predict_taken = v & 1
                elif name == 'train_mispredicted':
                    cur_train_mispredicted = v & 1
                elif name == 'train_taken':
                    cur_train_taken = v & 1
                elif name == 'train_history':
                    cur_train_history = v & 0xFFFFFFFF

    return result
