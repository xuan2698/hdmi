def reference(vectors):
    state = 0  # initial state A
    cur_in = 0
    cur_reset = 0
    results = []
    for row in vectors:
        # Apply row's direct input values before the sampled posedge
        for k in row:
            if k == "in":
                cur_in = row[k]
            elif k == "reset":
                cur_reset = row[k]

        # Synchronous posedge update
        old_state = state
        if cur_reset == 1:
            # update_during_reset: only A updates (to A); B-D hold
            if old_state == 0:
                state = 0
            else:
                state = old_state
        else:
            # Normal transitions
            if old_state == 0:       # A
                state = 0 if cur_in == 0 else 1
            elif old_state == 1:     # B
                state = 2 if cur_in == 0 else 1
            elif old_state == 2:     # C
                state = 0 if cur_in == 0 else 3
            elif old_state == 3:     # D
                state = 2 if cur_in == 0 else 1

        # Moore output based on new state
        if state == 0:               # out_A
            out = 0
        elif state == 1:             # out_B
            out = 0
        elif state == 2:             # out_C
            out = 0
        else:                        # state == 3, out_D
            out = 1

        results.append({"out": out})

        # Optional mid input changes occur AFTER sampling and carry forward
        if "mid" in row:
            mid_val = row["mid"]
            for mk in mid_val:
                if mk == "in":
                    cur_in = mid_val[mk]
                elif mk == "reset":
                    cur_reset = mid_val[mk]

        # Handle keys like in_mid, reset_mid
        for k in row:
            if k.endswith("_mid"):
                base = k[:-4]
                if base == "in":
                    cur_in = row[k]
                elif base == "reset":
                    cur_reset = row[k]

    return results
