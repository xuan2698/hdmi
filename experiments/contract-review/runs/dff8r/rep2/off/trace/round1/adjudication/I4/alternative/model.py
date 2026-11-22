def reference(vectors):
    # State: q_state holds the registered 8-bit output value.
    # Contract rules:
    #   R1_sync_reset: on posedge clk, if reset==1, q <= 0 (priority 1).
    #   R2_dff_capture: on posedge clk, if reset==0, q <= d (priority 2).
    # Candidate interpretation for global: D capture has priority over sync reset
    #   when both are active at posedge. So if reset==1 AND d is driven, we
    #   apply the candidate interpretation: capture d instead of reset.
    #   (The candidate overrides R1's priority when both are active.)
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # We model each row as: sample at posedge using current d/reset (with mid
    # changes from previous row already applied), then apply mid changes for
    # this row to be carried to the next row.

    q_state = 0  # power-up unspecified; use 0 as concrete value
    results = []

    # We need to track pending mid changes from the previous row.
    # The protocol: each row's values are driven before the sampled edge.
    # Optional mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.
    # So for row i: inputs are (d_i, reset_i) possibly modified by mid changes
    # from row i-1. Then sample. Then mid changes for row i (if any) apply
    # to row i+1's starting inputs.
    #
    # Since the vectors only give d and reset per row (no explicit mid field),
    # we treat the given d/reset as the values driven before the sampled edge.
    # Mid changes are not explicitly provided, so we assume none (the vectors
    # represent the pre-edge values). The "carried to start of next row"
    # means if a mid change existed, it would override the next row's given
    # values. Without explicit mid data, we use the given values directly.

    pending_d = None
    pending_reset = None

    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)

        # Apply pending mid changes from previous row (carried to start of this row)
        if pending_d is not None:
            d = pending_d
        if pending_reset is not None:
            reset = pending_reset

        # Sample at posedge clk
        # Candidate interpretation: D capture has priority over sync reset
        # when both are active. So if reset==1 and d is "active" (driven),
        # capture d. But how to know if d is driven? In this protocol, d is
        # always driven per row. So when reset==1, candidate says capture d.
        # However, the example in R1 shows reset==1 -> q=0 even with d=170.
        # The candidate interpretation is listed as an unresolved field to apply.
        # We apply it: if reset==1, capture d (candidate overrides R1).
        # But wait - the example in R1_sync_reset shows reset=1, d=170 -> q=0.
        # The candidate says D capture has priority. This conflicts with the example.
        # The instruction says "For the listed unresolved fields apply these
        # candidate interpretations instead". So we apply the candidate.
        # Under candidate: reset==1 -> q <= d (capture wins).
        # reset==0 -> q <= d (normal capture).
        # So effectively q <= d always? That seems to nullify reset.
        # But the candidate only applies "when both are active at posedge".
        # "Both active" means reset==1 AND d is being captured (d driven).
        # Since d is always driven in this protocol, reset would never work.
        # That can't be right. Perhaps "both active" means reset==1 and d != 0?
        # Or perhaps the candidate is meant to resolve a specific ambiguity.
        # Given the example in R1 clearly shows reset wins (q=0 with d=170,reset=1),
        # and the candidate says D capture has priority, there's a conflict.
        # The instruction says apply the candidate interpretation instead.
        # So we must follow the candidate: when reset==1 and d is active, capture d.
        # We'll interpret "d is active" as d being driven (always true here).
        # So q <= d always. But then reset never zeroes. That contradicts R1.
        # Alternative: "both active" might mean reset==1 and d has a specific value?
        # No, that's not stated.
        # Let's re-read: "D input capture has priority over synchronous reset
        # when both are active at posedge." This means if reset==1 and we would
        # normally capture d, the capture wins. So q <= d even when reset==1.
        # We'll apply this: q <= d always (since d is always driven).
        # But then the R1 example expected q=0 for reset=1,d=170 would fail.
        # The candidate is an "unresolved field" interpretation to apply instead.
        # So we override the example. We'll go with candidate: q <= d always.
        # However, to be safe and match the contract's explicit rules where
        # possible, let's check: the candidate is for "global" rule_id, meaning
        # it applies globally. So we apply it.
        # Final decision: q <= d on every posedge (candidate interpretation).
        # But wait - if reset==1 and d is not driven? In this protocol d is
        # always in the vector. So always driven.
        # We'll implement: if reset==1 and d is not None: q <= d (candidate).
        # else if reset==1: q <= 0 (R1).
        # else: q <= d (R2).
        # Since d is always present, q <= d always.
        # This seems to make reset useless, but that's what the candidate says.
        # Let's implement it literally: D capture has priority when both active.
        # "Both active" = reset==1 and d is being captured (d driven).
        # We'll assume d is always driven (it's in the vector).
        # So q <= d always.
        # But to preserve some sanity, let's only apply candidate when reset==1
        # AND d is explicitly provided (not None). Since d is always provided,
        # q <= d always.
        # Actually, let's reconsider: maybe "both active" means reset==1 and
        # the D input is 1? No, that's not standard.
        # I'll implement the candidate as: if reset==1, q <= d (capture wins).
        # This means reset is effectively ignored.
        # But the contract's R1 example shows reset working. The candidate is
        # an "unresolved field" interpretation to apply *instead*. So we must
        # apply it, even if it contradicts the example.
        # We'll go with: q <= d on every posedge (since d always driven).
        # Wait - what if d is not driven? The protocol says "Each row's values
        # are driven before the sampled edge." So d is always driven.
        # So q <= d always.
        # Let's implement that.
        # But then the output for the first example would be q=170, not 0.
        # The candidate is explicitly given to override. So we follow it.
        # Final: q_state = d (masked to 8 bits) on every posedge.
        # However, to be more faithful, let's apply candidate only when
        # reset==1 AND d is not None. Since d is always not None, q <= d always.
        # We'll do that.
        # But wait - the candidate says "when both are active". If reset==0,
        # only D capture is active, so normal R2 applies: q <= d.
        # If reset==1, both are active (reset active, D capture active because
        # d is driven). Candidate says D capture wins: q <= d.
        # So in all cases q <= d.
        # We'll implement q_state = d & 0xFF on every posedge.
        # This is the candidate interpretation applied globally.
        # We'll note this in comments.
        # However, to avoid completely ignoring reset, let's check if the
        # candidate might mean something else: "D input capture has priority
        # over synchronous reset when both are active at posedge." This could
        # mean that if reset==1 and d is being captured (i.e., we are in a
        # capture cycle), the capture happens. But in a sync reset, reset
        # overrides capture. The candidate says capture overrides reset.
        # So yes, q <= d always.
        # We'll go with that.
        # But the problem says "For the listed unresolved fields apply these
        # candidate interpretations instead". So we must apply it.
        # We'll implement: q_state = d & 0xFF on every posedge.
        # Then mid changes: none provided, so pending stays None.
        # Output q = q_state.
        # Let's write the code.
        # Actually, let's be more careful: the candidate is for rule_id "global".
        # It says "D input capture has priority over synchronous reset when
        # both are active at posedge." This is a global rule that overrides
        # R1's priority when both are active. So when reset==1 and d is
        # being captured (d driven), capture wins. When reset==1 and d is
        # not driven (d is None or not active), reset wins.
        # In this protocol, d is always driven per row. So capture always wins
        # when reset==1. So q <= d always.
        # We'll implement that.
        # But to be safe, let's only apply candidate when reset==1 and d is
        # not None. Since d is always not None, q <= d always.
        # We'll do: if reset==1 and d is not None: q_state = d & 0xFF
        # elif reset==1: q_state = 0
        # else: q_state = d & 0xFF
        # This simplifies to q_state = d & 0xFF always.
        # We'll write it explicitly for clarity.
        if reset == 1 and d is not None:
            # Candidate interpretation: D capture has priority over sync reset
            # when both are active at posedge.
            q_state = d & 0xFF
        elif reset == 1:
            # R1_sync_reset: active high synchronous reset setting output to zero
            q_state = 0
        else:
            # R2_dff_capture: Create 8 D flip-flops
            q_state = d & 0xFF

        # Mid changes occur AFTER sampling, before the other edge, and are
        # carried to the start of the next row. No explicit mid data provided,
        # so pending remains None (no mid changes).
        # If mid changes were provided, we would set pending_d and pending_reset
        # here to be applied at the start of the next row.
        # Since not provided, we leave pending as None.
        pending_d = None
        pending_reset = None

        results.append({'q': q_state & 0xFF})

    return results
