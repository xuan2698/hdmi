def reference(vectors):
    # States:
    # A: beginning state (reset)
    # B: f=1 for one cycle
    # C: monitoring x for 1,0,1
    # D: g=1, monitoring y for up to 2 cycles
    # E: g=1 permanently
    # F: g=0 permanently
    state = 'A'
    # x history tracking for sequence 1,0,1
    # We track progress: 0 = none, 1 = got 1, 2 = got 1,0, 3 = got 1,0,1
    xprog = 0
    # y monitoring counter in state D
    ycount = 0
    results = []
    for row in vectors:
        resetn = row['resetn']
        x = row['x']
        y = row['y']
        # Synchronous active-low reset: if resetn==0, next state is A
        if resetn == 0:
            state = 'A'
            xprog = 0
            ycount = 0
            f = 0
            g = 0
        else:
            # Compute outputs based on current state (Moore machine)
            if state == 'A':
                f = 0
                g = 0
            elif state == 'B':
                f = 1
                g = 0
            elif state == 'C':
                f = 0
                g = 0
            elif state == 'D':
                f = 0
                g = 1
            elif state == 'E':
                f = 0
                g = 1
            elif state == 'F':
                f = 0
                g = 0
            else:
                f = 0
                g = 0
            # Compute next state
            if state == 'A':
                state = 'B'
                xprog = 0
            elif state == 'B':
                state = 'C'
                xprog = 0
            elif state == 'C':
                # monitor x for 1,0,1
                if xprog == 0:
                    if x == 1:
                        xprog = 1
                    else:
                        xprog = 0
                elif xprog == 1:
                    if x == 0:
                        xprog = 2
                    elif x == 1:
                        xprog = 1
                    else:
                        xprog = 0
                elif xprog == 2:
                    if x == 1:
                        xprog = 3
                        state = 'D'
                        ycount = 0
                    elif x == 0:
                        xprog = 0
                    else:
                        xprog = 0
                # if xprog == 3 shouldn't happen here
            elif state == 'D':
                # g=1, monitor y for up to 2 cycles
                if y == 1:
                    state = 'E'
                else:
                    ycount += 1
                    if ycount >= 2:
                        state = 'F'
            elif state == 'E':
                state = 'E'
            elif state == 'F':
                state = 'F'
        results.append({'f': f, 'g': g})
    return results
