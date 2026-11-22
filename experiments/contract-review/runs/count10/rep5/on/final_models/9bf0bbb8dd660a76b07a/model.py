def reference(vectors):
    # R_RESET / R_COUNT: state q is the current decade count, 0..9.
    q = 0
    current_reset = 0
    out = []
    for row in vectors:
        # Inputs in the row are driven before the sampled posedge.
        if "reset" in row:
            reset = row["reset"]
        else:
            reset = current_reset
        current_reset = reset

        # R_RESET: reset == 1; q_next = 0 (synchronous active-high reset)
        # R_COUNT: reset == 0; q_next = (q + 1) mod 10
        if reset == 1:
            q = 0
        else:
            q = (q + 1) % 10

        out.append({"q": q})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        mid = row.get("mid")
        if mid is not None:
            try:
                current_reset = mid.get("reset", current_reset)
            except:
                current_reset = mid
    return out
