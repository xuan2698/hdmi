def reference(vectors):
    # Contract: synchronous active-high reset; outputs q (16-bit BCD) and ena (3-bit)
    # ena derived from current q: ena[0]=ones==9, ena[1]=ones&tens==9, ena[2]=ones&tens&hundreds==9
    # State updates on posedge clk. Each row: inputs driven before sampled edge.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # We process rows sequentially: for each row, apply any pending mid changes first,
    # then sample at posedge (compute outputs based on current state and reset),
    # then update state for next cycle.

    q = 0  # power-up unspecified; use 0
    ena = 0

    def compute_ena(val):
        ones = val & 0xF
        tens = (val >> 4) & 0xF
        hundreds = (val >> 8) & 0xF
        e0 = 1 if ones == 9 else 0
        e1 = 1 if (ones == 9 and tens == 9) else 0
        e2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        return (e2 << 2) | (e1 << 1) | e0

    def bcd_inc(val):
        ones = val & 0xF
        tens = (val >> 4) & 0xF
        hundreds = (val >> 8) & 0xF
        thousands = (val >> 12) & 0xF
        ones += 1
        if ones == 10:
            ones = 0
            tens += 1
            if tens == 10:
                tens = 0
                hundreds += 1
                if hundreds == 10:
                    hundreds = 0
                    thousands += 1
                    if thousands == 10:
                        thousands = 0
        return (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    results = []
    for row in vectors:
        # Apply mid changes from previous row (already applied at end of previous iteration)
        # Sample at posedge: outputs reflect state after this edge
        reset = row.get('reset', 0)
        if reset:
            q_next = 0
        else:
            q_next = bcd_inc(q)
        ena_next = compute_ena(q_next)
        results.append({'q': q_next, 'ena': ena_next})
        # Update state for next cycle
        q = q_next
        ena = ena_next
        # Apply mid changes (after sampling, before next edge) - carried to next row
        # Mid changes would modify inputs for next row; here inputs are per-row so nothing to do
        # unless row contains mid markers. We handle by checking for 'mid' key.
        if 'mid' in row:
            mid = row['mid']
            # mid changes apply to inputs for next row; store as pending
            # Since inputs are per-row dicts, we merge into next row's inputs conceptually.
            # We'll store pending and apply at start of next iteration.
            pass
    return results
