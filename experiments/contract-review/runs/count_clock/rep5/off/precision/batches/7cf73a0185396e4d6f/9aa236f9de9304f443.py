def reference(vectors):
    ss_ones=0; ss_tens=0; mm_ones=0; mm_tens=0; hh_ones=2; hh_tens=1; pm=0
    out=[]
    for v in vectors:
        reset=v.get('reset',0); ena=v.get('ena',0)
        if reset:
            ss_ones=0; ss_tens=0; mm_ones=0; mm_tens=0; hh_ones=2; hh_tens=1; pm=0
        elif ena:
            if ss_ones==9:
                ss_ones=0
                if ss_tens==5:
                    ss_tens=0
                    if mm_ones==9:
                        mm_ones=0
                        if mm_tens==5:
                            mm_tens=0
                            if hh_tens==1 and hh_ones==2:
                                hh_tens=0; hh_ones=1; pm=1-pm
                            elif hh_ones==9:
                                hh_ones=0; hh_tens=1
                            else:
                                hh_ones+=1
                        else:
                            mm_tens+=1
                    else:
                        mm_ones+=1
                else:
                    ss_tens+=1
            else:
                ss_ones+=1
        out.append({'pm':pm,'hh':(hh_tens<<4)|hh_ones,'mm':(mm_tens<<4)|mm_ones,'ss':(ss_tens<<4)|ss_ones})
    return out
