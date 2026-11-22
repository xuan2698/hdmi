def reference(vectors):
    # State: q_state holds the 8-bit registered output.
    q_state = 0  # power-up unspecified; use 0 as concrete value

    results = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)

        # R1: active high synchronous reset -> q becomes 0 at posedge
        # R2: otherwise q captures d at posedge
        if reset == 1:
            q_state = 0
        else:
            q_state = d & 0xFF

        results.append({'q': q_state & 0xFF})

    return results
