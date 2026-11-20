def stimulus(rng, cycles):
    seq = []
    def add(reset, data):
        seq.append({'reset': reset, 'data': data})
    def rand_bit():
        return rng.getrandbits(1)
    def rand_bits(n):
        return [rand_bit() for _ in range(n)]
    def emit_bits(bits, reset=0):
        for b in bits:
            add(reset, b)
    def reset_pulse():
        add(1, rand_bit())
        add(0, rand_bit())
    def target_1101():
        return [1, 1, 0, 1]
    def near_miss():
        return rng.choice([[1, 1, 0, 0], [1, 0, 1], [1, 1, 1, 0, 1], [0, 1, 1, 0, 1], [1, 1, 0, 1, 1, 0, 1]])
    def random_run(n):
        emit_bits(rand_bits(n))
    def directed():
        reset_pulse()
        emit_bits(target_1101())
        random_run(rng.randrange(1, 4))
        reset_pulse()
        emit_bits([1, 1, 0, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 1, 0, 0, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([0, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 0, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 1, 0, 1, 0, 1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 1, 0, 1])
        emit_bits([1, 1, 0, 1])
        reset_pulse()
        emit_bits([1, 1, 0, 1])
        add(1, 1)
        add(0, 1)
        add(0, 0)
        add(0, 1)
    directed()
    while len(seq) < cycles:
        choice = rng.randrange(6)
        if choice == 0:
            reset_pulse()
        elif choice == 1:
            emit_bits(target_1101())
        elif choice == 2:
            emit_bits(near_miss())
        elif choice == 3:
            random_run(rng.randrange(1, 8))
        elif choice == 4:
            emit_bits([1, 1, 0, 1])
            random_run(rng.randrange(0, 3))
        else:
            emit_bits(rand_bits(rng.randrange(1, 5)))
    return seq[:cycles]
