def reference(vectors):
    y1 = y2 = y3 = 0
    result = []
    for i, row in enumerate(vectors):
        edge = row.get('edge', None)
        if edge is None:
            is_posedge = (i % 2 == 0)
        elif isinstance(edge, str):
            is_posedge = (edge.lower() == 'posedge' or edge == '1')
        else:
            is_posedge = bool(edge)

        rst = row.get('reset', 0) & 1
        in1 = row.get('in_1', 0) & 0xFFFF
        in2 = row.get('in_2', 0) & 0xFFFF
        in3 = row.get('in_3', 0) & 0xFFFF
        sel = row.get('filter_select', 0) & 3

        if in1 >= 0x8000: in1 -= 0x10000
        if in2 >= 0x8000: in2 -= 0x10000
        if in3 >= 0x8000: in3 -= 0x10000

        if rst:
            y1 = y2 = y3 = 0
            out1 = out2 = out3 = 0
        else:
            out1 = y1 & 0xFFFF
            out2 = y2 & 0xFFFF
            out3 = y3 & 0xFFFF
            if is_posedge:
                y1 = y1 + ((in1 - y1) >> sel)
                y2 = y2 + ((in2 - y2) >> sel)
                y3 = y3 + ((in3 - y3) >> sel)

        result.append({'out_1': out1, 'out_2': out2, 'out_3': out3})
    return result
