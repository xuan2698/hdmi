def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 3:
            reset = 0
        if i == 5:
            start_stop = 1
        if i == 200:
            start_stop = 0
        if i == 250:
            start_stop = 1
        if i == 5000:
            reset = 1
        if i == 5003:
            reset = 0
        if i == 5005:
            start_stop = 1
        if i == 12000:
            start_stop = 0
        if i == 12050:
            start_stop = 1
        if i == 18000:
            reset = 1
        if i == 18003:
            reset = 0
        if i == 18005:
            start_stop = 1
        if i == 24000:
            start_stop = 0
        if i == 24010:
            start_stop = 1
        if i == 30000:
            reset = 1
        if i == 30003:
            reset = 0
        if i == 30005:
            start_stop = 1
        if i == 36000:
            start_stop = 0
        if i == 36020:
            start_stop = 1
        if i == 42000:
            reset = 1
        if i == 42003:
            reset = 0
        if i == 42005:
            start_stop = 1
        if i == 48000:
            start_stop = 0
        if i == 48030:
            start_stop = 1
        if i == 54000:
            reset = 1
        if i == 54003:
            reset = 0
        if i == 54005:
            start_stop = 1
        if i == 60000:
            start_stop = 0
        if i == 60040:
            start_stop = 1
        if i == 66000:
            reset = 1
        if i == 66003:
            reset = 0
        if i == 66005:
            start_stop = 1
        if i == 72000:
            start_stop = 0
        if i == 72050:
            start_stop = 1
        if i == 78000:
            reset = 1
        if i == 78003:
            reset = 0
        if i == 78005:
            start_stop = 1
        if i == 84000:
            start_stop = 0
        if i == 84060:
            start_stop = 1
        if i == 90000:
            reset = 1
        if i == 90003:
            reset = 0
        if i == 90005:
            start_stop = 1
        if i == 96000:
            start_stop = 0
        if i == 96070:
            start_stop = 1
        if i == 102000:
            reset = 1
        if i == 102003:
            reset = 0
        if i == 102005:
            start_stop = 1
        if i == 108000:
            start_stop = 0
        if i == 108080:
            start_stop = 1
        if i == 114000:
            reset = 1
        if i == 114003:
            reset = 0
        if i == 114005:
            start_stop = 1
        if i == 120000:
            start_stop = 0
        if i == 120090:
            start_stop = 1
        if i == 126000:
            reset = 1
        if i == 126003:
            reset = 0
        if i == 126005:
            start_stop = 1
        if i == 132000:
            start_stop = 0
        if i == 132100:
            start_stop = 1
        if i == 138000:
            reset = 1
        if i == 138003:
            reset = 0
        if i == 138005:
            start_stop = 1
        if i == 144000:
            start_stop = 0
        if i == 144110:
            start_stop = 1
        if i == 150000:
            reset = 1
        if i == 150003:
            reset = 0
        if i == 150005:
            start_stop = 1
        if i == 156000:
            start_stop = 0
        if i == 156120:
            start_stop = 1
        if i == 162000:
            reset = 1
        if i == 162003:
            reset = 0
        if i == 162005:
            start_stop = 1
        if i == 168000:
            start_stop = 0
        if i == 168130:
            start_stop = 1
        if i == 174000:
            reset = 1
        if i == 174003:
            reset = 0
        if i == 174005:
            start_stop = 1
        if i == 180000:
            start_stop = 0
        if i == 180140:
            start_stop = 1
        if i == 186000:
            reset = 1
        if i == 186003:
            reset = 0
        if i == 186005:
            start_stop = 1
        if i == 192000:
            start_stop = 0
        if i == 192150:
            start_stop = 1
        if i == 198000:
            reset = 1
        if i == 198003:
            reset = 0
        if i == 198005:
            start_stop = 1
        if i == 204000:
            start_stop = 0
        if i == 204160:
            start_stop = 1
        if i == 210000:
            reset = 1
        if i == 210003:
            reset = 0
        if i == 210005:
            start_stop = 1
        if i == 216000:
            start_stop = 0
        if i == 216170:
            start_stop = 1
        if i == 222000:
            reset = 1
        if i == 222003:
            reset = 0
        if i == 222005:
            start_stop = 1
        if i == 228000:
            start_stop = 0
        if i == 228180:
            start_stop = 1
        if i == 234000:
            reset = 1
        if i == 234003:
            reset = 0
        if i == 234005:
            start_stop = 1
        if i == 240000:
            start_stop = 0
        if i == 240190:
            start_stop = 1
        if i == 246000:
            reset = 1
        if i == 246003:
            reset = 0
        if i == 246005:
            start_stop = 1
        if i == 252000:
            start_stop = 0
        if i == 252200:
            start_stop = 1
        if i == 258000:
            reset = 1
        if i == 258003:
            reset = 0
        if i == 258005:
            start_stop = 1
        if i == 264000:
            start_stop = 0
        if i == 264210:
            start_stop = 1
        if i == 270000:
            reset = 1
        if i == 270003:
            reset = 0
        if i == 270005:
            start_stop = 1
        if i == 276000:
            start_stop = 0
        if i == 276220:
            start_stop = 1
        if i == 282000:
            reset = 1
        if i == 282003:
            reset = 0
        if i == 282005:
            start_stop = 1
        if i == 288000:
            start_stop = 0
        if i == 288230:
            start_stop = 1
        if i == 294000:
            reset = 1
        if i == 294003:
            reset = 0
        if i == 294005:
            start_stop = 1
        if i == 300000:
            start_stop = 0
        if i == 300240:
            start_stop = 1
        if i == 306000:
            reset = 1
        if i == 306003:
            reset = 0
        if i == 306005:
            start_stop = 1
        if i == 312000:
            start_stop = 0
        if i == 312250:
            start_stop = 1
        if i == 318000:
            reset = 1
        if i == 318003:
            reset = 0
        if i == 318005:
            start_stop = 1
        if i == 324000:
            start_stop = 0
        if i == 324260:
            start_stop = 1
        if i == 330000:
            reset = 1
        if i == 330003:
            reset = 0
        if i == 330005:
            start_stop = 1
        if i == 336000:
            start_stop = 0
        if i == 336270:
            start_stop = 1
        if i == 342000:
            reset = 1
        if i == 342003:
            reset = 0
        if i == 342005:
            start_stop = 1
        if i == 348000:
            start_stop = 0
        if i == 348280:
            start_stop = 1
        if i == 354000:
            reset = 1
        if i == 354003:
            reset = 0
        if i == 354005:
            start_stop = 1
        if i == 360000:
            start_stop = 0
        if i == 360290:
            start_stop = 1
        if i == 366000:
            reset = 1
        if i == 366003:
            reset = 0
        if i == 366005:
            start_stop = 1
        if i == 372000:
            start_stop = 0
        if i == 372300:
            start_stop = 1
        if i == 378000:
            reset = 1
        if i == 378003:
            reset = 0
        if i == 378005:
            start_stop = 1
        if i == 384000:
            start_stop = 0
        if i == 384310:
            start_stop = 1
        if i == 390000:
            reset = 1
        if i == 390003:
            reset = 0
        if i == 390005:
            start_stop = 1
        if i == 396000:
            start_stop = 0
        if i == 396320:
            start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        rows.append(row)
    return rows
