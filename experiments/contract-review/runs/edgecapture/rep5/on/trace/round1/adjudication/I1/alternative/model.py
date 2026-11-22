def reference(vectors):
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    mask = 4294967295
    result = []

    for row in vectors:
        if "reset" in row:
            cur_reset = row["reset"] & 1
        if "in" in row:
            cur_in = row["in"] & mask

        # synchronous_active_high_reset: reset == 1 at the posedge clears out.
        if cur_reset == 1:
            out = 0
            # global candidate interpretation: reset clears/suppresses prev_in history.
            prev_in = 0
        else:
            # falling_edge_capture_and_hold: sticky capture of 1-to-0 per bit.
            out = out | (prev_in & (cur_in ^ mask))
            prev_in = cur_in & mask

        result.append({"out": out & mask})

        # Optional mid changes occur after sampling and carry to the next row.
        if "mid" in row:
            mid = row["mid"]
            try:
                for key, value in mid.items():
                    if key == "reset":
                        cur_reset = value & 1
                    elif key == "in":
                        cur_in = value & mask
            except AttributeError:
                pass
        if "mid_reset" in row:
            cur_reset = row["mid_reset"] & 1
        if "mid_in" in row:
            cur_in = row["mid_in"] & mask

    return result
