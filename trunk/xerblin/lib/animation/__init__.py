from words import (
    timeframe,
    cubicdelta,
    quadraticdelta,
    sinedelta,
    cosinedelta,
    attach,
    run,
    )


a_script = '''

 18 timeframe
 2.5 100 23 sinedelta 2.5 100 23 cosinedelta
 2.5 120 50 cubicdelta 2.5 100 40 cubicdelta
 mul mul mul
 over
 self "TheStackController" lookup "setGeometry" lookup
 attach run

'''

# 18 timeframe 2.5 120 50 cubicdelta 2.5 100 40 cubicdelta 2.5 100 23 sinedelta 2.5 100 23 cosinedelta mul mul mul over self "TheStackController" lookup "setGeometry" lookup attach run

'''
1.0 480 -480 cubicdelta 1.0 364 -364 cubicdelta mul
1.0 25 255 cubicdelta 1.0 30 290 cubicdelta mul
mul
18 timeframe
self "TheStackController" lookup "setGeometry" lookup
attach run
'''

# 0 0 280 320 "setGeometry" TheStackController meta drop

