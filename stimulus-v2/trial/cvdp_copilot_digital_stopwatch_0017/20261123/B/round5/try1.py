def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        elif i == 5:
            start_stop = 1
        elif i == 5000:
            start_stop = 0
        elif i == 5100:
            start_stop = 1
        elif i == 12000:
            reset = 1
        elif i == 12003:
            reset = 0
            start_stop = 0
        elif i == 12005:
            start_stop = 1
        elif i == 18000:
            start_stop = 0
        elif i == 18100:
            start_stop = 1
        elif i == 24000:
            reset = 1
        elif i == 24002:
            reset = 0
            start_stop = 1
        elif i == 30000:
            start_stop = 0
        elif i == 30100:
            start_stop = 1
        elif i == 36000:
            reset = 1
        elif i == 36004:
            reset = 0
            start_stop = 0
        elif i == 36006:
            start_stop = 1
        elif i == 42000:
            start_stop = 0
        elif i == 42100:
            start_stop = 1
        elif i == 48000:
            reset = 1
        elif i == 48003:
            reset = 0
            start_stop = 1
        elif i == 54000:
            start_stop = 0
        elif i == 54100:
            start_stop = 1
        elif i == 60000:
            reset = 1
        elif i == 60002:
            reset = 0
            start_stop = 0
        elif i == 60004:
            start_stop = 1
        elif i == 66000:
            start_stop = 0
        elif i == 66100:
            start_stop = 1
        elif i == 72000:
            reset = 1
        elif i == 72003:
            reset = 0
            start_stop = 1
        elif i == 78000:
            start_stop = 0
        elif i == 78100:
            start_stop = 1
        elif i == 84000:
            reset = 1
        elif i == 84002:
            reset = 0
            start_stop = 0
        elif i == 84004:
            start_stop = 1
        elif i == 90000:
            start_stop = 0
        elif i == 90100:
            start_stop = 1
        elif i == 96000:
            reset = 1
        elif i == 96003:
            reset = 0
            start_stop = 1
        elif i == 102000:
            start_stop = 0
        elif i == 102100:
            start_stop = 1
        elif i == 108000:
            reset = 1
        elif i == 108002:
            reset = 0
            start_stop = 0
        elif i == 108004:
            start_stop = 1
        elif i == 114000:
            start_stop = 0
        elif i == 114100:
            start_stop = 1
        elif i == 120000:
            reset = 1
        elif i == 120003:
            reset = 0
            start_stop = 1
        elif i == 126000:
            start_stop = 0
        elif i == 126100:
            start_stop = 1
        elif i == 132000:
            reset = 1
        elif i == 132002:
            reset = 0
            start_stop = 0
        elif i == 132004:
            start_stop = 1
        elif i == 138000:
            start_stop = 0
        elif i == 138100:
            start_stop = 1
        elif i == 144000:
            reset = 1
        elif i == 144003:
            reset = 0
            start_stop = 1
        elif i == 150000:
            start_stop = 0
        elif i == 150100:
            start_stop = 1
        elif i == 156000:
            reset = 1
        elif i == 156002:
            reset = 0
            start_stop = 0
        elif i == 156004:
            start_stop = 1
        elif i == 162000:
            start_stop = 0
        elif i == 162100:
            start_stop = 1
        elif i == 168000:
            reset = 1
        elif i == 168003:
            reset = 0
            start_stop = 1
        elif i == 174000:
            start_stop = 0
        elif i == 174100:
            start_stop = 1
        elif i == 180000:
            reset = 1
        elif i == 180002:
            reset = 0
            start_stop = 0
        elif i == 180004:
            start_stop = 1
        elif i == 186000:
            start_stop = 0
        elif i == 186100:
            start_stop = 1
        elif i == 192000:
            reset = 1
        elif i == 192003:
            reset = 0
            start_stop = 1
        elif i == 198000:
            start_stop = 0
        elif i == 198100:
            start_stop = 1
        elif i == 204000:
            reset = 1
        elif i == 204002:
            reset = 0
            start_stop = 0
        elif i == 204004:
            start_stop = 1
        elif i == 210000:
            start_stop = 0
        elif i == 210100:
            start_stop = 1
        elif i == 216000:
            reset = 1
        elif i == 216003:
            reset = 0
            start_stop = 1
        elif i == 222000:
            start_stop = 0
        elif i == 222100:
            start_stop = 1
        elif i == 228000:
            reset = 1
        elif i == 228002:
            reset = 0
            start_stop = 0
        elif i == 228004:
            start_stop = 1
        elif i == 234000:
            start_stop = 0
        elif i == 234100:
            start_stop = 1
        elif i == 240000:
            reset = 1
        elif i == 240003:
            reset = 0
            start_stop = 1
        elif i == 246000:
            start_stop = 0
        elif i == 246100:
            start_stop = 1
        elif i == 252000:
            reset = 1
        elif i == 252002:
            reset = 0
            start_stop = 0
        elif i == 252004:
            start_stop = 1
        elif i == 258000:
            start_stop = 0
        elif i == 258100:
            start_stop = 1
        elif i == 264000:
            reset = 1
        elif i == 264003:
            reset = 0
            start_stop = 1
        elif i == 270000:
            start_stop = 0
        elif i == 270100:
            start_stop = 1
        elif i == 276000:
            reset = 1
        elif i == 276002:
            reset = 0
            start_stop = 0
        elif i == 276004:
            start_stop = 1
        elif i == 282000:
            start_stop = 0
        elif i == 282100:
            start_stop = 1
        elif i == 288000:
            reset = 1
        elif i == 288003:
            reset = 0
            start_stop = 1
        elif i == 294000:
            start_stop = 0
        elif i == 294100:
            start_stop = 1
        elif i == 300000:
            reset = 1
        elif i == 300002:
            reset = 0
            start_stop = 0
        elif i == 300004:
            start_stop = 1
        elif i == 306000:
            start_stop = 0
        elif i == 306100:
            start_stop = 1
        elif i == 312000:
            reset = 1
        elif i == 312003:
            reset = 0
            start_stop = 1
        elif i == 318000:
            start_stop = 0
        elif i == 318100:
            start_stop = 1
        elif i == 324000:
            reset = 1
        elif i == 324002:
            reset = 0
            start_stop = 0
        elif i == 324004:
            start_stop = 1
        elif i == 330000:
            start_stop = 0
        elif i == 330100:
            start_stop = 1
        elif i == 336000:
            reset = 1
        elif i == 336003:
            reset = 0
            start_stop = 1
        elif i == 342000:
            start_stop = 0
        elif i == 342100:
            start_stop = 1
        elif i == 348000:
            reset = 1
        elif i == 348002:
            reset = 0
            start_stop = 0
        elif i == 348004:
            start_stop = 1
        elif i == 354000:
            start_stop = 0
        elif i == 354100:
            start_stop = 1
        elif i == 360000:
            reset = 1
        elif i == 360003:
            reset = 0
            start_stop = 1
        elif i == 366000:
            start_stop = 0
        elif i == 366100:
            start_stop = 1
        elif i == 372000:
            reset = 1
        elif i == 372002:
            reset = 0
            start_stop = 0
        elif i == 372004:
            start_stop = 1
        elif i == 378000:
            start_stop = 0
        elif i == 378100:
            start_stop = 1
        elif i == 384000:
            reset = 1
        elif i == 384003:
            reset = 0
            start_stop = 1
        elif i == 390000:
            start_stop = 0
        elif i == 390100:
            start_stop = 1
        elif i == 396000:
            reset = 1
        elif i == 396002:
            reset = 0
            start_stop = 0
        elif i == 396004:
            start_stop = 1
        rows.append({'reset': reset & 1, 'start_stop': start_stop & 1})
    return rows
