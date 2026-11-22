def reference(vectors):
    # Persistent input state carried from optional mid changes after sampling.
    d_state = 0
    reset_state = 0
    outputs = []

    for row in vectors:
        # Each row's explicit inputs are driven before the sampled negedge.
        if "d" in row:
            d_state = row["d"]
        if "reset" in row:
            reset_state = row["reset"]

        # sync_reset_high: reset == 1 on negedge sets q to 0x34 and has priority.
        # negedge_d_update: reset == 0 on negedge makes q capture d.
        if reset_state:
            q_next = 52  # 0x34
        else:
            q_next = d_state

        # Return concrete unsigned 8-bit output after the negedge has settled.
        outputs.append({"q": q_next & 0xFF})

        # Mid changes happen AFTER sampling and are carried to the next row start.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                if "d" in mid:
                    d_state = mid["d"]
                if "reset" in mid:
                    reset_state = mid["reset"]

    return outputs
