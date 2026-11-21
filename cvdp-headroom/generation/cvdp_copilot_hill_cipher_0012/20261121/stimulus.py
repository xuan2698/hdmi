def stimulus(rng, cycles):
    rows = []
    # Directed edge cases first
    directed = [
        (0, 0, 0),                      # reset
        (0, 0, 0),                      # idle
        (0, 1, 0),                      # start with zeros
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 1, (1<<45)-1),              # start with max key, zero plaintext
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
        (0, 1, 0),                      # start with zero key, max plaintext
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 1, (1<<45)-1),              # both max
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
        (0, 0, (1<<45)-1),
    ]
    # Back-to-back starts
    for _ in range(3):
        directed.append((0, 1, rng.getrandbits(45)))
        directed.append((0, 0, rng.getrandbits(45)))
        directed.append((0, 0, rng.getrandbits(45)))
        directed.append((0, 0, rng.getrandbits(45)))
        directed.append((0, 0, rng.getrandbits(45)))

    idx = 0
    n_directed = len(directed)
    # Track plaintext separately since directed tuples only have (reset,start,key)
    # We'll generate plaintext per row
    pt_list = []
    for i in range(n_directed):
        if i < 2:
            pt_list.append(0)
        elif i == 2:
            pt_list.append(0)
        elif i == 7:
            pt_list.append(0)
        elif i == 12:
            pt_list.append((1<<15)-1)
        elif i == 17:
            pt_list.append((1<<15)-1)
        else:
            pt_list.append(rng.getrandbits(15))

    for i in range(cycles):
        if i < n_directed:
            r, s, k = directed[i]
            p = pt_list[i]
        else:
            # Random exploration with occasional start pulses
            r = 0
            s = 1 if rng.random() < 0.15 else 0
            p = rng.getrandbits(15)
            k = rng.getrandbits(45)
            # Occasionally inject reset
            if rng.random() < 0.02:
                r = 1
                s = 0
        row = {'reset': r, 'start': s, 'plaintext': p, 'key': k}
        # Mid-cycle changes sometimes
        if i >= n_directed and rng.random() < 0.1:
            mid = {}
            if rng.random() < 0.5:
                mid['start'] = 1 if rng.random() < 0.5 else 0
            if rng.random() < 0.3:
                mid['plaintext'] = rng.getrandbits(15)
            if rng.random() < 0.3:
                mid['key'] = rng.getrandbits(45)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
