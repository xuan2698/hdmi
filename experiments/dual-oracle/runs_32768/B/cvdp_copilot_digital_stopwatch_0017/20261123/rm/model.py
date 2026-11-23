def reference(vectors):
    seconds = minutes = hour = div = 0
    result = []
    last_ss = 0
    last_reset = 0

    for i, row in enumerate(vectors):
        def get(key):
            if isinstance(row, dict):
                if key in row:
                    return row[key]
                if 'inputs' in row and isinstance(row['inputs'], dict) and key in row['inputs']:
                    return row['inputs'][key]
            return None

        edge = get('edge')
        if edge is None:
            edge = get('clk')
        if edge is None:
            edge = 1 if i % 2 == 0 else 0

        if isinstance(edge, str):
            e = edge.lower()
            posedge = e.startswith('pos') or e in ('1', 'true', 'rising')
        else:
            posedge = bool(edge)

        reset_value = get('reset')
        if reset_value is None:
            reset = last_reset
        else:
            reset = int(reset_value)
            last_reset = reset

        start_value = get('start_stop')
        if start_value is None:
            start_stop = last_ss
        else:
            start_stop = int(start_value)
            last_ss = start_stop

        if reset:
            seconds = minutes = hour = div = 0

        result.append({'seconds': seconds, 'minutes': minutes, 'hour': hour})

        if posedge:
            if reset:
                seconds = minutes = hour = div = 0
            elif start_stop:
                if div == 3:
                    div = 0
                    if seconds == 59:
                        seconds = 0
                        if minutes == 59:
                            minutes = 0
                            hour = 1
                        else:
                            minutes += 1
                    else:
                        seconds += 1
                else:
                    div += 1

    return result
