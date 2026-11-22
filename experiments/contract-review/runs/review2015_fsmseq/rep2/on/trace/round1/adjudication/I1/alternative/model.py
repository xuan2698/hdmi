def reference(vectors):
    # State encodings
    S0, S1, S2, S3, SF = 0, 1, 2, 3, 4

    # Power-up assumed initial/reset state: S0 and start_shifting = 0
    state = S0
    start_shifting = 0

    # Current input values (persist across rows unless changed)
    reset = 0
    data = 0

    outputs = []

    for row in vectors:
        # Drive row inputs before the sampled posedge
        if 'reset' in row:
            reset = row['reset'] & 1
        if 'data' in row:
            data = row['data'] & 1

        # Sampled posedge: compute next state and next start_shifting
        if reset:
            # R_RESET: reset == 1 at sampled posedge overrides all; state <= S0, start_shifting <= 0
            next_state = S0
            next_start_shifting = 0
        else:
            if state == SF:
                # R_HOLD: current state == SF; next state <= SF, start_shifting <= 1
                next_state = SF
                next_start_shifting = 1
            elif state == S3 and data == 1:
                # R_DETECT: current state == S3 and data == 1; next state <= SF
                # Candidate interpretation: registered output, start_shifting becomes 1 one cycle after detection posedge
                next_state = SF
                next_start_shifting = 0
            else:
                # R_PROGRESS: state in {S0,S1,S2,S3} and not (S3 and data==1)
                # Explicit transition table
                if state == S0:
                    next_state = S1 if data == 1 else S0
                elif state == S1:
                    next_state = S2 if data == 1 else S0
                elif state == S2:
                    next_state = S3 if data == 0 else S2
                elif state == S3:
                    # data must be 0 here (S3+1 handled by R_DETECT)
                    next_state = S0
                else:
                    next_state = S0
                next_start_shifting = 0

        # Update registers after posedge settled
        state = next_state
        start_shifting = next_start_shifting

        # Record output for this row (after sampled posedge)
        outputs.append({'start_shifting': start_shifting})

        # Apply optional mid-cycle changes after sampling; they persist to next row
        if 'mid' in row:
            mid = row['mid']
            if 'reset' in mid:
                reset = mid['reset'] & 1
            if 'data' in mid:
                data = mid['data'] & 1

    return outputs
