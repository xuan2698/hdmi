def reference(vectors):
    # Q_posedge_update: At each posedge of clk, after settlement, Q becomes r_in when L=1.
    # Candidate interpretation: L=0 holds Q (q_in is current-state feedback, not external data).
    q = 0  # initial state Q0 (power-up unspecified, default to 0)
    carried = {}  # input values carried from previous mid changes
    out = []
    for row in vectors:
        # Determine inputs at this posedge; explicit row values override carried mid changes.
        L = row['L'] if 'L' in row else carried.get('L', 0)
        r_in = row['r_in'] if 'r_in' in row else carried.get('r_in', 0)
        # q_in is ignored per candidate interpretation.
        # Apply posedge update.
        if L == 1:
            q = r_in & 1
        # else: L=0 holds Q (candidate interpretation).
        out.append({'Q': q & 1})
        # After posedge, update carried with the row's driven inputs (they persist until changed).
        if 'L' in row:
            carried['L'] = row['L']
        if 'r_in' in row:
            carried['r_in'] = row['r_in']
        if 'q_in' in row:
            carried['q_in'] = row['q_in']
        # Apply optional mid input changes (after sampling, before next edge).
        if 'mid' in row:
            mid = row['mid']
            for k in mid:
                carried[k] = mid[k]
        # Also handle keys like 'L_mid', 'r_in_mid', etc.
        for k in row:
            if len(k) > 4 and k[-4:] == '_mid':
                base = k[:-4]
                carried[base] = row[k]
    return out
