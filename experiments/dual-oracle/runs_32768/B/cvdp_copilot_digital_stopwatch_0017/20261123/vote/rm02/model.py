def reference(vectors):
    seconds = 0
    minutes = 0
    hour = 0
    counter = 0
    pulse = 0
    out = []
    for row in vectors:
        r = row["reset"]
        s = row["start_stop"]
        e = row["edge"]
        if r == 1 or r == "1":
            seconds = 0
            minutes = 0
            hour = 0
            counter = 0
            pulse = 0
        is_pos = (e == 1 or e == True or e == "posedge" or e == "pos" or e == "1")
        out.append({"seconds": seconds, "minutes": minutes, "hour": hour})
        running = (s == 1 or s == "1" or s == True)
        if is_pos and not (r == 1 or r == "1"):
            old_pulse = pulse
            if running:
                if counter == 3:
                    counter_new = 0
                    pulse_new = 1
                else:
                    counter_new = counter + 1
                    pulse_new = 0
            else:
                counter_new = counter
                pulse_new = 0
            if old_pulse == 1:
                if seconds == 59:
                    seconds = 0
                    if minutes == 59:
                        minutes = 0
                        hour = 1 - hour
                    else:
                        minutes = minutes + 1
                else:
                    seconds = seconds + 1
            counter = counter_new
            pulse = pulse_new
    return out
