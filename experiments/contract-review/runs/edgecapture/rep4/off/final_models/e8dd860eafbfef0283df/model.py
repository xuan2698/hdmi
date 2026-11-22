def reference(vectors):
    # R1_reset_clear: synchronous active-high reset clears out_reg.
    # R2_capture_falling: set sticky bit when in bit goes 1->0 (registered, visible next cycle).
    # R3_hold: sticky bits remain 1 until reset.
    # State: out_reg (32-bit sticky), in_prev (32-bit previous input), initialized flag.
    out_reg = 0
    in_prev = 0
    initialized = False
    results = []
    for row in vectors:
        reset = row.get("reset", 0) & 1
        cur_in = row.get("in", 0) & 0xFFFFFFFF
        # Sample at posedge: compute next state based on current inputs and prior state.
        if reset == 1:
            # R1_reset_clear
            next_out = 0
            next_prev = cur_in
            initialized = True
        else:
            if not initialized:
                # First cycle after reset release: initialize in_prev to current in
                # to avoid spurious capture.
                next_out = out_reg
                next_prev = cur_in
                initialized = True
            else:
                # R2_capture_falling: detect 1->0 transitions
                falling = (~cur_in) & in_prev & 0xFFFFFFFF
                # R3_hold: OR in new captures (idempotent)
                next_out = (out_reg | falling) & 0xFFFFFFFF
                next_prev = cur_in
        # Output visible this cycle is the registered value (next_cycle visibility).
        results.append({"out": next_out & 0xFFFFFFFF})
        out_reg = next_out
        in_prev = next_prev
    return results
