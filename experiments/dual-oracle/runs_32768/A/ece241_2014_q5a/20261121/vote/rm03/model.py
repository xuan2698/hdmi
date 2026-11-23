def reference(vectors):
    carry = 1
    result = []
    for v in vectors:
        areset = int(v.get('areset', 0)) & 1
        x = int(v.get('x', 0)) & 1
        if areset:
            carry = 1
            z = 0
        else:
            z = ((x ^ 1) ^ carry) & 1
            carry = ((x ^ 1) & carry) & 1
        result.append({'z': z})
    return result
