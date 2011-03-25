#!/usr/bin/env python3

import view

def test():
    x = view.View()
    x.bgblitter.blit()
    x.flip()
    input()

if __name__=='__main__':
    test()
