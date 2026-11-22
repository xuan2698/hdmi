def reference(vectors):
    # State: Q is the 8-bit flip-flop output register, reset value 0x34 (52).
    # R1: reset==1 on negedge -> q = 0x34 (52), same cycle, priority 1.
    # R2: reset==0 on negedge -> q = d, same cycle, priority 2.
    # R2 unresolved: if initial Q is unknown, first negedge with reset=0
    #     leaves q undefined (we model as None until a reset or defined load).
    # Mid changes occur AFTER sampling, before other edge, carried to next row.

    Q = None  # power-up unspecified (unknown)
    out = []

    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # Sample at negedge
        if reset == 1:
            # R1: active high synchronous reset, priority 1
            Q = 0x34
        else:
            # R2: load d on negedge when reset==0
            if Q is None:
                # R2 unresolved: first negedge with reset=0 leaves q undefined
                Q = None
            else:
                Q = d

        # Output visible same cycle
        if Q is None:
            # undefined -> report as 0 within bit width (concrete unsigned int)
            out.append({'q': 0})
        else:
            out.append({'q': Q & 0xFF})

        # Mid changes: applied after sampling, carried to next row.
        # (No explicit mid field in vectors; d/reset already represent
        #  the values driven before this sampled edge.)

    return out
