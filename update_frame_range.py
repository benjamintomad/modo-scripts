#python
#----------------------------------------------------------
# 2013-10-23 Add Edit
#----------------------------------------------------------

import os
 
#Get the path
a = lx.args()
seq = a[0]
shot = a[1]
path = "w:\\LAIGB\\Episodes\\%s\\%s\\Data\\" % (seq,shot)
filename = "%s_%s_FrameRange.txt" % (seq.replace(seq[:1],''), shot.replace(shot[:1],''))
txtfile = path + filename

lx.out(txtfile)

# Read the txt file with frame range
i = open(txtfile, "r")
lx.out(i)
array = []
for line in i:
    array.append( line )
    lx.out(line)
i.close()

# set the first and last frames
first=array[0]
lx.out(first)

last=array[1]
lx.out(last)

# Change frame range
lx.eval('select.item Render')
lx.eval('item.channel first {%s}' % first)
lx.eval('item.channel last {%s}' % last)
