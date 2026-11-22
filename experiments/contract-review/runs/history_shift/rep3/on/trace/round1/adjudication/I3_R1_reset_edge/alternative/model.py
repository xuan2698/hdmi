def reference(vectors):
    # R1_async_reset: state initialized to 0; reset is edge-triggered on 0->1 areset.
    history_reg = 0

    # Current input values, including mid-cycle changes from the previous row.
    inputs = {
        'areset': 0,
        'predict_valid': 0,
        'predict_taken': 0,
        'train_mispredicted': 0,
        'train_taken': 0,
        'train_history': 0
    }

    outputs = []

    for row in vectors:
        # Determine the input values presented before this sampled clock edge.
        row_vals = {}
        for key in inputs:
            if key in row:
                row_vals[key] = row[key]
            else:
                row_vals[key] = inputs[key]

        # R1_async_reset: asynchronous reset only on a 0-to-1 transition of areset.
        # This happens before the clock edge, so clocked updates may still occur
        # on the same sampled edge if areset remains high.
        old_areset = inputs['areset']
        new_areset = row_vals['areset']
        if old_areset == 0 and new_areset == 1:
            history_reg = 0

        # The row's values are now the stable values before the posedge.
        inputs.update(row_vals)

        # Posedge clocked update.
        if row_vals['train_mispredicted']:
            # R2_train_mispredicted_load: load history after the mispredicted branch.
            # Standard truncation: new = ((train_history << 1) | train_taken) & 0xFFFFFFFF.
            th = row_vals['train_history'] & 0xFFFFFFFF
            tt = row_vals['train_taken'] & 1
            history_reg = ((th << 1) | tt) & 0xFFFFFFFF
        elif row_vals['predict_valid']:
            # R3_predict_update: shift predict_taken in at the LSB side.
            pt = row_vals['predict_taken'] & 1
            history_reg = ((history_reg << 1) | pt) & 0xFFFFFFFF
        else:
            # R4_hold: no update, history_reg holds its value.
            pass

        # Output is sampled after the posedge has settled.
        outputs.append({'predict_history': history_reg & 0xFFFFFFFF})

        # Mid-cycle input changes occur after sampling and before the next edge.
        if 'mid' in row and row['mid']:
            mid = row['mid']

            # R1_async_reset: a mid-cycle 0->1 on areset resets the state immediately.
            if 'areset' in mid:
                old = inputs['areset']
                new = mid['areset']
                if old == 0 and new == 1:
                    history_reg = 0
                inputs['areset'] = new

            # Carry other mid-cycle changes forward to the start of the next row.
            for key, value in mid.items():
                if key == 'areset':
                    continue
                if key in inputs:
                    inputs[key] = value

    return outputs
