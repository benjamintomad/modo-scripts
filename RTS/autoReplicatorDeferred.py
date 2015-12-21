# python
# telnet.listen 12357 true


from pyModo import pyModo as pym
import re
import lx
import modo

scene = modo.scene.current()

selectedDF = pym.Deferred_Mesh_ID_Selected()
pointSourceID = pym.Item_ID_Get("Replicator Point Source")
replicas = []


# create the base replica based on selectedDF selection
for df in selectedDF:
    assetName = pym.Item_Name_Get(df).split(' ')[0]
    assetName = "PRP_" + assetName.split('_')[0]
    pym.Replicator_Add_New()
    selectedReplicator = pym.Replicator_ID_Selected()[0]
    replicas.append(selectedReplicator)
    lx.eval('replicator.source {%s}' % df)
    lx.eval('replicator.particle %s' % pointSourceID)
    pym.Item_Name_Set(selectedReplicator, "Replica_%s" % assetName)



# create replicas for each group
groups = pym.Group_Locator_ID_All()
for group in groups:
    groupName = pym.Item_Name_Get(group)
    if re.match (assetName, groupName):
        groupID = pym.Item_ID_Get(groupName)
        for rep in replicas:
            pym.Item_Duplicate(rep)
            currentDupli = pym.Replicator_ID_Selected()[0]
            lx.eval("item.parent %s %s 0 inPlace:0" % (currentDupli, groupID))

# delete the base replica
for rep in replicas:
    pym.Item_Delete(rep)

