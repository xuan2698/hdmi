def reference(vectors):
    sec = 0
    mins = 0
    hour = 0
    div = 0
    pulse = 0
    out = []
    pos_default = True
    for row in vectors:
        if isinstance(row, dict):
            reset = int(row.get('reset', 0)) & 1
            start_stop = int(row.get('start_stop', 0)) & 1
            if 'clk' in row:
                v = row['clk']
                if isinstance(v, str):
                    is_pos = v.lower() in ('posedge', '1', 'true', 'high')
                else:
                    is_pos = int(v) != 0
            elif 'edge' in row:
                v = row['edge']
                if isinstance(v, str):
                    is_pos = v.lower() in ('posedge', '1', 'true', 'high')
                else:
                    is_pos = int(v) != 0
            else:
                is_pos = pos_default
        else:
            reset = 0
            start_stop = 0
            is_pos = pos_default
            if len(row) >= 2:
                reset = int(row[0]) & 1
                start_stop = int(row[1]) & 1
                if len(row) >= 3:
                    v = row[2]
                    if isinstance(v, str):
                        is_pos = v.lower() in ('posedge', '1', 'true', 'high')
                    else:
                        is_pos = int(v) != 0
            elif len(row) == 1:
                reset = int(row[0]) & 1

        if reset:
            sec = 0
            mins = 0
            hour = 0
            div = 0
            pulse = 0

        out.append({'seconds': sec & 63, 'minutes': mins & 63, 'hour': hour & 1})

        if is_pos and not reset:
            old_pulse = pulse
            old_div = div
            if old_div == 3:
                div = 0
                pulse = 1
            else:
                div = old_div + 1
                pulse = 0
            if start_stop and old_pulse:
                if sec == 59:
                    sec = 0
                    if mins == 59:
                        mins = 0
                        hour = 1
                    else:
                        mins += 1
                else:
                    sec = sec + 1

        pos_default = not pos_default

    return out
