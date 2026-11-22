def reference(vectors):
    # Initial state: reset values (12:00 AM)
    pm = 0
    hh = 0x12
    mm = 0x00
    ss = 0x00

    reset_in = 0
    ena_in = 0

    result = []

    for row in vectors:
        # Drive inputs before sampled edge
        if "reset" in row:
            reset_in = row["reset"]
        if "ena" in row:
            ena_in = row["ena"]

        # reset_priority: sync reset has priority over ena
        if reset_in == 1:
            pm = 0
            hh = 0x12
            mm = 0x00
            ss = 0x00
        else:
            # increment_clock (candidate: ss=0x59 wraps to 0x00 but mm not incremented)
            if ena_in == 1:
                if ss == 0x59:
                    ss = 0x00
                    # mm not incremented per candidate interpretation
                else:
                    low = ss & 0x0F
                    high = ss >> 4
                    if low < 9:
                        low = low + 1
                    else:
                        low = 0
                        high = high + 1
                    ss = (high << 4) | low
                # mm, hh, pm unchanged from ena due to candidate
            else:
                # hold_clock
                pass

        # Output after posedge (next_cycle)
        out = {"pm": pm, "hh": hh, "mm": mm, "ss": ss}
        result.append(out)

        # Apply mid input changes after sampling, carried to next row
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                reset_in = mid["reset"]
            if "ena" in mid:
                ena_in = mid["ena"]

    return result
