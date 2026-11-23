def reference(vectors):
    s = 0
    out = []
    for row in vectors:
        if int(row['areset']):
            s = 0
        else:
            x = int(row['x'])
            if s == 0:
                if x:
                    s = 1
            else:
                s = 2 if x else 1
        out.append({'z': 1 if s == 1 else 0})
        mid = row.get('mid')
        if mid and int(mid.get('areset', 0)):
            s = 0
    return out
