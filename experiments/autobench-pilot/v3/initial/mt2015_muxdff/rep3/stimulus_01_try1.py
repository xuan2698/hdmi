def stimulus(rng, cycles):
    rows = []
    rows.append({'r': 0, 'L': 1, 'clk': 0})
    rows.append({'r': 7, 'L': 1, 'clk': 1})
    rows.append({'r': 0, 'L': 0, 'clk': 0})
    rows.append({'r': 0, 'L': 0, 'clk': 1})
    rows.append({'r': 5, 'L': 1, 'clk': 0})
    rows.append({'r': 5, 'L': 1, 'clk': 1})
    rows.append({'r': 0, 'L': 0, 'clk': 0})
    rows.append({'r': 0, 'L': 0, 'clk': 1})
    rows.append({'r': 3, 'L': 1, 'clk': 0})
    rows.append({'r': 3, 'L': 1, 'clk': 1})
    rows.append({'r': 0, 'L': 0, 'clk': 0})
    rows.append({'r': 0, 'L': 0, 'clk': 1})
    rows.append({'r': 6, 'L': 1, 'clk': 0})
    rows.append({'r': 6, 'L': 1, 'clk': 1})
    rows.append({'r': 0, 'L': 0, 'clk': 0})
    rows.append({'r': 0, 'L': 0, 'clk': 1})
    while len(rows) < cycles:
        r = rng.getrandbits(3)
        L = rng.getrandbits(1)
        rows.append({'r': r, 'L': L, 'clk': 0})
        if len(rows) < cycles:
            mid = {}
            if rng.random() < 0.3:
                mid['r'] = rng.getrandbits(3)
            if rng.random() < 0.3:
                mid['L'] = rng.getrandbits(1)
            row = {'r': r, 'L': L, 'clk': 1}
            if mid:
                row['mid'] = mid
            rows.append(row)
    return rows[:cycles]
