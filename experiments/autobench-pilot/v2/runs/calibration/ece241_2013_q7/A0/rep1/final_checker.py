def reference(vectors):
    results = []
    q = None
    for v in vectors:
        j = v.get('j', 0)
        k = v.get('k', 0)
        clk = v.get('clk', 0)
        prev_clk = v.get('_prev_clk', None)
        # Determine if rising edge
        if prev_clk is None:
            # First sample: no prior clock known; treat as no edge unless clk is 1?
            # Spec says inputs driven before active rising edge; samples observed after edge.
            # We assume each vector represents a clock cycle with rising edge.
            edge = True
        else:
            edge = (prev_clk == 0 and clk == 1)
        if edge:
            if q is None:
                # unknown power-up; JK with J=K=0 keeps unknown
                if j == 0 and k == 0:
                    q = None
                elif j == 0 and k == 1:
                    q = 0
                elif j == 1 and k == 0:
                    q = 1
                else:
                    q = None  # ~Qold unknown
            else:
                if j == 0 and k == 0:
                    pass
                elif j == 0 and k == 1:
                    q = 0
                elif j == 1 and k == 0:
                    q = 1
                else:
                    q = 1 - q
        results.append({'Q': q})
    return results
