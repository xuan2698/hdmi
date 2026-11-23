def reference(vectors):
    y1 = y2 = y3 = 0
    outputs = []
    for row in vectors:
        rst = row.get('reset', 0)
        if rst == 1:
            y1 = y2 = y3 = 0

        if 'edge' in row:
            ev = row['edge']
            if ev == 'posedge' or ev == 1 or ev is True:
                edge = 'posedge'
            else:
                edge = 'negedge'
        elif 'clk' in row:
            edge = 'posedge' if row['clk'] == 1 else 'negedge'
        else:
            edge = 'posedge' if len(outputs) % 2 == 0 else 'negedge'

        outputs.append({
            'out_1': y1 & 0xFFFF,
            'out_2': y2 & 0xFFFF,
            'out_3': y3 & 0xFFFF
        })

        if edge == 'posedge' and rst == 0:
            in1 = row.get('in_1', 0)
            in2 = row.get('in_2', 0)
            in3 = row.get('in_3', 0)
            if in1 >= 32768: in1 -= 65536
            if in2 >= 32768: in2 -= 65536
            if in3 >= 32768: in3 -= 65536
            fs = row.get('filter_select', 0)
            shift = fs

            n1 = y1 + ((in1 - y1) >> shift)
            n2 = y2 + ((in2 - y2) >> shift)
            n3 = y3 + ((in3 - y3) >> shift)

            if n1 < -32768: n1 = -32768
            elif n1 > 32767: n1 = 32767
            if n2 < -32768: n2 = -32768
            elif n2 > 32767: n2 = 32767
            if n3 < -32768: n3 = -32768
            elif n3 > 32767: n3 = 32767

            y1, y2, y3 = n1, n2, n3

    return outputs
