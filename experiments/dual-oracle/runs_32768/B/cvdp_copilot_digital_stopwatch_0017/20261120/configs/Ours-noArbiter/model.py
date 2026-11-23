def reference(vectors):
    count = 0
    pulse = 0
    sec = 0
    minute = 0
    hour = 0
    out = []
    for row in vectors:
        reset = int(row.get('reset', 0)) & 1
        start_stop = int(row.get('start_stop', 0)) & 1
        if reset:
            count = 0
            pulse = 0
            sec = 0
            minute = 0
            hour = 0
        out.append({'seconds': sec & 63, 'minutes': minute & 63, 'hour': hour & 1})
        e = row.get('edge', '')
        if isinstance(e, str):
            is_pos = e.lower().startswith('pos')
        else:
            is_pos = (int(e) == 1)
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
