def reference(vectors):
    sec = 0
    minute = 0
    hour = 0
    div = 0
    out = []
    CLK_FREQ = 4

    for row in vectors:
        reset = row.get('reset', 0)
        if reset:
            sec = 0
            minute = 0
            hour = 0
            div = 0

        out.append({
            'seconds': sec & 0x3F,
            'minutes': minute & 0x3F,
            'hour': hour & 1
        })

        edge = row.get('edge', row.get('clk', 0))
        if isinstance(edge, str):
            s = edge.lower()
            is_pos = s.startswith('pos') or s == 'p' or s == '1'
        else:
            is_pos = bool(edge)

        if is_pos and not reset:
            start_stop = row.get('start_stop', 0)
            if start_stop:
                if div == CLK_FREQ - 1:
                    div = 0
                    if sec == 59:
                        sec = 0
                        if minute == 59:
                            minute = 0
                            hour = (hour + 1) & 1
                        else:
                            minute += 1
                    else:
                        sec += 1
                else:
                    div += 1
    return out
