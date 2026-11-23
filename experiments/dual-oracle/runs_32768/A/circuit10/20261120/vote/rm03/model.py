def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        a = int(row['a']) & 1
        b = int(row['b']) & 1
        nxt = int((a & b) | (state & (a ^ b)))
        q = int(a ^ b ^ nxt)
        outputs.append({'q': q, 'state': nxt})
        state = nxt
    return outputs
