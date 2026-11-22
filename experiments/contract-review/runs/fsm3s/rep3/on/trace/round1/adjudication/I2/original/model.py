def reference(vectors):
    # Start in state A (concrete choice for unspecified power-up)
    state = "A"
    cur_in = 0
    cur_reset = 0
    result = []
    for row in vectors:
        # Drive row's explicit inputs before the sampled posedge
        if "in" in row:
            cur_in = row["in"]
        if "reset" in row:
            cur_reset = row["reset"]

        # R_RESET: synchronous active high reset at posedge clk; priority 100
        if cur_reset == 1:
            state = "A"
        else:
            # State transition logic per table
            if state == "A":
                if cur_in == 0:
                    state = "A"
                else:
                    state = "B"
            elif state == "B":
                if cur_in == 0:
                    state = "C"
                else:
                    state = "B"
            elif state == "C":
                if cur_in == 0:
                    state = "A"
                else:
                    state = "D"
            elif state == "D":
                if cur_in == 0:
                    state = "C"
                else:
                    state = "B"

        # Moore output based on state after posedge settles
        # R_OUT_A: state A -> out 0
        # R_OUT_B: state B -> out 0
        # R_OUT_C: state C -> out 0
        # R_OUT_D: state D -> out 1
        if state == "A" or state == "B" or state == "C":
            out = 0
        else:  # state == "D"
            out = 1
        result.append({"out": out})

        # Process optional mid input changes AFTER sampling, before other edge
        # These are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            for k, v in mid.items():
                if k == "in":
                    cur_in = v
                elif k == "reset":
                    cur_reset = v
        if "mid_in" in row:
            cur_in = row["mid_in"]
        if "mid_reset" in row:
            cur_reset = row["mid_reset"]
        if "in_mid" in row:
            cur_in = row["in_mid"]
        if "reset_mid" in row:
            cur_reset = row["reset_mid"]

    return result
