def reference(vectors):
    results = []
    state = None  # unknown until reset
    for v in vectors:
        areset = v.get('areset')
        x = v.get('x')
        if areset == 1:
            state = 'S0'
            z = 0
        else:
            if state is None:
                z = None
            else:
                if state == 'S0':
                    if x == 0:
                        z = 0
                        state = 'S0'
                    else:
                        z = 1
                        state = 'S1'
                elif state == 'S1':
                    if x == 0:
                        z = 1
                        state = 'S1'
                    else:
                        z = 0
                        state = 'S0'
                else:
                    z = None
        results.append({'z': z})
    return results
