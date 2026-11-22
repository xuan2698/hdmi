def reference(vectors):
    # Initialize state q. Power-up is unspecified; choose 0 as a concrete initial state.
    state_q = 0
    # Current input values maintained across cycles for mid-cycle changes.
    current_inputs = {'a': 0}
    outputs = []

    for v in vectors:
        # Apply inputs driven before the sampled posedge.
        # Skip mid-change descriptors, which are applied after sampling.
        for k, val in v.items():
            if k == 'mid':
                continue
            if k.startswith('mid_') or k.endswith('_mid'):
                continue
            current_inputs[k] = val

        # Determine input a for this posedge (1-bit).
        a = current_inputs.get('a', 0) & 1

        # Explicit next-state transition at posedge clk.
        if a == 1:
            # rule q_load4_when_a_high
            next_q = 4
        else:
            # rule q_increment_mod7_when_a_low
            next_q = (state_q + 1) % 7

        state_q = next_q
        # Output q after posedge has settled (3-bit width).
        outputs.append({'q': state_q & 7})

        # Apply mid-cycle input changes after sampling, carried to next row.
        if 'mid' in v:
            mid = v['mid']
            if isinstance(mid, dict):
                for k, val in mid.items():
                    current_inputs[k] = val
            else:
                # Fallback: treat non-dict mid as a change to the single input 'a'.
                current_inputs['a'] = mid

        for k, val in v.items():
            if k.startswith('mid_'):
                input_name = k[4:]
                current_inputs[input_name] = val
            elif k.endswith('_mid'):
                input_name = k[:-4]
                current_inputs[input_name] = val

    return outputs
