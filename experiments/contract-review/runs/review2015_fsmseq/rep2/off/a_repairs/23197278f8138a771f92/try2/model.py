def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S2, 3=S3, 4=S4
    state = 0
    start_shifting = 0
    out = []
    for row in vectors:
        reset = row['reset']
        data = row['data']
        # R1: synchronous reset, priority 1
        if reset == 1:
            state = 0
            start_shifting = 0
        else:
            # R2: state S4 latches start_shifting high forever
            if state == 4:
                start_shifting = 1
            # R3: state S3 and data==1 -> found sequence
            elif state == 3 and data == 1:
                state = 4
                start_shifting = 1
            else:
                # R4: normal search transitions
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 3 if data == 0 else 2
                elif state == 3:
                    # data == 0 here (data==1 handled above)
                    state = 1 if data == 1 else 0
                start_shifting = 0
        out.append({'start_shifting': start_shifting})
    return out
