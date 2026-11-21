def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            if i < 10:
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 30:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 210:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 410:
                start_stop = 0
            elif i < 600:
                start_stop = 1
            elif i < 610:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 810:
                start_stop = 0
            elif i < 1000:
                start_stop = 1
            elif i < 1010:
                start_stop = 0
            elif i < 1200:
                start_stop = 1
            elif i < 1210:
                start_stop = 0
            elif i < 1400:
                start_stop = 1
            elif i < 1410:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1610:
                start_stop = 0
            elif i < 1800:
                start_stop = 1
            elif i < 1810:
                start_stop = 0
            elif i < 2000:
                start_stop = 1
            elif i < 2010:
                start_stop = 0
            elif i < 2200:
                start_stop = 1
            elif i < 2210:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2410:
                start_stop = 0
            elif i < 2600:
                start_stop = 1
            elif i < 2610:
                start_stop = 0
            elif i < 2800:
                start_stop = 1
            elif i < 2810:
                start_stop = 0
            elif i < 3000:
                start_stop = 1
            elif i < 3010:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3210:
                start_stop = 0
            elif i < 3400:
                start_stop = 1
            elif i < 3410:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3610:
                start_stop = 0
            elif i < 3800:
                start_stop = 1
            elif i < 3810:
                start_stop = 0
            elif i < 4000:
                start_stop = 1
            elif i < 4010:
                start_stop = 0
            elif i < 4200:
                start_stop = 1
            elif i < 4210:
                start_stop = 0
            elif i < 4400:
                start_stop = 1
            elif i < 4410:
                start_stop = 0
            elif i < 4600:
                start_stop = 1
            elif i < 4610:
                start_stop = 0
            elif i < 4800:
                start_stop = 1
            elif i < 4810:
                start_stop = 0
            elif i < 5000:
                start_stop = 1
            elif i < 5010:
                start_stop = 0
            elif i < 5200:
                start_stop = 1
            elif i < 5210:
                start_stop = 0
            elif i < 5400:
                start_stop = 1
            elif i < 5410:
                start_stop = 0
            elif i < 5600:
                start_stop = 1
            elif i < 5610:
                start_stop = 0
            elif i < 5800:
                start_stop = 1
            elif i < 5810:
                start_stop = 0
            elif i < 6000:
                start_stop = 1
            elif i < 6010:
                start_stop = 0
            elif i < 6200:
                start_stop = 1
            elif i < 6210:
                start_stop = 0
            elif i < 6400:
                start_stop = 1
            elif i < 6410:
                start_stop = 0
            elif i < 6600:
                start_stop = 1
            elif i < 6610:
                start_stop = 0
            elif i < 6800:
                start_stop = 1
            elif i < 6810:
                start_stop = 0
            elif i < 7000:
                start_stop = 1
            elif i < 7010:
                start_stop = 0
            elif i < 7200:
                start_stop = 1
            elif i < 7210:
                start_stop = 0
            elif i < 7400:
                start_stop = 1
            elif i < 7410:
                start_stop = 0
            elif i < 7600:
                start_stop = 1
            elif i < 7610:
                start_stop = 0
            elif i < 7800:
                start_stop = 1
            elif i < 7810:
                start_stop = 0
            elif i < 8000:
                start_stop = 1
            elif i < 8010:
                start_stop = 0
            elif i < 8200:
                start_stop = 1
            elif i < 8210:
                start_stop = 0
            elif i < 8400:
                start_stop = 1
            elif i < 8410:
                start_stop = 0
            elif i < 8600:
                start_stop = 1
            elif i < 8610:
                start_stop = 0
            elif i < 8800:
                start_stop = 1
            elif i < 8810:
                start_stop = 0
            elif i < 9000:
                start_stop = 1
            elif i < 9010:
                start_stop = 0
            elif i < 9200:
                start_stop = 1
            elif i < 9210:
                start_stop = 0
            elif i < 9400:
                start_stop = 1
            elif i < 9410:
                start_stop = 0
            elif i < 9600:
                start_stop = 1
            elif i < 9610:
                start_stop = 0
            elif i < 9800:
                start_stop = 1
            elif i < 9810:
                start_stop = 0
            elif i < 10000:
                start_stop = 1
            elif i < 10010:
                start_stop = 0
            elif i < 10200:
                start_stop = 1
            elif i < 10210:
                start_stop = 0
            elif i < 10400:
                start_stop = 1
            elif i < 10410:
                start_stop = 0
            elif i < 10600:
                start_stop = 1
            elif i < 10610:
                start_stop = 0
            elif i < 10800:
                start_stop = 1
            elif i < 10810:
                start_stop = 0
            elif i < 11000:
                start_stop = 1
            elif i < 11010:
                start_stop = 0
            elif i < 11200:
                start_stop = 1
            elif i < 11210:
                start_stop = 0
            elif i < 11400:
                start_stop = 1
            elif i < 11410:
                start_stop = 0
            elif i < 11600:
                start_stop = 1
            elif i < 11610:
                start_stop = 0
            elif i < 11800:
                start_stop = 1
            elif i < 11810:
                start_stop = 0
            elif i < 12000:
                start_stop = 1
            elif i < 12010:
                start_stop = 0
            elif i < 12200:
                start_stop = 1
            elif i < 12210:
                start_stop = 0
            elif i < 12400:
                start_stop = 1
            elif i < 12410:
                start_stop = 0
            elif i < 12600:
                start_stop = 1
            elif i < 12610:
                start_stop = 0
            elif i < 12800:
                start_stop = 1
            elif i < 12810:
                start_stop = 0
            elif i < 13000:
                start_stop = 1
            elif i < 13010:
                start_stop = 0
            elif i < 13200:
                start_stop = 1
            elif i < 13210:
                start_stop = 0
            elif i < 13400:
                start_stop = 1
            elif i < 13410:
                start_stop = 0
            elif i < 13600:
                start_stop = 1
            elif i < 13610:
                start_stop = 0
            elif i < 13800:
                start_stop = 1
            elif i < 13810:
                start_stop = 0
            elif i < 14000:
                start_stop = 1
            elif i < 14010:
                start_stop = 0
            elif i < 14200:
                start_stop = 1
            elif i < 14210:
                start_stop = 0
            elif i < 14400:
                start_stop = 1
            elif i < 14410:
                start_stop = 0
            elif i < 14600:
                start_stop = 1
            elif i < 14610:
                start_stop = 0
            elif i < 14800:
                start_stop = 1
            elif i < 14810:
                start_stop = 0
            elif i < 15000:
                start_stop = 1
            elif i < 15010:
                start_stop = 0
            elif i < 15200:
                start_stop = 1
            elif i < 15210:
                start_stop = 0
            elif i < 15400:
                start_stop = 1
            elif i < 15410:
                start_stop = 0
            elif i < 15600:
                start_stop = 1
            elif i < 15610:
                start_stop = 0
            elif i < 15800:
                start_stop = 1
            elif i < 15810:
                start_stop = 0
            elif i < 16000:
                start_stop = 1
            elif i < 16010:
                start_stop = 0
            elif i < 16200:
                start_stop = 1
            elif i < 16210:
                start_stop = 0
            elif i < 16400:
                start_stop = 1
            elif i < 16410:
                start_stop = 0
            elif i < 16600:
                start_stop = 1
            elif i < 16610:
                start_stop = 0
            elif i < 16800:
                start_stop = 1
            elif i < 16810:
                start_stop = 0
            elif i < 17000:
                start_stop = 1
            elif i < 17010:
                start_stop = 0
            elif i < 17200:
                start_stop = 1
            elif i < 17210:
                start_stop = 0
            elif i < 17400:
                start_stop = 1
            elif i < 17410:
                start_stop = 0
            elif i < 17600:
                start_stop = 1
            elif i < 17610:
                start_stop = 0
            elif i < 17800:
                start_stop = 1
            elif i < 17810:
                start_stop = 0
            elif i < 18000:
                start_stop = 1
            elif i < 18010:
                start_stop = 0
            elif i < 18200:
                start_stop = 1
            elif i < 18210:
                start_stop = 0
            elif i < 18400:
                start_stop = 1
            elif i < 18410:
                start_stop = 0
            elif i < 18600:
                start_stop = 1
            elif i < 18610:
                start_stop = 0
            elif i < 18800:
                start_stop = 1
            elif i < 18810:
                start_stop = 0
            elif i < 19000:
                start_stop = 1
            elif i < 19010:
                start_stop = 0
            elif i < 19200:
                start_stop = 1
            elif i < 19210:
                start_stop = 0
            elif i < 19400:
                start_stop = 1
            elif i < 19410:
                start_stop = 0
            elif i < 19600:
                start_stop = 1
            elif i < 19610:
                start_stop = 0
            elif i < 19800:
                start_stop = 1
            elif i < 19810:
                start_stop = 0
            else:
                start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
