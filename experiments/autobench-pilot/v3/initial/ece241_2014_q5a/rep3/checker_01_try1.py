def reference(vectors):
    st = 0
    out = []
    for row in vectors:
        if row.get('areset', 0):
            st = 0
        else:
            x = row.get('x', 0)
            if st == 0:
                z = x
                st = 1 if x else 0
            else:
                z = 1 - x
        out.append({'z': z})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset', 0):
                st = 0
            elif 'x' in m:
                x = m['x']
                if st == 0:
                    st = 1 if x else 0
                else:
                    st = 1
    return out
