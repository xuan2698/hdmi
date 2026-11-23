def reference(vectors):
    state = 0
    prev_clk = 0
    result = []
    for v in vectors:
        do_edge = True
        if "clk" in v:
            clk = v["clk"] & 1
            do_edge = (prev_clk == 0 and clk == 1)
            prev_clk = clk
        if do_edge:
            if v.get("reset", 0) & 1:
                state = 0
            else:
                i = v.get("in", 0) & 1
                if state == 0:
                    state = 1 if i else 0
                elif state == 1:
                    state = 1 if i else 2
                elif state == 2:
                    state = 3 if i else 0
                else:
                    state = 1 if i else 2
        result.append({"out": 1 if state == 3 else 0})
    return result
