def reference(vectors):
    q = 0  # initial concrete state (power-up unspecified resolved to 0)
    current_a = 0
    outputs = []
    for vec in vectors:
        # Apply inputs driven before the sampled (posedge) edge
        if 'a' in vec:
            current_a = vec['a']
        # posedge update
        if current_a == 1:
            # q_load4_when_a_high
            q = 4
        else:
            # q_increment_mod7_when_a_low
            q = (q + 1) % 7
        outputs.append({'q': q})
        # Process mid-cycle changes after sampling, carried to next row
        if 'mid' in vec:
            mid = vec['mid']
            if 'a' in mid:
                current_a = mid['a']
    return outputs
