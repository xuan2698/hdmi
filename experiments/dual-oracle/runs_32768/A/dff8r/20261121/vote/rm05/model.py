def reference(vectors):
    return [{'q': 0 if v['reset'] else (v['d'] & 0xFF)} for v in vectors]
