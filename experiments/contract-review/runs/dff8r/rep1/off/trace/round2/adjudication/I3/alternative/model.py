def reference(vectors):
    # State: q_state holds the registered 8-bit output value.
    # Initial value before first posedge is unspecified; we use 0 as a concrete
    # placeholder (allowed since power-up is unspecified).
    q_state = 0

    # Candidate interpretation for global unresolved field:
    # "Reset is sampled at posedge but output zeroing occurs on the following
    # posedge (one-cycle delayed reset visibility)."
    # We track a pending_reset flag that was sampled at the previous posedge.
    pending_reset = 0

    results = []

    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # --- posedge clk sampling ---
        # R1_sync_reset: active high synchronous reset setting output to zero.
        # Under the candidate interpretation, reset sampled now takes effect
        # on the NEXT posedge. So we apply the previously-sampled pending_reset.
        if pending_reset == 1:
            # R1_sync_reset (delayed visibility per candidate interpretation)
            q_state = 0
        else:
            # R2_dff_capture: capture d on posedge when reset not active
            q_state = d

        # Sample current reset for next cycle (delayed visibility)
        pending_reset = reset

        # Output visible same cycle after posedge settles
        results.append({'q': q_state & 0xFF})

        # mid changes occur AFTER sampling, before other edge, carried to next row.
        # Since we read inputs at the start of each row, mid changes are already
        # reflected in the next row's inputs. No action needed here.

    return results
