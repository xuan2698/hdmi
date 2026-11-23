def reference(vectors):
    cnt = 0
    pulse = 0
    seconds = 0
    minutes = 0
    hour = 0
    out = []
    toggle = 1
    for row in vectors:
        reset = row.get('reset', 0)
        start_stop = row.get('start_stop', 0)

        if reset:
            cnt = 0
            pulse = 0
            seconds = 0
            minutes = 0
            hour = 0

        clk = row.get('clk', -1)
        if clk == -1:
            edge = row.get('edge', -1)
            if edge == -1:
                posedge = toggle == 1
            elif edge == 'posedge' or edge == 'pos' or edge == 'rising' or edge == 1:
                posedge = 1
            else:
                posedge = 0
        else:
            posedge = clk == 1

        out.append({'seconds': seconds, 'minutes': minutes, 'hour': hour})

        if posedge and not reset:
            old_cnt = cnt
            old_pulse = pulse
            old_seconds = seconds
            old_minutes = minutes
            old_hour = hour

            if start_stop:
                if old_cnt == 3:
                    new_cnt = 0
                    new_pulse = 1
                else:
                    new_cnt = old_cnt + 1
                    new_pulse = 0
            else:
                new_cnt = old_cnt
                new_pulse = 0

            new_seconds = old_seconds
            new_minutes = old_minutes
            new_hour = old_hour

            if old_pulse:
                if old_seconds == 59:
                    new_seconds = 0
                    if old_minutes == 59:
                        new_minutes = 0
                        new_hour = 1
                    else:
                        new_minutes = old_minutes + 1
                else:
                    new_seconds = old_seconds + 1

            cnt = new_cnt
            pulse = new_pulse
            seconds = new_seconds
            minutes = new_minutes
            hour = new_hour

        if toggle == 1:
            toggle = 0
        else:
            toggle = 1

    return out
