def reference(vectors):
    cnt = 0
    pulse = 0
    sec = 0
    mi = 0
    hr = 0
    out = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        start = row.get('start_stop', 0)

        if reset:
            cnt = 0
            pulse = 0
            sec = 0
            mi = 0
            hr = 0

        out.append({'seconds': sec, 'minutes': mi, 'hour': hr})

        if i % 2 == 0:
            if reset:
                cnt = 0
                pulse = 0
                sec = 0
                mi = 0
                hr = 0
            else:
                if start:
                    if cnt == 3:
                        ncnt = 0
                        npulse = 1
                    else:
                        ncnt = cnt + 1
                        npulse = 0
                else:
                    ncnt = cnt
                    npulse = 0

                nsec = sec
                nmi = mi
                nhr = hr

                if pulse:
                    if sec == 59:
                        nsec = 0
                        if mi == 59:
                            nmi = 0
                            nhr = 1
                        else:
                            nmi = mi + 1
                    else:
                        nsec = sec + 1

                cnt, pulse, sec, mi, hr = ncnt, npulse, nsec, nmi, nhr

    return out
