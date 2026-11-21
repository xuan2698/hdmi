def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        row = {
            'addr_a': rng.randrange(8192),
            'en_a': rng.randrange(2),
            'be_a': rng.randrange(16),
            'data_in_a': rng.randrange(1 << 32),
            'addr_b': rng.randrange(8192),
            'en_b': rng.randrange(2),
            'be_b': rng.randrange(16),
            'data_in_b': rng.randrange(1 << 32),
        }
        if i % 97 == 0:
            row['en_a'] = 1
            row['be_a'] = 15
        if i % 89 == 0:
            row['en_b'] = 1
            row['be_b'] = 15
        if i % 53 == 0:
            row['addr_b'] = row['addr_a']
            row['en_b'] = 1
            row['en_a'] = 1
        if i % 211 == 0:
            row['en_a'] = 0
            row['en_b'] = 0
        if i % 37 == 0:
            row['be_a'] = 1 << (i % 4)
            row['be_b'] = 1 << ((i + 2) % 4)
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 71 == 0:
            row['be_a'] = 0
            row['be_b'] = 0
        if i % 131 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['addr_a'] = row['addr_b']
            row['en_a'] = 1
            row['en_b'] = 1
        if i % 43 == 0:
            row['be_a'] = 0
            row['be_b'] = 0
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 59 == 0:
            row['be_a'] = 15
            row['be_b'] = 0
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 61 == 0:
            row['be_a'] = 0
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 67 == 0:
            row['be_a'] = 1 << (i % 4)
            row['be_b'] = 1 << (i % 4)
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 73 == 0:
            row['be_a'] = 1 << ((i + 1) % 4)
            row['be_b'] = 1 << ((i + 3) % 4)
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 79 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = row['data_in_b']
        if i % 83 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = (~row['data_in_b']) & 0xFFFFFFFF
        if i % 101 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0
            row['data_in_b'] = 0xFFFFFFFF
        if i % 103 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xFFFFFFFF
            row['data_in_b'] = 0
        if i % 107 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xAAAAAAAA
            row['data_in_b'] = 0x55555555
        if i % 109 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x55555555
            row['data_in_b'] = 0xAAAAAAAA
        if i % 113 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x12345678
            row['data_in_b'] = 0x9ABCDEF0
        if i % 127 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x9ABCDEF0
            row['data_in_b'] = 0x12345678
        if i % 137 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xDEADBEEF
            row['data_in_b'] = 0xCAFEBABE
        if i % 139 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xCAFEBABE
            row['data_in_b'] = 0xDEADBEEF
        if i % 149 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xFFFFFFFF
            row['data_in_b'] = 0xFFFFFFFF
        if i % 151 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0
            row['data_in_b'] = 0
        if i % 157 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x000000FF
            row['data_in_b'] = 0xFF000000
        if i % 163 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xFF000000
            row['data_in_b'] = 0x000000FF
        if i % 167 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x00FF00FF
            row['data_in_b'] = 0xFF00FF00
        if i % 173 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xFF00FF00
            row['data_in_b'] = 0x00FF00FF
        if i % 179 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x0F0F0F0F
            row['data_in_b'] = 0xF0F0F0F0
        if i % 181 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xF0F0F0F0
            row['data_in_b'] = 0x0F0F0F0F
        if i % 191 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x33333333
            row['data_in_b'] = 0xCCCCCCCC
        if i % 193 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xCCCCCCCC
            row['data_in_b'] = 0x33333333
        if i % 197 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0x0000FFFF
            row['data_in_b'] = 0xFFFF0000
        if i % 199 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
            row['data_in_a'] = 0xFFFF0000
            row['data_in_b'] = 0x0000FFFF
        rows.append(row)
    return rows
