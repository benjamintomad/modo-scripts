# python

import sys
import re
import modo

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

sys.path.append(r'W:\RTS\People\Btomad\Scripting\modo-scripts\RTS')
import wtdPrepareShot as wtd
reload(wtd)


scene = modo.scene.current()

bkegrp = wtd.RenderOutputs('Outputs_bake').bake()