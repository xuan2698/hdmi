def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 15000:
            reset = 1
        elif i == 15003:
            reset = 0
        elif i == 30000:
            reset = 1
        elif i == 30002:
            reset = 0
        elif i == 45000:
            reset = 1
        elif i == 45001:
            reset = 0
        elif i > 45001 and i < 45010:
            reset = 1 if (i % 2 == 0) else 0
        elif i >= 45010 and i < 45020:
            reset = 0
        elif i >= 45020 and i < 45030:
            reset = 1 if (i % 3 == 0) else 0
        elif i >= 45030 and i < 45040:
            reset = 0
        elif i >= 45040 and i < 45050:
            reset = 1 if (i % 5 == 0) else 0
        elif i >= 45050 and i < 45060:
            reset = 0
        elif i >= 45060 and i < 45070:
            reset = 1 if (i % 7 == 0) else 0
        elif i >= 45070 and i < 45080:
            reset = 0
        elif i >= 45080 and i < 45090:
            reset = 1 if (i % 11 == 0) else 0
        elif i >= 45090 and i < 45100:
            reset = 0
        elif i >= 45100 and i < 45110:
            reset = 1 if (i % 13 == 0) else 0
        elif i >= 45110 and i < 45120:
            reset = 0
        elif i >= 45120 and i < 45130:
            reset = 1 if (i % 17 == 0) else 0
        elif i >= 45130 and i < 45140:
            reset = 0
        elif i >= 45140 and i < 45150:
            reset = 1 if (i % 19 == 0) else 0
        elif i >= 45150 and i < 45160:
            reset = 0
        elif i >= 45160 and i < 45170:
            reset = 1 if (i % 23 == 0) else 0
        elif i >= 45170 and i < 45180:
            reset = 0
        elif i >= 45180 and i < 45190:
            reset = 1 if (i % 29 == 0) else 0
        elif i >= 45190 and i < 45200:
            reset = 0
        elif i >= 45200 and i < 45210:
            reset = 1 if (i % 31 == 0) else 0
        elif i >= 45210 and i < 45220:
            reset = 0
        elif i >= 45220 and i < 45230:
            reset = 1 if (i % 37 == 0) else 0
        elif i >= 45230 and i < 45240:
            reset = 0
        elif i >= 45240 and i < 45250:
            reset = 1 if (i % 41 == 0) else 0
        elif i >= 45250 and i < 45260:
            reset = 0
        elif i >= 45260 and i < 45270:
            reset = 1 if (i % 43 == 0) else 0
        elif i >= 45270 and i < 45280:
            reset = 0
        elif i >= 45280 and i < 45290:
            reset = 1 if (i % 47 == 0) else 0
        elif i >= 45290 and i < 45300:
            reset = 0
        elif i >= 45300 and i < 45310:
            reset = 1 if (i % 53 == 0) else 0
        elif i >= 45310 and i < 45320:
            reset = 0
        elif i >= 45320 and i < 45330:
            reset = 1 if (i % 59 == 0) else 0
        elif i >= 45330 and i < 45340:
            reset = 0
        elif i >= 45340 and i < 45350:
            reset = 1 if (i % 61 == 0) else 0
        elif i >= 45350 and i < 45360:
            reset = 0
        elif i >= 45360 and i < 45370:
            reset = 1 if (i % 67 == 0) else 0
        elif i >= 45370 and i < 45380:
            reset = 0
        elif i >= 45380 and i < 45390:
            reset = 1 if (i % 71 == 0) else 0
        elif i >= 45390 and i < 45400:
            reset = 0
        elif i >= 45400 and i < 45410:
            reset = 1 if (i % 73 == 0) else 0
        elif i >= 45410 and i < 45420:
            reset = 0
        elif i >= 45420 and i < 45430:
            reset = 1 if (i % 79 == 0) else 0
        elif i >= 45430 and i < 45440:
            reset = 0
        elif i >= 45440 and i < 45450:
            reset = 1 if (i % 83 == 0) else 0
        elif i >= 45450 and i < 45460:
            reset = 0
        elif i >= 45460 and i < 45470:
            reset = 1 if (i % 89 == 0) else 0
        elif i >= 45470 and i < 45480:
            reset = 0
        elif i >= 45480 and i < 45490:
            reset = 1 if (i % 97 == 0) else 0
        elif i >= 45490 and i < 45500:
            reset = 0
        elif i >= 45500 and i < 45510:
            reset = 1 if (i % 101 == 0) else 0
        elif i >= 45510 and i < 45520:
            reset = 0
        elif i >= 45520 and i < 45530:
            reset = 1 if (i % 103 == 0) else 0
        elif i >= 45530 and i < 45540:
            reset = 0
        elif i >= 45540 and i < 45550:
            reset = 1 if (i % 107 == 0) else 0
        elif i >= 45550 and i < 45560:
            reset = 0
        elif i >= 45560 and i < 45570:
            reset = 1 if (i % 109 == 0) else 0
        elif i >= 45570 and i < 45580:
            reset = 0
        elif i >= 45580 and i < 45590:
            reset = 1 if (i % 113 == 0) else 0
        elif i >= 45590 and i < 45600:
            reset = 0
        elif i >= 45600 and i < 45610:
            reset = 1 if (i % 127 == 0) else 0
        elif i >= 45610 and i < 45620:
            reset = 0
        elif i >= 45620 and i < 45630:
            reset = 1 if (i % 131 == 0) else 0
        elif i >= 45630 and i < 45640:
            reset = 0
        elif i >= 45640 and i < 45650:
            reset = 1 if (i % 137 == 0) else 0
        elif i >= 45650 and i < 45660:
            reset = 0
        elif i >= 45660 and i < 45670:
            reset = 1 if (i % 139 == 0) else 0
        elif i >= 45670 and i < 45680:
            reset = 0
        elif i >= 45680 and i < 45690:
            reset = 1 if (i % 149 == 0) else 0
        elif i >= 45690 and i < 45700:
            reset = 0
        elif i >= 45700 and i < 45710:
            reset = 1 if (i % 151 == 0) else 0
        elif i >= 45710 and i < 45720:
            reset = 0
        elif i >= 45720 and i < 45730:
            reset = 1 if (i % 157 == 0) else 0
        elif i >= 45730 and i < 45740:
            reset = 0
        elif i >= 45740 and i < 45750:
            reset = 1 if (i % 163 == 0) else 0
        elif i >= 45750 and i < 45760:
            reset = 0
        elif i >= 45760 and i < 45770:
            reset = 1 if (i % 167 == 0) else 0
        elif i >= 45770 and i < 45780:
            reset = 0
        elif i >= 45780 and i < 45790:
            reset = 1 if (i % 173 == 0) else 0
        elif i >= 45790 and i < 45800:
            reset = 0
        elif i >= 45800 and i < 45810:
            reset = 1 if (i % 179 == 0) else 0
        elif i >= 45810 and i < 45820:
            reset = 0
        elif i >= 45820 and i < 45830:
            reset = 1 if (i % 181 == 0) else 0
        elif i >= 45830 and i < 45840:
            reset = 0
        elif i >= 45840 and i < 45850:
            reset = 1 if (i % 191 == 0) else 0
        elif i >= 45850 and i < 45860:
            reset = 0
        elif i >= 45860 and i < 45870:
            reset = 1 if (i % 193 == 0) else 0
        elif i >= 45870 and i < 45880:
            reset = 0
        elif i >= 45880 and i < 45890:
            reset = 1 if (i % 197 == 0) else 0
        elif i >= 45890 and i < 45900:
            reset = 0
        elif i >= 45900 and i < 45910:
            reset = 1 if (i % 199 == 0) else 0
        elif i >= 45910 and i < 45920:
            reset = 0
        elif i >= 45920 and i < 45930:
            reset = 1 if (i % 211 == 0) else 0
        elif i >= 45930 and i < 45940:
            reset = 0
        elif i >= 45940 and i < 45950:
            reset = 1 if (i % 223 == 0) else 0
        elif i >= 45950 and i < 45960:
            reset = 0
        elif i >= 45960 and i < 45970:
            reset = 1 if (i % 227 == 0) else 0
        elif i >= 45970 and i < 45980:
            reset = 0
        elif i >= 45980 and i < 45990:
            reset = 1 if (i % 229 == 0) else 0
        elif i >= 45990 and i < 46000:
            reset = 0
        elif i >= 46000 and i < 46010:
            reset = 1 if (i % 233 == 0) else 0
        elif i >= 46010 and i < 46020:
            reset = 0
        elif i >= 46020 and i < 46030:
            reset = 1 if (i % 239 == 0) else 0
        elif i >= 46030 and i < 46040:
            reset = 0
        elif i >= 46040 and i < 46050:
            reset = 1 if (i % 241 == 0) else 0
        elif i >= 46050 and i < 46060:
            reset = 0
        elif i >= 46060 and i < 46070:
            reset = 1 if (i % 251 == 0) else 0
        elif i >= 46070 and i < 46080:
            reset = 0
        elif i >= 46080 and i < 46090:
            reset = 1 if (i % 257 == 0) else 0
        elif i >= 46090 and i < 46100:
            reset = 0
        elif i >= 46100 and i < 46110:
            reset = 1 if (i % 263 == 0) else 0
        elif i >= 46110 and i < 46120:
            reset = 0
        elif i >= 46120 and i < 46130:
            reset = 1 if (i % 269 == 0) else 0
        elif i >= 46130 and i < 46140:
            reset = 0
        elif i >= 46140 and i < 46150:
            reset = 1 if (i % 271 == 0) else 0
        elif i >= 46150 and i < 46160:
            reset = 0
        elif i >= 46160 and i < 46170:
            reset = 1 if (i % 277 == 0) else 0
        elif i >= 46170 and i < 46180:
            reset = 0
        elif i >= 46180 and i < 46190:
            reset = 1 if (i % 281 == 0) else 0
        elif i >= 46190 and i < 46200:
            reset = 0
        elif i >= 46200 and i < 46210:
            reset = 1 if (i % 283 == 0) else 0
        elif i >= 46210 and i < 46220:
            reset = 0
        elif i >= 46220 and i < 46230:
            reset = 1 if (i % 293 == 0) else 0
        elif i >= 46230 and i < 46240:
            reset = 0
        elif i >= 46240 and i < 46250:
            reset = 1 if (i % 307 == 0) else 0
        elif i >= 46250 and i < 46260:
            reset = 0
        elif i >= 46260 and i < 46270:
            reset = 1 if (i % 311 == 0) else 0
        elif i >= 46270 and i < 46280:
            reset = 0
        elif i >= 46280 and i < 46290:
            reset = 1 if (i % 313 == 0) else 0
        elif i >= 46290 and i < 46300:
            reset = 0
        elif i >= 46300 and i < 46310:
            reset = 1 if (i % 317 == 0) else 0
        elif i >= 46310 and i < 46320:
            reset = 0
        elif i >= 46320 and i < 46330:
            reset = 1 if (i % 331 == 0) else 0
        elif i >= 46330 and i < 46340:
            reset = 0
        elif i >= 46340 and i < 46350:
            reset = 1 if (i % 337 == 0) else 0
        elif i >= 46350 and i < 46360:
            reset = 0
        elif i >= 46360 and i < 46370:
            reset = 1 if (i % 347 == 0) else 0
        elif i >= 46370 and i < 46380:
            reset = 0
        elif i >= 46380 and i < 46390:
            reset = 1 if (i % 349 == 0) else 0
        elif i >= 46390 and i < 46400:
            reset = 0
        elif i >= 46400 and i < 46410:
            reset = 1 if (i % 353 == 0) else 0
        elif i >= 46410 and i < 46420:
            reset = 0
        elif i >= 46420 and i < 46430:
            reset = 1 if (i % 359 == 0) else 0
        elif i >= 46430 and i < 46440:
            reset = 0
        elif i >= 46440 and i < 46450:
            reset = 1 if (i % 367 == 0) else 0
        elif i >= 46450 and i < 46460:
            reset = 0
        elif i >= 46460 and i < 46470:
            reset = 1 if (i % 373 == 0) else 0
        elif i >= 46470 and i < 46480:
            reset = 0
        elif i >= 46480 and i < 46490:
            reset = 1 if (i % 379 == 0) else 0
        elif i >= 46490 and i < 46500:
            reset = 0
        elif i >= 46500 and i < 46510:
            reset = 1 if (i % 383 == 0) else 0
        elif i >= 46510 and i < 46520:
            reset = 0
        elif i >= 46520 and i < 46530:
            reset = 1 if (i % 389 == 0) else 0
        elif i >= 46530 and i < 46540:
            reset = 0
        elif i >= 46540 and i < 46550:
            reset = 1 if (i % 397 == 0) else 0
        elif i >= 46550 and i < 46560:
            reset = 0
        elif i >= 46560 and i < 46570:
            reset = 1 if (i % 401 == 0) else 0
        elif i >= 46570 and i < 46580:
            reset = 0
        elif i >= 46580 and i < 46590:
            reset = 1 if (i % 409 == 0) else 0
        elif i >= 46590 and i < 46600:
            reset = 0
        elif i >= 46600 and i < 46610:
            reset = 1 if (i % 419 == 0) else 0
        elif i >= 46610 and i < 46620:
            reset = 0
        elif i >= 46620 and i < 46630:
            reset = 1 if (i % 421 == 0) else 0
        elif i >= 46630 and i < 46640:
            reset = 0
        elif i >= 46640 and i < 46650:
            reset = 1 if (i % 431 == 0) else 0
        elif i >= 46650 and i < 46660:
            reset = 0
        elif i >= 46660 and i < 46670:
            reset = 1 if (i % 433 == 0) else 0
        elif i >= 46670 and i < 46680:
            reset = 0
        elif i >= 46680 and i < 46690:
            reset = 1 if (i % 439 == 0) else 0
        elif i >= 46690 and i < 46700:
            reset = 0
        elif i >= 46700 and i < 46710:
            reset = 1 if (i % 443 == 0) else 0
        elif i >= 46710 and i < 46720:
            reset = 0
        elif i >= 46720 and i < 46730:
            reset = 1 if (i % 449 == 0) else 0
        elif i >= 46730 and i < 46740:
            reset = 0
        elif i >= 46740 and i < 46750:
            reset = 1 if (i % 457 == 0) else 0
        elif i >= 46750 and i < 46760:
            reset = 0
        elif i >= 46760 and i < 46770:
            reset = 1 if (i % 461 == 0) else 0
        elif i >= 46770 and i < 46780:
            reset = 0
        elif i >= 46780 and i < 46790:
            reset = 1 if (i % 463 == 0) else 0
        elif i >= 46790 and i < 46800:
            reset = 0
        elif i >= 46800 and i < 46810:
            reset = 1 if (i % 467 == 0) else 0
        elif i >= 46810 and i < 46820:
            reset = 0
        elif i >= 46820 and i < 46830:
            reset = 1 if (i % 479 == 0) else 0
        elif i >= 46830 and i < 46840:
            reset = 0
        elif i >= 46840 and i < 46850:
            reset = 1 if (i % 487 == 0) else 0
        elif i >= 46850 and i < 46860:
            reset = 0
        elif i >= 46860 and i < 46870:
            reset = 1 if (i % 491 == 0) else 0
        elif i >= 46870 and i < 46880:
            reset = 0
        elif i >= 46880 and i < 46890:
            reset = 1 if (i % 499 == 0) else 0
        elif i >= 46890 and i < 46900:
            reset = 0
        elif i >= 46900 and i < 46910:
            reset = 1 if (i % 503 == 0) else 0
        elif i >= 46910 and i < 46920:
            reset = 0
        elif i >= 46920 and i < 46930:
            reset = 1 if (i % 509 == 0) else 0
        elif i >= 46930 and i < 46940:
            reset = 0
        elif i >= 46940 and i < 46950:
            reset = 1 if (i % 521 == 0) else 0
        elif i >= 46950 and i < 46960:
            reset = 0
        elif i >= 46960 and i < 46970:
            reset = 1 if (i % 523 == 0) else 0
        elif i >= 46970 and i < 46980:
            reset = 0
        elif i >= 46980 and i < 46990:
            reset = 1 if (i % 541 == 0) else 0
        elif i >= 46990 and i < 47000:
            reset = 0
        elif i >= 47000 and i < 47010:
            reset = 1 if (i % 547 == 0) else 0
        elif i >= 47010 and i < 47020:
            reset = 0
        elif i >= 47020 and i < 47030:
            reset = 1 if (i % 557 == 0) else 0
        elif i >= 47030 and i < 47040:
            reset = 0
        elif i >= 47040 and i < 47050:
            reset = 1 if (i % 563 == 0) else 0
        elif i >= 47050 and i < 47060:
            reset = 0
        elif i >= 47060 and i < 47070:
            reset = 1 if (i % 569 == 0) else 0
        elif i >= 47070 and i < 47080:
            reset = 0
        elif i >= 47080 and i < 47090:
            reset = 1 if (i % 571 == 0) else 0
        elif i >= 47090 and i < 47100:
            reset = 0
        elif i >= 47100 and i < 47110:
            reset = 1 if (i % 577 == 0) else 0
        elif i >= 47110 and i < 47120:
            reset = 0
        elif i >= 47120 and i < 47130:
            reset = 1 if (i % 587 == 0) else 0
        elif i >= 47130 and i < 47140:
            reset = 0
        elif i >= 47140 and i < 47150:
            reset = 1 if (i % 593 == 0) else 0
        elif i >= 47150 and i < 47160:
            reset = 0
        elif i >= 47160 and i < 47170:
            reset = 1 if (i % 599 == 0) else 0
        elif i >= 47170 and i < 47180:
            reset = 0
        elif i >= 47180 and i < 47190:
            reset = 1 if (i % 601 == 0) else 0
        elif i >= 47190 and i < 47200:
            reset = 0
        elif i >= 47200 and i < 47210:
            reset = 1 if (i % 607 == 0) else 0
        elif i >= 47210 and i < 47220:
            reset = 0
        elif i >= 47220 and i < 47230:
            reset = 1 if (i % 613 == 0) else 0
        elif i >= 47230 and i < 47240:
            reset = 0
        elif i >= 47240 and i < 47250:
            reset = 1 if (i % 617 == 0) else 0
        elif i >= 47250 and i < 47260:
            reset = 0
        elif i >= 47260 and i < 47270:
            reset = 1 if (i % 619 == 0) else 0
        elif i >= 47270 and i < 47280:
            reset = 0
        elif i >= 47280 and i < 47290:
            reset = 1 if (i % 631 == 0) else 0
        elif i >= 47290 and i < 47300:
            reset = 0
        elif i >= 47300 and i < 47310:
            reset = 1 if (i % 641 == 0) else 0
        elif i >= 47310 and i < 47320:
            reset = 0
        elif i >= 47320 and i < 47330:
            reset = 1 if (i % 643 == 0) else 0
        elif i >= 47330 and i < 47340:
            reset = 0
        elif i >= 47340 and i < 47350:
            reset = 1 if (i % 647 == 0) else 0
        elif i >= 47350 and i < 47360:
            reset = 0
        elif i >= 47360 and i < 47370:
            reset = 1 if (i % 653 == 0) else 0
        elif i >= 47370 and i < 47380:
            reset = 0
        elif i >= 47380 and i < 47390:
            reset = 1 if (i % 659 == 0) else 0
        elif i >= 47390 and i < 47400:
            reset = 0
        elif i >= 47400 and i < 47410:
            reset = 1 if (i % 661 == 0) else 0
        elif i >= 47410 and i < 47420:
            reset = 0
        elif i >= 47420 and i < 47430:
            reset = 1 if (i % 673 == 0) else 0
        elif i >= 47430 and i < 47440:
            reset = 0
        elif i >= 47440 and i < 47450:
            reset = 1 if (i % 677 == 0) else 0
        elif i >= 47450 and i < 47460:
            reset = 0
        elif i >= 47460 and i < 47470:
            reset = 1 if (i % 683 == 0) else 0
        elif i >= 47470 and i < 47480:
            reset = 0
        elif i >= 47480 and i < 47490:
            reset = 1 if (i % 691 == 0) else 0
        elif i >= 47490 and i < 47500:
            reset = 0
        elif i >= 47500 and i < 47510:
            reset = 1 if (i % 701 == 0) else 0
        elif i >= 47510 and i < 47520:
            reset = 0
        elif i >= 47520 and i < 47530:
            reset = 1 if (i % 709 == 0) else 0
        elif i >= 47530 and i < 47540:
            reset = 0
        elif i >= 47540 and i < 47550:
            reset = 1 if (i % 719 == 0) else 0
        elif i >= 47550 and i < 47560:
            reset = 0
        elif i >= 47560 and i < 47570:
            reset = 1 if (i % 727 == 0) else 0
        elif i >= 47570 and i < 47580:
            reset = 0
        elif i >= 47580 and i < 47590:
            reset = 1 if (i % 733 == 0) else 0
        elif i >= 47590 and i < 47600:
            reset = 0
        elif i >= 47600 and i < 47610:
            reset = 1 if (i % 739 == 0) else 0
        elif i >= 47610 and i < 47620:
            reset = 0
        elif i >= 47620 and i < 47630:
            reset = 1 if (i % 743 == 0) else 0
        elif i >= 47630 and i < 47640:
            reset = 0
        elif i >= 47640 and i < 47650:
            reset = 1 if (i % 751 == 0) else 0
        elif i >= 47650 and i < 47660:
            reset = 0
        elif i >= 47660 and i < 47670:
            reset = 1 if (i % 757 == 0) else 0
        elif i >= 47670 and i < 47680:
            reset = 0
        elif i >= 47680 and i < 47690:
            reset = 1 if (i % 761 == 0) else 0
        elif i >= 47690 and i < 47700:
            reset = 0
        elif i >= 47700 and i < 47710:
            reset = 1 if (i % 769 == 0) else 0
        elif i >= 47710 and i < 47720:
            reset = 0
        elif i >= 47720 and i < 47730:
            reset = 1 if (i % 773 == 0) else 0
        elif i >= 47730 and i < 47740:
            reset = 0
        elif i >= 47740 and i < 47750:
            reset = 1 if (i % 787 == 0) else 0
        elif i >= 47750 and i < 47760:
            reset = 0
        elif i >= 47760 and i < 47770:
            reset = 1 if (i % 797 == 0) else 0
        elif i >= 47770 and i < 47780:
            reset = 0
        elif i >= 47780 and i < 47790:
            reset = 1 if (i % 809 == 0) else 0
        elif i >= 47790 and i < 47800:
            reset = 0
        elif i >= 47800 and i < 47810:
            reset = 1 if (i % 811 == 0) else 0
        elif i >= 47810 and i < 47820:
            reset = 0
        elif i >= 47820 and i < 47830:
            reset = 1 if (i % 821 == 0) else 0
        elif i >= 47830 and i < 47840:
            reset = 0
        elif i >= 47840 and i < 47850:
            reset = 1 if (i % 823 == 0) else 0
        elif i >= 47850 and i < 47860:
            reset = 0
        elif i >= 47860 and i < 47870:
            reset = 1 if (i % 827 == 0) else 0
        elif i >= 47870 and i < 47880:
            reset = 0
        elif i >= 47880 and i < 47890:
            reset = 1 if (i % 829 == 0) else 0
        elif i >= 47890 and i < 47900:
            reset = 0
        elif i >= 47900 and i < 47910:
            reset = 1 if (i % 839 == 0) else 0
        elif i >= 47910 and i < 47920:
            reset = 0
        elif i >= 47920 and i < 47930:
            reset = 1 if (i % 853 == 0) else 0
        elif i >= 47930 and i < 47940:
            reset = 0
        elif i >= 47940 and i < 47950:
            reset = 1 if (i % 857 == 0) else 0
        elif i >= 47950 and i < 47960:
            reset = 0
        elif i >= 47960 and i < 47970:
            reset = 1 if (i % 859 == 0) else 0
        elif i >= 47970 and i < 47980:
            reset = 0
        elif i >= 47980 and i < 47990:
            reset = 1 if (i % 863 == 0) else 0
        elif i >= 47990 and i < 48000:
            reset = 0
        elif i >= 48000 and i < 48010:
            reset = 1 if (i % 877 == 0) else 0
        elif i >= 48010 and i < 48020:
            reset = 0
        elif i >= 48020 and i < 48030:
            reset = 1 if (i % 881 == 0) else 0
        elif i >= 48030 and i < 48040:
            reset = 0
        elif i >= 48040 and i < 48050:
            reset = 1 if (i % 883 == 0) else 0
        elif i >= 48050 and i < 48060:
            reset = 0
        elif i >= 48060 and i < 48070:
            reset = 1 if (i % 887 == 0) else 0
        elif i >= 48070 and i < 48080:
            reset = 0
        elif i >= 48080 and i < 48090:
            reset = 1 if (i % 907 == 0) else 0
        elif i >= 48090 and i < 48100:
            reset = 0
        elif i >= 48100 and i < 48110:
            reset = 1 if (i % 911 == 0) else 0
        elif i >= 48110 and i < 48120:
            reset = 0
        elif i >= 48120 and i < 48130:
            reset = 1 if (i % 919 == 0) else 0
        elif i >= 48130 and i < 48140:
            reset = 0
        elif i >= 48140 and i < 48150:
            reset = 1 if (i % 929 == 0) else 0
        elif i >= 48150 and i < 48160:
            reset = 0
        elif i >= 48160 and i < 48170:
            reset = 1 if (i % 937 == 0) else 0
        elif i >= 48170 and i < 48180:
            reset = 0
        elif i >= 48180 and i < 48190:
            reset = 1 if (i % 941 == 0) else 0
        elif i >= 48190 and i < 48200:
            reset = 0
        elif i >= 48200 and i < 48210:
            reset = 1 if (i % 947 == 0) else 0
        elif i >= 48210 and i < 48220:
            reset = 0
        elif i >= 48220 and i < 48230:
            reset = 1 if (i % 953 == 0) else 0
        elif i >= 48230 and i < 48240:
            reset = 0
        elif i >= 48240 and i < 48250:
            reset = 1 if (i % 967 == 0) else 0
        elif i >= 48250 and i < 48260:
            reset = 0
        elif i >= 48260 and i < 48270:
            reset = 1 if (i % 971 == 0) else 0
        elif i >= 48270 and i < 48280:
            reset = 0
        elif i >= 48280 and i < 48290:
            reset = 1 if (i % 977 == 0) else 0
        elif i >= 48290 and i < 48300:
            reset = 0
        elif i >= 48300 and i < 48310:
            reset = 1 if (i % 983 == 0) else 0
        elif i >= 48310 and i < 48320:
            reset = 0
        elif i >= 48320 and i < 48330:
            reset = 1 if (i % 991 == 0) else 0
        elif i >= 48330 and i < 48340:
            reset = 0
        elif i >= 48340 and i < 48350:
            reset = 1 if (i % 997 == 0) else 0
        elif i >= 48350:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
    return rows
