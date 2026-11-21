def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    mid = None
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        elif i < 12:
            reset = 0
            start_stop = 1
        elif i < 20:
            reset = 0
            start_stop = 0
        elif i < 60:
            reset = 0
            start_stop = 1
        elif i < 70:
            reset = 0
            start_stop = 0
        elif i < 130:
            reset = 0
            start_stop = 1
        elif i < 140:
            reset = 0
            start_stop = 0
        elif i < 200:
            reset = 0
            start_stop = 1
        elif i < 210:
            reset = 0
            start_stop = 0
        elif i < 270:
            reset = 0
            start_stop = 1
        elif i < 280:
            reset = 0
            start_stop = 0
        elif i < 340:
            reset = 0
            start_stop = 1
        elif i < 350:
            reset = 0
            start_stop = 0
        elif i < 410:
            reset = 0
            start_stop = 1
        elif i < 420:
            reset = 0
            start_stop = 0
        elif i < 480:
            reset = 0
            start_stop = 1
        elif i < 490:
            reset = 0
            start_stop = 0
        elif i < 550:
            reset = 0
            start_stop = 1
        elif i < 560:
            reset = 0
            start_stop = 0
        elif i < 620:
            reset = 0
            start_stop = 1
        elif i < 630:
            reset = 0
            start_stop = 0
        elif i < 690:
            reset = 0
            start_stop = 1
        elif i < 700:
            reset = 0
            start_stop = 0
        elif i < 760:
            reset = 0
            start_stop = 1
        elif i < 770:
            reset = 0
            start_stop = 0
        elif i < 830:
            reset = 0
            start_stop = 1
        elif i < 840:
            reset = 0
            start_stop = 0
        elif i < 900:
            reset = 0
            start_stop = 1
        elif i < 910:
            reset = 0
            start_stop = 0
        elif i < 970:
            reset = 0
            start_stop = 1
        elif i < 980:
            reset = 0
            start_stop = 0
        elif i < 1040:
            reset = 0
            start_stop = 1
        elif i < 1050:
            reset = 0
            start_stop = 0
        elif i < 1110:
            reset = 0
            start_stop = 1
        elif i < 1120:
            reset = 0
            start_stop = 0
        elif i < 1180:
            reset = 0
            start_stop = 1
        elif i < 1190:
            reset = 0
            start_stop = 0
        elif i < 1250:
            reset = 0
            start_stop = 1
        elif i < 1260:
            reset = 0
            start_stop = 0
        elif i < 1320:
            reset = 0
            start_stop = 1
        elif i < 1330:
            reset = 0
            start_stop = 0
        elif i < 1390:
            reset = 0
            start_stop = 1
        elif i < 1400:
            reset = 0
            start_stop = 0
        elif i < 1460:
            reset = 0
            start_stop = 1
        elif i < 1470:
            reset = 0
            start_stop = 0
        elif i < 1530:
            reset = 0
            start_stop = 1
        elif i < 1540:
            reset = 0
            start_stop = 0
        elif i < 1600:
            reset = 0
            start_stop = 1
        elif i < 1610:
            reset = 0
            start_stop = 0
        elif i < 1670:
            reset = 0
            start_stop = 1
        elif i < 1680:
            reset = 0
            start_stop = 0
        elif i < 1740:
            reset = 0
            start_stop = 1
        elif i < 1750:
            reset = 0
            start_stop = 0
        elif i < 1810:
            reset = 0
            start_stop = 1
        elif i < 1820:
            reset = 0
            start_stop = 0
        elif i < 1880:
            reset = 0
            start_stop = 1
        elif i < 1890:
            reset = 0
            start_stop = 0
        elif i < 1950:
            reset = 0
            start_stop = 1
        elif i < 1960:
            reset = 0
            start_stop = 0
        elif i < 2020:
            reset = 0
            start_stop = 1
        elif i < 2030:
            reset = 0
            start_stop = 0
        elif i < 2090:
            reset = 0
            start_stop = 1
        elif i < 2100:
            reset = 0
            start_stop = 0
        elif i < 2160:
            reset = 0
            start_stop = 1
        elif i < 2170:
            reset = 0
            start_stop = 0
        elif i < 2230:
            reset = 0
            start_stop = 1
        elif i < 2240:
            reset = 0
            start_stop = 0
        elif i < 2300:
            reset = 0
            start_stop = 1
        elif i < 2310:
            reset = 0
            start_stop = 0
        elif i < 2370:
            reset = 0
            start_stop = 1
        elif i < 2380:
            reset = 0
            start_stop = 0
        elif i < 2440:
            reset = 0
            start_stop = 1
        elif i < 2450:
            reset = 0
            start_stop = 0
        elif i < 2510:
            reset = 0
            start_stop = 1
        elif i < 2520:
            reset = 0
            start_stop = 0
        elif i < 2580:
            reset = 0
            start_stop = 1
        elif i < 2590:
            reset = 0
            start_stop = 0
        elif i < 2650:
            reset = 0
            start_stop = 1
        elif i < 2660:
            reset = 0
            start_stop = 0
        elif i < 2720:
            reset = 0
            start_stop = 1
        elif i < 2730:
            reset = 0
            start_stop = 0
        elif i < 2790:
            reset = 0
            start_stop = 1
        elif i < 2800:
            reset = 0
            start_stop = 0
        elif i < 2860:
            reset = 0
            start_stop = 1
        elif i < 2870:
            reset = 0
            start_stop = 0
        elif i < 2930:
            reset = 0
            start_stop = 1
        elif i < 2940:
            reset = 0
            start_stop = 0
        elif i < 3000:
            reset = 0
            start_stop = 1
        elif i < 3010:
            reset = 0
            start_stop = 0
        elif i < 3070:
            reset = 0
            start_stop = 1
        elif i < 3080:
            reset = 0
            start_stop = 0
        elif i < 3140:
            reset = 0
            start_stop = 1
        elif i < 3150:
            reset = 0
            start_stop = 0
        elif i < 3210:
            reset = 0
            start_stop = 1
        elif i < 3220:
            reset = 0
            start_stop = 0
        elif i < 3280:
            reset = 0
            start_stop = 1
        elif i < 3290:
            reset = 0
            start_stop = 0
        elif i < 3350:
            reset = 0
            start_stop = 1
        elif i < 3360:
            reset = 0
            start_stop = 0
        elif i < 3420:
            reset = 0
            start_stop = 1
        elif i < 3430:
            reset = 0
            start_stop = 0
        elif i < 3490:
            reset = 0
            start_stop = 1
        elif i < 3500:
            reset = 0
            start_stop = 0
        elif i < 3560:
            reset = 0
            start_stop = 1
        elif i < 3570:
            reset = 0
            start_stop = 0
        elif i < 3630:
            reset = 0
            start_stop = 1
        elif i < 3640:
            reset = 0
            start_stop = 0
        elif i < 3700:
            reset = 0
            start_stop = 1
        elif i < 3710:
            reset = 0
            start_stop = 0
        elif i < 3770:
            reset = 0
            start_stop = 1
        elif i < 3780:
            reset = 0
            start_stop = 0
        elif i < 3840:
            reset = 0
            start_stop = 1
        elif i < 3850:
            reset = 0
            start_stop = 0
        elif i < 3910:
            reset = 0
            start_stop = 1
        elif i < 3920:
            reset = 0
            start_stop = 0
        elif i < 3980:
            reset = 0
            start_stop = 1
        else:
            reset = 0
            start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 3 and rng.random() < 0.02:
            mid = {'start_stop': 1 - start_stop}
    return rows
