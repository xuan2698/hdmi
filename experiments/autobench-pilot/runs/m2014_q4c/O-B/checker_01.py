def reference(vectors):
    return [{'q': 0 if row['r'] else row['d']} for row in vectors]
