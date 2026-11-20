def stimulus(rng, cycles):
    result = []
    # State machine: 2's complementer, LSB first.
    # Moore machine: output depends only on state.
    # States: S0 (initial, no carry yet, output 0), S1 (carry propagated, output 1)
    # Actually for 2's complement LSB-first:
    #   Start in state "pass" (output = input bit) until first 1 seen.
    #   After first 1, output = NOT input bit (carry propagates).
    # Moore: state A = haven't seen first 1 yet (output 0), state B = seen first 1 (output 1).
    # Wait, Moore output depends only on state, not input. But 2's complement LSB-first:
    #   output bit = input bit while in "pass" mode (before first 1)
    #   output bit = NOT input bit after first 1
    # That's Mealy, not Moore. For Moore, we need output to depend only on state.
    # Moore version: state encodes what output to produce.
    #   State P0: output 0, meaning we're in pass mode and... no, output must be fixed per state.
    # Actually a Moore 2's complementer: output is determined by state.
    #   State S0: output 0 (pass mode, but output is 0 regardless of input? No...)
    # Hmm. Standard Moore 2's complementer:
    #   State A: output 0, "before first 1" - but then output would always be 0 in pass mode,
    #   which is wrong since pass mode outputs the input bit.
    # Wait - re-read: "Moore state machine" - output depends only on state.
    # For 2's complement LSB first: while scanning, output = input until first 1, then NOT input.
    # Moore can't do this directly because output depends on input in pass mode.
    # Unless... the Moore output is the 2's complement bit, and state tracks carry.
    # Actually the standard Moore 2's complementer:
    #   State S0 (carry=0, haven't seen 1): output = 0? No.
    # Let me reconsider. The classic Moore 2's complementer has states:
    #   S0: output 0 (initial, no carry)
    #   S1: output 1 (carry active)
    # Transitions: from S0, if x=0 stay S0, if x=1 go to S1.
    #              from S1, stay S1 regardless.
    # Output: S0 -> 0, S1 -> 1.
    # But this gives output = 0 until first 1, then 1 forever. That's not 2's complement.
    # Hmm, that's wrong. Let me think again.
    # 2's complement of N: ~N + 1. LSB first:
    #   bit 0: N[0] (since +1 only affects if N[0]=0... wait)
    #   Actually: 2's comp bits: start with carry=1. For each bit from LSB:
    #     out = x XOR carry_in; carry_out = carry_in AND x? No.
    #   Standard: out = x XOR carry; carry = carry AND x (for 2's complement, carry starts at 1).
    #   Wait: adding 1 to ~N. ~N bit = NOT x. Add 1: sum = NOT x + carry.
    #   carry starts 1. sum bit = NOT x XOR carry, new carry = NOT x AND carry.
    #   If carry=1: sum = NOT x XOR 1 = x, new carry = NOT x.
    #     So while carry=1: out = x, carry becomes NOT x.
    #     Once x=1, NOT x=0, carry=0.
    #   If carry=0: sum = NOT x, new carry = 0.
    #   So: before first 1 (carry=1): out = x. After first 1 (carry=0): out = NOT x.
    # That matches. But this is Mealy (out depends on x and state).
    # For Moore: state must encode output. States:
    #   S_pass: output = ? depends on x. Can't be Moore.
    # Unless we delay: Moore output is registered. The spec says Moore, so output is
    # a function of state only. Perhaps the intended Moore machine:
    #   State S0: output 0, "carry still 1, haven't seen 1" - but output should be x.
    # Hmm, maybe the Moore machine outputs the bit one cycle late? Or maybe the
    # intended design: state = (carry, last_output)? 
    # Actually a common Moore 2's complementer:
    #   States: A (output 0), B (output 1).
    #   A: x=0 -> A, x=1 -> B. B: x=0 -> B, x=1 -> B.
    #   Output: A=0, B=1.
    # This outputs 0 until first 1, then 1. That's a "detect first 1" machine, not 2's comp.
    # I think the spec might be loosely worded. Let me just generate stimulus that
    # exercises the interface: reset, x bits, various patterns.
    # The stimulus just needs to drive areset and x. The DUT behavior is what it is.
    # I'll generate: reset pulses, random bits, runs of zeros, runs of ones, alternating.
    
    state = 'idle'
    pattern = []
    idx = 0
    
    # Build a varied sequence of (areset, x) pairs
    seq = []
    
    # Start with reset asserted for a few cycles
    for _ in range(rng.randrange(1, 4)):
        seq.append((1, 0))
    
    # Then release reset and drive bits
    while len(seq) < cycles:
        choice = rng.randrange(10)
        if choice == 0:
            # Assert reset briefly
            for _ in range(rng.randrange(1, 3)):
                if len(seq) < cycles:
                    seq.append((1, rng.getrandbits(1)))
        elif choice == 1:
            # Run of zeros
            for _ in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, 0))
        elif choice == 2:
            # Run of ones
            for _ in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, 1))
        elif choice == 3:
            # Alternating
            start = rng.getrandbits(1)
            for i in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, (start + i) & 1))
        elif choice == 4:
            # Single 1 then zeros (tests carry propagation)
            if len(seq) < cycles:
                seq.append((0, 1))
            for _ in range(rng.randrange(2, 6)):
                if len(seq) < cycles:
                    seq.append((0, 0))
        elif choice == 5:
            # Zeros then single 1
            for _ in range(rng.randrange(1, 5)):
                if len(seq) < cycles:
                    seq.append((0, 0))
            if len(seq) < cycles:
                seq.append((0, 1))
        else:
            # Random bits
            for _ in range(rng.randrange(1, 6)):
                if len(seq) < cycles:
                    seq.append((0, rng.getrandbits(1)))
    
    seq = seq[:cycles]
    
    for areset, x in seq:
        result.append({'areset': areset, 'x': x})
    
    return result
