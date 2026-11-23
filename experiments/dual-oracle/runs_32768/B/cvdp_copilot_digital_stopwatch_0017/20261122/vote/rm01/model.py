def reference(vectors):
    count = 0
    one_sec_pulse = 0
    seconds = 0
    minutes = 0
    hour = 0
    res = []
    for v in vectors:
        res.append({'seconds': seconds, 'minutes': minutes, 'hour': hour})
        if v.get('reset', 0) == 1:
            count = 0
            one_sec_pulse = 0
            seconds = 0
            minutes = 0
            hour = 0
            continue
        edge = v.get('edge')
        if isinstance(edge, str):
            is_pos = (edge == 'posedge')
        else:
            is_pos = (edge == 1)
        if is_pos:
            start_stop = v.get('start_stop', 0)
            if start_stop == 1:
                if count == 3:
                    new_count = 0
                    new_pulse = 1
                else:
                    new_count = count + 1
                    new_pulse = 0
            else:
                new_count = count
                new_pulse = 0
            if one_sec_pulse == 1:
                if seconds == 59:
                    new_seconds = 0
                    if minutes == 59:
                        new_minutes = 0
                        new_hour = 1 - hour
                    else:
                        new_minutes = minutes + 1
                        new_hour = hour
                else:
                    new_seconds = seconds + 1
                    new_minutes = minutes
                    new_hour = hour
            else:
                new_seconds = seconds
                new_minutes = minutes
                new_hour = hour
            count = new_count
            one_sec_pulse = new_pulse
            seconds = new_seconds
            minutes = new_minutes
            hour = new_hour
    return res
