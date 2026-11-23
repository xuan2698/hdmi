def reference(vectors):
    seconds = 0
    minutes = 0
    hour = 0
    divider = 0
    out = []
    for i, row in enumerate(vectors):
        reset = 0
        start_stop = 0
        edge = None
        if isinstance(row, dict):
            reset = int(row.get('reset', 0))
            start_stop = int(row.get('start_stop', 0))
            edge = row.get('edge', row.get('clk', None))
        else:
            if isinstance(row, (list, tuple)):
                if len(row) >= 3:
                    if isinstance(row[-1], str) and ('pos' in row[-1].lower() or 'neg' in row[-1].lower()):
                        edge = row[-1]
                        reset = int(row[0])
                        start_stop = int(row[1])
                    elif isinstance(row[0], str) and ('pos' in row[0].lower() or 'neg' in row[0].lower()):
                        edge = row[0]
                        reset = int(row[1])
                        start_stop = int(row[2])
                    else:
                        edge = row[0]
                        reset = int(row[1])
                        start_stop = int(row[2])
                elif len(row) == 2:
                    reset = int(row[0])
                    start_stop = int(row[1])
                elif len(row) == 1:
                    reset = int(row[0])
            else:
                reset = int(row)

        if isinstance(edge, str):
            e = edge.lower()
            is_pos = ('pos' in e) or ('ris' in e) or (e == '1') or (e == 'true')
        else:
            is_pos = (i % 2 == 0)

        out.append({'seconds': seconds, 'minutes': minutes, 'hour': hour})

        if reset:
            seconds = 0
            minutes = 0
            hour = 0
            divider = 0
        elif is_pos and start_stop:
            if divider == 3:
                divider = 0
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
                divider += 1

    return out
