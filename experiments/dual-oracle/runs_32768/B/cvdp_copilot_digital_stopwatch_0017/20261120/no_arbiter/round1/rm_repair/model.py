def reference(vectors):
    count = 0
    pulse = 0
    sec = 0
    minute = 0
    hour = 0
    out = []
    prev_clk = 0

    for i, row in enumerate(vectors):
        reset = 1 if row.get('reset', 0) else 0
        start_stop = 1 if row.get('start_stop', 0) else 0

        if reset:
            count = 0
            pulse = 0
            sec = 0
            minute = 0
            hour = 0

        out.append({
            'seconds': sec & 63,
            'minutes': minute & 63,
            'hour': hour & 1
        })

        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = e.lower().startswith('pos')
            else:
                is_pos = (int(e) == 1)
        elif 'clk' in row:
            c = int(row['clk'])
            is_pos = (prev_clk == 0 and c == 1)
            prev_clk = c
        else:
            is_pos = (i % 2 == 0)

        if is_pos and not reset:
            if count == 3:
                new_count = 0
                new_pulse = 1
            else:
                new_count = count + 1
                new_pulse = 0

            if start_stop and pulse:
                if sec == 59:
                    sec = 0
                    if minute == 59:
                        minute = 0
                        hour = (hour + 1) & 1
                    else:
                        minute = (minute + 1) & 63
                else:
                    sec = (sec + 1) & 63

            count = new_count
            pulse = new_pulse

    return out
