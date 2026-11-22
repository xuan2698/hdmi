def reference(vectors):
    # Initial state: use reset value as concrete power-up default
    pm = 0
    hh = 0x12
    mm = 0x00
    ss = 0x00

    cur_inputs = {'reset': 0, 'ena': 0}
    results = []

    for row in vectors:
        # Drive row inputs before the sampled posedge (exclude mid)
        for k in row:
            if k != 'mid':
                cur_inputs[k] = row[k]

        reset = cur_inputs.get('reset', 0)
        ena = cur_inputs.get('ena', 0)

        # Rule reset_priority: synchronous reset has highest priority
        if reset == 1:
            pm = 0
            hh = 0x12
            mm = 0x00
            ss = 0x00

        # Rule increment_clock: advance one displayed second
        elif ena == 1:
            # Increment seconds
            if ss == 0x59:
                ss = 0x00

                # Carry to minutes
                if mm == 0x59:
                    mm = 0x00

                    # Carry to hours
                    if hh == 0x12:
                        hh = 0x01
                        # Alternative interpretation: toggle pm on hh 12->01
                        pm = 1 - pm
                    elif hh == 0x11:
                        hh = 0x12
                        # No pm toggle on hh 11->12 under alternative rule
                    else:
                        # BCD increment hours
                        if (hh & 0x0F) == 0x09:
                            hh = (hh & 0xF0) + 0x10
                        else:
                            hh = hh + 1
                else:
                    # BCD increment minutes
                    if (mm & 0x0F) == 0x09:
                        mm = (mm & 0xF0) + 0x10
                    else:
                        mm = mm + 1
            else:
                # BCD increment seconds
                if (ss & 0x0F) == 0x09:
                    ss = (ss & 0xF0) + 0x10
                else:
                    ss = ss + 1

        # Rule hold_clock: reset == 0 && ena == 0; state is unchanged

        # Output state after posedge has settled
        results.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})

        # Optional mid input changes occur after sampling, before next edge
        if 'mid' in row:
            mid = row['mid']
            for k in mid:
                cur_inputs[k] = mid[k]

    return results
