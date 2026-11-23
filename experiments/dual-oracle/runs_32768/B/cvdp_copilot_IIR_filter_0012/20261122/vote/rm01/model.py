def reference(vectors):
    def s16(x):
        x = int(x) & 0xFFFF
        return x - 0x10000 if x & 0x8000 else x

    def u16(x):
        x = int(x)
        if x < -32768: x = -32768
        elif x > 32767: x = 32767
        return x & 0xFFFF

    def is_pos(row):
        if 'clk' in row:
            return int(row['clk']) != 0
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                return 'pos' in e.lower()
            return int(e) != 0
        if 'posedge' in row:
            return bool(row['posedge'])
        return None

    y1 = y2 = y3 = 0
    res = []
    first = True
    for row in vectors:
        reset = int(row.get('reset', 0))
        fsel = int(row.get('filter_select', 0)) & 3
        in1 = s16(row.get('in_1', 0))
        in2 = s16(row.get('in_2', 0))
        in3 = s16(row.get('in_3', 0))
        pos = is_pos(row)
        if pos is None:
            pos = first
            first = not first

        if reset:
            y1 = y2 = y3 = 0
            res.append({'out_1': 0, 'out_2': 0, 'out_3': 0})
            continue

        res.append({'out_1': u16(y1), 'out_2': u16(y2), 'out_3': u16(y3)})

        if pos:
            shift = (1, 2, 3, 4)[fsel]
            y1 = y1 + ((in1 - y1) >> shift)
            y2 = y2 + ((in2 - y2) >> shift)
            y3 = y3 + ((in3 - y3) >> shift)
            if y1 < -32768: y1 = -32768
            elif y1 > 32767: y1 = 32767
            if y2 < -32768: y2 = -32768
            elif y2 > 32767: y2 = 32767
            if y3 < -32768: y3 = -32768
            elif y3 > 32767: y3 = 32767

    return res
