def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # State: COUNT (0..9). Initial value is unspecified; we use 0 as a concrete
    # power-up value (allowed since power-up is unspecified, but must be concrete).
    # R1: reset == 1 on posedge -> q = 0 (synchronous, same_cycle, priority 1)
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1
    # R3: reset == 0 && q == 9 on posedge -> q = 0
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Each row's inputs are driven before the sampled posedge.

    count = 0  # concrete initial state (unspecified at power-up)
    out = []

    for row in vectors:
        # Inputs for this row are driven before the sampled posedge.
        reset = row.get("reset", 0)

        # Sample on posedge: compute next state per rules (R1 > R2/R3).
        if reset == 1:
            # R1: synchronous active-high reset
            count = 0
        else:
            if count < 9:
                # R2: increment
                count = count + 1
            else:
                # R3: wrap from 9 to 0
                count = 0

        # Output visible same_cycle after posedge settles.
        out.append({"q": count & 0xF})

        # Mid changes (if any) occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. Since we read inputs
        # fresh at the start of each row, mid changes are naturally applied
        # to the next row's inputs. No state change here.

    return out
