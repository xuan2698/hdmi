def reference(vectors):
    def get_val(row, names, default, pos):
        if isinstance(row, dict):
            for n in names:
                if n in row:
                    return int(row[n]) & 1
            return default
        if isinstance(row, (list, tuple)):
            if len(row) >= 3:
                if isinstance(row[0], str):
                    if len(row) > pos + 1:
                        return int(row[pos + 1]) & 1
                else:
                    return int(row[pos + 1]) & 1
            elif len(row) > pos:
                return int(row[pos]) & 1
            return default
        return default

    def get_edge(row, idx):
        if isinstance(row, dict):
            for k in ('edge', 'clk', 'clock'):
                if k in row:
                    v = row[k]
                    if isinstance(v, str):
                        s = v.lower()
                        if 'pos' in s:
                            return 1
                        if 'neg' in s:
                            return 0
                    return 1 if v else 0
        elif isinstance(row, (list, tuple)):
            for v in row:
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s:
                        return 1
                    if 'neg' in s:
                        return 0
            if len(row) >= 3 and not isinstance(row[0], str):
                v = row[0]
                if v in (0, 1, False, True):
                    return 1 if v else 0
        return 1 if (idx % 2 == 0) else 0

    count = 0
    pulse = 0
    seconds = 0
    minutes = 0
    hour = 0
    out = []

    for idx, row in enumerate(vectors):
        rst = get_val(row, ('reset', 'rst'), 0, 0)
        start = get_val(row, ('start_stop', 'startstop', 'start'), 0, 1)
        edge = get_edge(row, idx)

        if rst:
            count = 0
            pulse = 0
            seconds = 0
            minutes = 0
            hour = 0

        out.append({'seconds': seconds, 'minutes': minutes, 'hour': hour})

        if edge:
            if rst:
                count = 0
                pulse = 0
                seconds = 0
                minutes = 0
                hour = 0
            else:
                n_count = 0 if count == 3 else count + 1
                n_pulse = 1 if count == 3 else 0
                n_seconds = seconds
                n_minutes = minutes
                n_hour = hour

                if pulse == 1 and start == 1:
                    if seconds == 59:
                        n_seconds = 0
                        if minutes == 59:
                            n_minutes = 0
                            n_hour = 1
                        else:
                            n_minutes = minutes + 1
                    else:
                        n_seconds = seconds + 1

                count = n_count
                pulse = n_pulse
                seconds = n_seconds
                minutes = n_minutes
                hour = n_hour

    return out
