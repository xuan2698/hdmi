def reference(vectors):
    st = 0
    fc = 0
    out = []
    for v in vectors:
        a = v['areset']
        bl = v['bump_left']
        br = v['bump_right']
        g = v['ground']
        d = v['dig']
        if a:
            st = 0
            fc = 0
        else:
            if st == 0:
                if g == 0:
                    st = 2
                    fc = 1
                elif d:
                    st = 4
                    fc = 0
                elif bl:
                    st = 1
                    fc = 0
                else:
                    fc = 0
            elif st == 1:
                if g == 0:
                    st = 3
                    fc = 1
                elif d:
                    st = 5
                    fc = 0
                elif br:
                    st = 0
                    fc = 0
                else:
                    fc = 0
            elif st == 2:
                if g:
                    if fc > 20:
                        st = 6
                    else:
                        st = 0
                    fc = 0
                else:
                    fc += 1
            elif st == 3:
                if g:
                    if fc > 20:
                        st = 6
                    else:
                        st = 1
                    fc = 0
                else:
                    fc += 1
            elif st == 4:
                if g == 0:
                    st = 2
                    fc = 1
                else:
                    fc = 0
            elif st == 5:
                if g == 0:
                    st = 3
                    fc = 1
                else:
                    fc = 0
            else:
                fc = 0
        out.append({
            'walk_left': 1 if st == 0 else 0,
            'walk_right': 1 if st == 1 else 0,
            'aaah': 1 if st == 2 or st == 3 else 0,
            'digging': 1 if st == 4 or st == 5 else 0
        })
    return out
