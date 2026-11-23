def reference(vectors):
    state = 0  # A=0, B=1, C=2, D=3
    prev_clk = 0
    result = []
    for row in vectors:
        if 'clk' in row:
            clk = row['clk'] & 1
            edge = (prev_clk == 0 and clk == 1)
            prev_clk = clk
        else:
            edge = True

        if edge:
            if row.get('reset', 0):
                state = 0
            else:
                inp = row.get('in', 0) & 1
                if state == 0:
                    state = 1 if inp else 0
                elif state == 1:
                    state = 2 if not inp else 1
                elif state == 2:
                    state = 3 if inp else 0
                else:
                    state = 1 if inp else 2

        result.append({'out': 1 if state == 3 else 0})
    return result
