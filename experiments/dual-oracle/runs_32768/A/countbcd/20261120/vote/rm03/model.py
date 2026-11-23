def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
        else:
            reset = row
        if reset:
            q = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15
            
            c1 = 1 if d0 == 9 else 0
            d0 = 0 if d0 == 9 else d0 + 1
            
            c2 = 1 if (c1 and d1 == 9) else 0
            d1 = (d1 + c1) % 10
            
            c3 = 1 if (c2 and d2 == 9) else 0
            d2 = (d2 + c2) % 10
            
            d3 = (d3 + c3) % 10
            
            q = (d3 << 12) | (d2 << 8) | (d1 << 4) | d0
        
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        
        e0 = 1 if ones == 9 else 0
        e1 = 1 if (ones == 9 and tens == 9) else 0
        e2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        
        ena = (e2 << 2) | (e1 << 1) | e0
        result.append({'q': q, 'ena': ena})
    return result
