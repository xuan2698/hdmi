def stimulus(rng, cycles):
    result = []
    # State tracking for targeted sequence generation
    # We want to cover: reset, f pulse, x=1,0,1 detection, g=1, y within 2 cycles, y timeout
    phase = 0  # 0=reset, 1=after reset waiting, 2=x sequence, 3=g monitoring y
    x_hist = []
    y_count = 0
    resetn = 0
    x = 0
    y = 0
    cycle_count = 0
    # We'll build a plan of phases with random lengths
    # Phase plan: reset for a few cycles, then release, then x sequence, then y test
    reset_len = rng.randrange(1, 4)
    # After reset release, f=1 for one cycle (state B), then monitor x
    # x sequence: need 1,0,1 in three successive cycles
    # We'll generate x values to hit 1,0,1, but also sometimes random to test non-matching
    # Then g=1, monitor y for up to 2 cycles
    # Then either y=1 (permanent g=1) or y=0 twice (permanent g=0)
    # Then stay in that state until reset again
    
    # Build a sequence of (resetn, x, y) tuples
    seq = []
    
    # Initial reset phase
    for _ in range(reset_len):
        seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))
    
    # Decide how many test rounds
    num_rounds = rng.randrange(1, 4)
    for _ in range(num_rounds):
        # Release reset
        seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        # f=1 cycle, x can be anything
        seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        
        # Now try to produce x=1,0,1 sequence
        # Sometimes inject random noise before
        noise_len = rng.randrange(0, 3)
        for _ in range(noise_len):
            seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        
        # Produce 1,0,1
        seq.append((1, 1, rng.getrandbits(1)))
        seq.append((1, 0, rng.getrandbits(1)))
        seq.append((1, 1, rng.getrandbits(1)))
        
        # Now g=1, monitor y for up to 2 cycles
        # Decide outcome: y=1 within 2 cycles, or timeout
        outcome = rng.randrange(0, 3)  # 0: y=1 first cycle, 1: y=1 second cycle, 2: timeout
        if outcome == 0:
            seq.append((1, rng.getrandbits(1), 1))
            # g stays 1 permanently, add some cycles
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        elif outcome == 1:
            seq.append((1, rng.getrandbits(1), 0))
            seq.append((1, rng.getrandbits(1), 1))
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        else:
            seq.append((1, rng.getrandbits(1), 0))
            seq.append((1, rng.getrandbits(1), 0))
            # g=0 permanently
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        
        # Reset again before next round (if any)
        if _ < num_rounds - 1:
            for _ in range(rng.randrange(1, 3)):
                seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))
    
    # Fill or truncate to exactly cycles
    while len(seq) < cycles:
        # Random tail, but occasionally reset
        if rng.random() < 0.1:
            seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))
        else:
            seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
    
    seq = seq[:cycles]
    
    for (r, xv, yv) in seq:
        result.append({'resetn': r, 'x': xv, 'y': yv})
    
    return result
