def reference(vectors):
    state = 0
    prev_clk = 0
    result = []
    for row in vectors:
        clk = row.get('clk', None)
        if clk is None:
            posedge = True
        else:
            posedge = (clk == 1 and prev_clk == 0)
            prev_clk = clk
        if posedge:
            reset = row.get('reset', 0)
            if reset:
                state = 0
            else:
                inp = row.get('in', 0)
                if state == 0:
                    state = 0 if inp == 0 else 1
                elif state == 1:
                    state = 2 if inp == 0 else 1
                elif state == 2:
                    state = 0 if inp == 0 else 3
                else:
                    state = 2 if inp == 0 else 1
        result.append({'out': 1 if state == 3 else 0})
    return result
