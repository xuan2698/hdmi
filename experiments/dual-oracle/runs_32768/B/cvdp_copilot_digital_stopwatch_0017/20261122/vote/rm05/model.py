def reference(vectors):
    CLK_FREQ = 4
    sec = 0
    minute = 0
    hour = 0
    div = 0
    out = []
    for i, row in enumerate(vectors):
        out.append({'seconds': sec, 'minutes': minute, 'hour': hour})
        rst = int(row.get('reset', 0))
        ss = int(row.get('start_stop', 0))
        if 'edge' in row:
            edge = row['edge']
            if isinstance(edge, str):
                is_pos = edge.lower().startswith('p')
            else:
                is_pos = bool(edge)
        else:
            is_pos = (i % 2 == 0)
        if is_pos:
            if rst:
                sec = 0
                minute = 0
                hour = 0
                div = 0
            else:
                pulse = (div == CLK_FREQ - 1)
                if pulse:
                    div = 0
                else:
                    div += 1
                if ss and pulse:
                    if sec == 59:
                        sec = 0
                        if minute == 59:
                            minute = 0
                            hour = 1
                        else:
                            minute += 1
                    else:
                        sec += 1
        else:
            if rst:
                sec = 0
                minute = 0
                hour = 0
                div = 0
    return out
