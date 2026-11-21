def stimulus(rng, cycles):
    rows = []
    # Phase plan (in cycles):
    # 0-4: reset asserted
    # 5-9: idle with start_stop=0
    # 10-19: start_stop=1 (run)
    # 20-24: start_stop=0 (pause)
    # 25-34: start_stop=1 (run)
    # 35-39: reset asserted mid-run
    # 40-49: start_stop=1 (run after reset)
    # 50-59: start_stop=0
    # 60-69: start_stop=1
    # 70-74: reset
    # 75-84: start_stop=1
    # 85-94: start_stop=0
    # 95-104: start_stop=1
    # 105-109: reset
    # 110-119: start_stop=1
    # 120-129: start_stop=0
    # 130-139: start_stop=1
    # 140-144: reset
    # 145-154: start_stop=1
    # 155-164: start_stop=0
    # 165-174: start_stop=1
    # 175-179: reset
    # 180-189: start_stop=1
    # 190-199: start_stop=0
    # 200-209: start_stop=1
    # 210-214: reset
    # 215-224: start_stop=1
    # 225-234: start_stop=0
    # 235-244: start_stop=1
    # 245-249: reset
    # 250-259: start_stop=1
    # 260-269: start_stop=0
    # 270-279: start_stop=1
    # 280-284: reset
    # 285-294: start_stop=1
    # 295-304: start_stop=0
    # 305-314: start_stop=1
    # 315-319: reset
    # 320-329: start_stop=1
    # 330-339: start_stop=0
    # 340-349: start_stop=1
    # 350-354: reset
    # 355-364: start_stop=1
    # 365-374: start_stop=0
    # 375-384: start_stop=1
    # 385-389: reset
    # 390-399: start_stop=1
    # 400-409: start_stop=0
    # 410-419: start_stop=1
    # 420-424: reset
    # 425-434: start_stop=1
    # 435-444: start_stop=0
    # 445-454: start_stop=1
    # 455-459: reset
    # 460-469: start_stop=1
    # 470-479: start_stop=0
    # 480-489: start_stop=1
    # 490-494: reset
    # 495-504: start_stop=1
    # 505-514: start_stop=0
    # 515-524: start_stop=1
    # 525-529: reset
    # 530-539: start_stop=1
    # 540-549: start_stop=0
    # 550-559: start_stop=1
    # 560-564: reset
    # 565-574: start_stop=1
    # 575-584: start_stop=0
    # 585-594: start_stop=1
    # 595-599: reset
    # 600-609: start_stop=1
    # 610-619: start_stop=0
    # 620-629: start_stop=1
    # 630-634: reset
    # 635-644: start_stop=1
    # 645-654: start_stop=0
    # 655-664: start_stop=1
    # 665-669: reset
    # 670-679: start_stop=1
    # 680-689: start_stop=0
    # 690-699: start_stop=1
    # 700-704: reset
    # 705-714: start_stop=1
    # 715-724: start_stop=0
    # 725-734: start_stop=1
    # 735-739: reset
    # 740-749: start_stop=1
    # 750-759: start_stop=0
    # 760-769: start_stop=1
    # 770-774: reset
    # 775-784: start_stop=1
    # 785-794: start_stop=0
    # 795-804: start_stop=1
    # 805-809: reset
    # 810-819: start_stop=1
    # 820-829: start_stop=0
    # 830-839: start_stop=1
    # 840-844: reset
    # 845-854: start_stop=1
    # 855-864: start_stop=0
    # 865-874: start_stop=1
    # 875-879: reset
    # 880-889: start_stop=1
    # 890-899: start_stop=0
    # 900-909: start_stop=1
    # 910-914: reset
    # 915-924: start_stop=1
    # 925-934: start_stop=0
    # 935-944: start_stop=1
    # 945-949: reset
    # 950-959: start_stop=1
    # 960-969: start_stop=0
    # 970-979: start_stop=1
    # 980-984: reset
    # 985-994: start_stop=1
    # 995-1004: start_stop=0
    # 1005-1014: start_stop=1
    # 1015-1019: reset
    # 1020-1029: start_stop=1
    # 1030-1039: start_stop=0
    # 1040-1049: start_stop=1
    # 1050-1054: reset
    # 1055-1064: start_stop=1
    # 1065-1074: start_stop=0
    # 1075-1084: start_stop=1
    # 1085-1089: reset
    # 1090-1099: start_stop=1
    # 1100-1109: start_stop=0
    # 1110-1119: start_stop=1
    # 1120-1124: reset
    # 1125-1134: start_stop=1
    # 1135-1144: start_stop=0
    # 1145-1154: start_stop=1
    # 1155-1159: reset
    # 1160-1169: start_stop=1
    # 1170-1179: start_stop=0
    # 1180-1189: start_stop=1
    # 1190-1194: reset
    # 1195-1204: start_stop=1
    # 1205-1214: start_stop=0
    # 1215-1224: start_stop=1
    # 1225-1229: reset
    # 1230-1239: start_stop=1
    # 1240-1249: start_stop=0
    # 1250-1259: start_stop=1
    # 1260-1264: reset
    # 1265-1274: start_stop=1
    # 1275-1284: start_stop=0
    # 1285-1294: start_stop=1
    # 1295-1299: reset
    # 1300-1309: start_stop=1
    # 1310-1319: start_stop=0
    # 1320-1329: start_stop=1
    # 1330-1334: reset
    # 1335-1344: start_stop=1
    # 1345-1354: start_stop=0
    # 1355-1364: start_stop=1
    # 1365-1369: reset
    # 1370-1379: start_stop=1
    # 1380-1389: start_stop=0
    # 1390-1399: start_stop=1
    # 1400-1404: reset
    # 1405-1414: start_stop=1
    # 1415-1424: start_stop=0
    # 1425-1434: start_stop=1
    # 1435-1439: reset
    # 1440-1449: start_stop=1
    # 1450-1459: start_stop=0
    # 1460-1469: start_stop=1
    # 1470-1474: reset
    # 1475-1484: start_stop=1
    # 1485-1494: start_stop=0
    # 1495-1504: start_stop=1
    # 1505-1509: reset
    # 1510-1519: start_stop=1
    # 1520-1529: start_stop=0
    # 1530-1539: start_stop=1
    # 1540-1544: reset
    # 1545-1554: start_stop=1
    # 1555-1564: start_stop=0
    # 1565-1574: start_stop=1
    # 1575-1579: reset
    # 1580-1589: start_stop=1
    # 1590-1599: start_stop=0
    # 1600-1609: start_stop=1
    # 1610-1614: reset
    # 1615-1624: start_stop=1
    # 1625-1634: start_stop=0
    # 1635-1644: start_stop=1
    # 1645-1649: reset
    # 1650-1659: start_stop=1
    # 1660-1669: start_stop=0
    # 1670-1679: start_stop=1
    # 1680-1684: reset
    # 1685-1694: start_stop=1
    # 1695-1704: start_stop=0
    # 1705-1714: start_stop=1
    # 1715-1719: reset
    # 1720-1729: start_stop=1
    # 1730-1739: start_stop=0
    # 1740-1749: start_stop=1
    # 1750-1754: reset
    # 1755-1764: start_stop=1
    # 1765-1774: start_stop=0
    # 1775-1784: start_stop=1
    # 1785-1789: reset
    # 1790-1799: start_stop=1
    # 1800-1809: start_stop=0
    # 1810-1819: start_stop=1
    # 1820-1824: reset
    # 1825-1834: start_stop=1
    # 1835-1844: start_stop=0
    # 1845-1854: start_stop=1
    # 1855-1859: reset
    # 1860-1869: start_stop=1
    # 1870-1879: start_stop=0
    # 1880-1889: start_stop=1
    # 1890-1894: reset
    # 1895-1904: start_stop=1
    # 1905-1914: start_stop=0
    # 1915-1924: start_stop=1
    # 1925-1929: reset
    # 1930-1939: start_stop=1
    # 1940-1949: start_stop=0
    # 1950-1959: start_stop=1
    # 1960-1964: reset
    # 1965-1974: start_stop=1
    # 1975-1984: start_stop=0
    # 1985-1994: start_stop=1
    # 1995-1999: reset
    # Simplify: use a repeating pattern with occasional random perturbations.
    pattern = []
    # Build a base repeating pattern of length 50
    for i in range(50):
        if i < 5:
            pattern.append((1, 0))
        elif i < 10:
            pattern.append((0, 0))
        elif i < 20:
            pattern.append((0, 1))
        elif i < 25:
            pattern.append((0, 0))
        elif i < 35:
            pattern.append((0, 1))
        elif i < 40:
            pattern.append((1, 0))
        elif i < 45:
            pattern.append((0, 1))
        else:
            pattern.append((0, 0))
    for c in range(cycles):
        base = pattern[c % 50]
        reset = base[0]
        start_stop = base[1]
        # Random perturbations
        r = rng.random()
        if r < 0.02:
            reset = 1
        elif r < 0.04:
            reset = 0
        r2 = rng.random()
        if r2 < 0.05:
            start_stop = 1 - start_stop
        row = {'reset': reset, 'start_stop': start_stop}
        # Occasionally add mid-cycle changes
        if rng.random() < 0.1:
            mid = {}
            if rng.random() < 0.5:
                mid['reset'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['start_stop'] = rng.randint(0, 1)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
