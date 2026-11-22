def reference(vectors):
    # Named states: S0, S1, S11, S110, FOUND
    state = "S0"
    carried_reset = 0
    carried_data = 0
    outputs = []

    for row in vectors:
        # Inputs driven before the sampled posedge override carried mid changes.
        if "reset" in row:
            reset = row["reset"]
        else:
            reset = carried_reset
        if "data" in row:
            data = row["data"]
        else:
            data = carried_data

        # Compute state and output after the posedge has settled.
        if reset == 1:
            # R_RESET: active-high synchronous reset, priority 0, same-cycle start_shifting=0.
            next_state = "S0"
            out = 0
        else:
            if state == "FOUND":
                # R_HOLD_FOUND: reset==0 and state==FOUND, hold start_shifting=1 forever.
                next_state = "FOUND"
                out = 1
            elif state == "S110" and data == 1:
                # R_COMPLETE_1101: reset==0, state==S110, data==1 completes 1101.
                next_state = "FOUND"
                out = 1
            else:
                # R_ZERO_NOT_FOUND: reset==0 and not found/completion, start_shifting=0.
                out = 0
                if state == "S0":
                    if data == 1:
                        next_state = "S1"
                    else:
                        next_state = "S0"
                elif state == "S1":
                    if data == 1:
                        next_state = "S11"
                    else:
                        next_state = "S0"
                elif state == "S11":
                    if data == 1:
                        next_state = "S11"
                    else:
                        next_state = "S110"
                elif state == "S110":
                    if data == 1:
                        # Explicit transition for completeness; handled above by R_COMPLETE_1101.
                        next_state = "FOUND"
                        out = 1
                    else:
                        next_state = "S0"
                else:
                    next_state = "S0"
                    out = 0

        outputs.append({"start_shifting": out})
        state = next_state

        # After sampling, hold sampled inputs, then apply optional mid changes
        # for the start of the next row.
        carried_reset = reset
        carried_data = data

        if "mid" in row:
            m = row["mid"]
            try:
                carried_reset = m["reset"]
            except:
                pass
            try:
                carried_data = m["data"]
            except:
                pass
            try:
                for mm in m:
                    try:
                        carried_reset = mm["reset"]
                    except:
                        pass
                    try:
                        carried_data = mm["data"]
                    except:
                        pass
            except:
                pass

        if "reset_mid" in row:
            carried_reset = row["reset_mid"]
        if "data_mid" in row:
            carried_data = row["data_mid"]
        if "mid_reset" in row:
            carried_reset = row["mid_reset"]
        if "mid_data" in row:
            carried_data = row["mid_data"]
        if "reset__mid" in row:
            carried_reset = row["reset__mid"]
        if "data__mid" in row:
            carried_data = row["data__mid"]
        if "reset@mid" in row:
            carried_reset = row["reset@mid"]
        if "data@mid" in row:
            carried_data = row["data@mid"]

        for k in row:
            if k == "mid":
                continue
            try:
                kl = k.lower()
            except:
                continue
            if kl in ("reset_mid", "mid_reset", "reset__mid", "reset@mid", "reset-mid"):
                carried_reset = row[k]
            elif kl in ("data_mid", "mid_data", "data__mid", "data@mid", "data-mid"):
                carried_data = row[k]

    return outputs
