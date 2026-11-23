def reference(vectors):
    sec = 0
    mins = 0
    hour = 0
    div = 0
    results = []
    for idx, row in enumerate(vectors):
        reset = int(row.get('reset', 0)) & 1
        if reset:
            sec = 0
            mins = 0
            hour = 0
            div = 0
        if 'clk' in row:
            clk_val = int(row['clk'])
            posedge = (clk_val == 1)
        elif 'clock' in row:
            clk_val = int(row['clock'])
            posedge = (clk_val == 1)
        else:
            edge = row.get('edge')
            if isinstance(edge, str):
                posedge = edge.lower().startswith('pos')
            elif edge is not None:
                posedge = (int(edge) == 1)
            else:
                posedge = (idx % 2 == 0)
        results.append({'seconds': sec & 0x3F, 'minutes': mins & 0x3F, 'hour': hour & 1})
        if posedge and not reset:
            start_stop = int(row.get('start_stop', 0)) & 1
            pulse = (div == 3)
            div_next = 0 if pulse else div + 1
            if start_stop and pulse:
                if sec == 59:
                    sec_next = 0
                    if mins == 59:
                        mins_next = 0
                        hour_next = 1
                    else:
                        mins_next = mins + 1
                        hour_next = hour
                else:
                    sec_next = sec + 1
                    mins_next = mins
                    hour_next = hour
            else:
                sec_next = sec
                mins_next = mins
                hour_next = hour
            sec = sec_next
            mins = mins_next
            hour = hour_next
            div = div_next
    return results
