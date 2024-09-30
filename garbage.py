
def test_or():

    in_orarr =  (arr_0, arr_1,  arr_2,  arr_3, )
    ou_orarr =  (0, 1, 1, 1,)
    tin_orarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_orarr =  (0, 1, 1, 1,)

    nn = S2sNp(len(in_orarr), 1)
    nn.verbose = args.verbose

    for aa in range(len(in_orarr)):
        nn.memorize(in_orarr[aa], ou_orarr[aa])

    for cnt, aa in enumerate(tin_orarr):
        ttt = time.time()
        nn.recall(aa)
        print(nn.outputs, tou_orarr[cnt])
        assert nn.outputs == tou_orarr[cnt]
    #assert 0

def test_and():

    in_andarr =  (arr_0, arr_1,  arr_2,  arr_3,)
    ou_andarr =  (0, 0, 0, 1)
    tin_andarr =  ((0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_andarr =  (0, 0, 0, 1)

    nn = S2sNp(len(in_andarr), 1)
    for aa in range(len(in_andarr)):
        nn.memorize(in_andarr[aa], ou_andarr[aa])

    for cnt, aa in enumerate(tin_andarr):
        ttt = time.time()
        nn.recall(aa)
        print(nn.outputs, tou_andarr[cnt])
        assert nn.outputs == tou_andarr[cnt]
    #assert 0


