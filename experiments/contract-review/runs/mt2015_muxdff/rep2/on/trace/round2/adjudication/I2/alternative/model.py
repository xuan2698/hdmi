def reference(vectors):
    # Contract: reset kind none; use concrete 0 for unspecified power-up state.
    Q_reg = 0
    outputs = []

    for vec in vectors:
        L = int(vec.get("L", 0)) & 1
        q_in = int(vec.get("q_in", 0)) & 1
        r_in = int(vec.get("r_in", 0)) & 1

        if L == 1:
            # Rule load_L_high priority 1: Q_next = r_in
            Q_next = r_in
        else:
            # Rule feedback_L_low priority 2, candidate interpretation:
            # Q_next = q_in ^ Q when L=0
            Q_next = (q_in ^ Q_reg) & 1

        Q_reg = Q_next & 1
        outputs.append({"Q": Q_reg})

    return outputs
