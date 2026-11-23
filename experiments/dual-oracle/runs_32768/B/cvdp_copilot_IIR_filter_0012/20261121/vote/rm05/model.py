def reference(vectors):
    state = [0, 0, 0]
    outputs = []
    for idx, row in enumerate(vectors):
        reset = row.get('reset', 0) & 1
        if 'clk' in row:
            is_posedge = (row['clk'] & 1) == 1
        elif 'edge' in row:
            edge = row['edge']
            is_posedge = (edge.lower() == 'posedge') if isinstance(edge, str) else bool(edge)
        else:
            is_posedge = (idx % 2 == 0)
        if reset:
            state = [0, 0, 0]
        out_vals = [y & 0xFFFF for y in state]
        outputs.append({'out_1': out_vals[0], 'out_2': out_vals[1], 'out_3': out_vals[2]})
        if is_posedge and not reset:
            k = row.get('filter_select', 0) & 3
            new_state = []
            for i in range(1, 4):
                x_raw = row.get(f'in_{i}', 0) & 0xFFFF
                x = x_raw - 65536 if x_raw >= 32768 else x_raw
                y = state[i - 1]
                if k == 0:
                    ny = x
                else:
                    ny = y + ((x - y) >> k)
                if ny > 32767:
                    ny = 32767
                elif ny < -32768:
                    ny = -32768
                new_state.append(ny)
            state = new_state
    return outputs
