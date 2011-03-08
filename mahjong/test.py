#!/usr/bin/env python3

from mahjong.tiles import *
from mahjong.scoring import *

def test():
    # 2000/4000, menzen tsumo, itsu, dora, dora
    print('2000/4000, menzen tsumo, itsu, dora, dora')
    a = [M1(), M2(), M3()]
    b = [M4(), M5(), M6()]
    c = [M7(), M8(), M9()]
    d = [P1(), P1(), P1()]
    d[2].last = 1
    d[2].tsumo = 1
    e = [S6(), S6()]
    s, y = score(0, ['S', 'E'], a, b, c, d, e, dora=[S5()], ura=[P7()])
    print(s)
    print(y)

    # 2900, fanpai, dora
    print('2900, fanpai, dora')
    a = [M4(), M5(), M6()]
    b = [P7(), P8(), P9()]
    c = [R(), R(), R()]
    for tile in c:
        tile.pon = 1
    d = [S6(), S7(), S8()]
    d[1].last = 1
    d[1].ron = 1
    e = [S1(), S1()]
    s, y = score(1, ['E', 'E'], a, b, c, d, e, dora=[S7()], ura=[S9()])
    print(s)
    print(y)
     
    # 2400, chi toitsu
    print('2400, chi toitsu')
    a = [S1(), S1()]
    b = [S2(), S2()]
    c = [S7(), S7()]
    c[1].last = 1
    c[1].ron = 1
    d = [M2(), M2()]
    e = [M3(), M3()]
    f = [P7(), P7()]
    g = [R(), R()]
    s, y = score(1, ['E', 'E'], a, b, c, d, e, f, g, dora=[S8()])
    print(s)
    print(y)

    # 1300, tanyao
    print('1300, tanyao')
    a = [S2(), S3(), S4()]
    b = [M2(), M3(), M4()]
    c = [M5(), M6(), M7()]
    d = [P6(), P7(), P8()]
    e = [M8(), M8()]
    e[0].last = 1
    e[0].ron = 1
    s, y = score(0, ['W', 'E'], a, b, c, d, e)
    print(s)
    print(y)

if __name__=="__main__":
    test()
