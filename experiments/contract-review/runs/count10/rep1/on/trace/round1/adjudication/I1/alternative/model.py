def reference(vectors):
    # Rule global: Power-up q initialized to 0; first sampled reset=0 posedge yields q=1.
    q = 0
    reset_state = 0
    result = []
    for row in vectors:
        # Inputs are driven before the sampled edge; explicit row value overrides carried mid change.
        if "reset" in row:
            reset_state = row["reset"]
        # Rule sync_reset_to_zero: synchronous active-high reset at sampled posedge sets q to 0.
        if reset_state == 1:
            q = 0
        else:
            # Rule count_modulo_10: if reset == 0, q increments modulo 10.
            q = (q + 1) % 10
        result.append({"q": q})
        # Optional mid input changes occur after sampling and carry to start of next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    reset_state = mid["reset"]
    return result
