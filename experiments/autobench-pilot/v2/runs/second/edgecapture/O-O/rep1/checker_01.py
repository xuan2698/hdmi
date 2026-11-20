def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0)
        if reset:
            state = 0
        else:
            prev = getattr(reference, '_prev', None)
            if prev is not None:
                state |= (prev & ~inp) & 0xFFFFFFFF
        reference._prev = inp
        out.append({'out': state & 0xFFFFFFFF})
    if hasattr(reference, '_prev'):
        del reference._prev
    return out
