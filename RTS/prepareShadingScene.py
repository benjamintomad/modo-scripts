# python

from pyModo import pyModo as pym
import lx
import os




# define folder, version and character and set current scene
currentScene = pym.Scene_Current_Index_Get()
pym.Scene_Current_Set(currentScene)

path = pym.Scene_Name(currentScene)[0]

folder = '/home/ben/Documents/tests/modo/prepareShadingScene/renders/sha'

pathPart = path.split('_')
character = str(pathPart[0])
version = str(pathPart[-1].strip('.lxo'))

outputPath = str('%s/%s/modo/%s/' % (folder, character, version))
fullPath = outputPath + character
outputPathBake = str('%s/%s/modo/bake/%s/' % (folder, character, version))
fullPathBake = outputPathBake + character


def createRenderOutput():
    lx.eval('shader.create renderOutput')


def setRenderOutputPath():
    currentOutput = str(pym.Render_Output_Name_Selected()[0])

    if currentOutput == 'bake' or currentOutput == 'bakeAlpha':
        output = outputPathBake
        path = fullPathBake
    else:
        output = outputPath
        path = fullPath

    if os.path.exists(output):
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')
    else:
        os.makedirs(output)
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')


def createRNpasses():
    lx.eval('group.create RN_passes pass empty')


def configOCIO():
    ocioNames = pym.Scene_Get_Item_Names_All()
    for scn in ocioNames:
        if scn == 'Scene':
            pym.Item_Select(scn)
            pym.Item_Channel_Edit('ocioConfig', 'nuke-default')
            pym.Item_Channel_Edit('def8bitColorspace', 'nuke-default:sRGB')
            pym.Item_Channel_Edit('def16bitColorspace', 'nuke-default:linear')
            pym.Item_Channel_Edit('defFloatColorspace', 'nuke-default:linear')
    pym.Item_DeSelect()


def prepareItems():
    getI = pym.Scene_Get_Item_IDs_All()
    for it in getI:
        itemType = pym.Item_Type_Get(it)
        for t in itemType:
            if t == 'mesh' or t == 'locator':
                pym.Item_Select(it)
                pym.Item_Channel_Edit('visible', 'default')
                pym.Item_DeSelect()
            if t == 'mesh':
                lx.eval('select.Item %s add' % it)
    lx.eval('mesh.cleanup true')
    pym.Item_DeSelect()


def tagScene():
    tagNames = pym.Scene_Get_Item_Tags_All()
    itemNames = pym.Scene_Get_Item_Names_All()
    check = int(0)

    for i in itemNames:
        if i == 'GRP_%s' % character:
            id = pym.Item_ID_Get(i)

    for tag in tagNames:
        if tag == 'prep sha OK':
            check += 1
    if check == 0:
        pym.Item_Select(id)
        lx.eval('item.tagAdd CMMT')
        lx.eval('item.tag string CMMT "prep sha OK"')


def prepScene():
    # prepare items : visibility and cleanup
    prepareItems()

    # create bake group
    lx.eval('group.create bake_GRP std empty')

    # select the render item first
    render = pym.Render_ID_All()
    pym.Item_Select(render)

    # set the output pattern
    pym.Item_Channel_Edit('outPat', "_[<pass>]_[<output>]_<FFFF>")

    # delete default render outputs
    oldOutputs = pym.Render_Output_ID_All()
    for out in oldOutputs:
        pym.Item_Delete(out)

    # create render output sha group
    pym.Group_Add_New()
    currentShaGroup = str(pym.Group_ID_Selected()[0])
    pym.Item_Name_Set(currentShaGroup, 'Outputs_sha')

    # create bty output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'BTY')
    setRenderOutputPath()

    # create Z output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'Z')
    lx.eval('shader.setEffect depth')
    setRenderOutputPath()

    # create alpha output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'alpha')
    lx.eval('shader.setEffect shade.alpha')
    setRenderOutputPath()

    # create DIR output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'DIR')
    lx.eval('shader.setEffect shade.illumDir')
    setRenderOutputPath()

    # create SSS output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'SSS')
    lx.eval('shader.setEffect shade.subsurface')
    setRenderOutputPath()

    pym.Item_DeSelect()

    # create render output bake group
    pym.Group_Add_New()
    currentShaGroup = str(pym.Group_ID_Selected()[0])
    pym.Item_Name_Set(currentShaGroup, 'Outputs_bke')

    # create alpha bake output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'bakeAlpha')
    lx.eval('shader.setEffect shade.alpha')
    setRenderOutputPath()

    # create bty bake output
    createRenderOutput()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'bake')
    setRenderOutputPath()


    # set render ouputs colorspace to linear
    allOutputs = pym.Render_Output_ID_All()
    for out in allOutputs:
        pym.Item_Select(out)
        pym.Item_Channel_Edit('renderOutput$colorspace', 'nuke-default:linear')


    # create the render pass group and assign the outputs channels

    createRNpasses()
    allItems = pym.Scene_Get_Item_IDs_All()

    for i in allItems:
        itemName = pym.Item_Name_Get(i)
        if itemName == "RN_passes":
            passGroup = pym.Item_ID_Get(itemName)
            pym.Item_Select(passGroup)
            lx.eval('group.layer name:sha transfer:false grpType:pass')
            lx.eval('group.layer name:bke transfer:false grpType:pass')

        if itemName == 'Outputs_bke' or itemName == 'Outputs_sha':
            channelNames = pym.Item_Channel_Get_Names(i)

            for channel in channelNames:
                if channel == 'enable':
                    pym.Item_Channel_Select(i, channel)
                    lx.eval('group.edit add chan item:%s' % passGroup)





    # configure layer visibility for the outputs groups

    allItems = pym.Scene_Get_Item_IDs_All()

    # configure bake pass
    for i in allItems:
        name = pym.Item_Name_Get(i)
        if name == 'bke':
            pym.Item_Select(i)
            lx.eval('layer.enable enable:toggle')
            lx.eval('layer.active %s type:pass' % i)

    for output in allItems:
        outputName = pym.Item_Name_Get(output)
        if outputName == 'Outputs_sha':
            channelNames = pym.Item_Channel_Get_Names(output)
            for channel in channelNames:
                if channel == 'enable':
                    pym.Item_Channel_Edit(channel, 'enable')
            lx.eval('edit.apply')


    # configure sha pass

    # configure bake pass
    for i in allItems:
        name = pym.Item_Name_Get(i)
        if name == 'sha':
            pym.Item_Select(i)
            lx.eval('layer.active %s type:pass' % i)

    for output in allItems:
        outputName = pym.Item_Name_Get(output)
        if outputName == 'Outputs_bke':
            channelNames = pym.Item_Channel_Get_Names(output)
            for channel in channelNames:
                if channel == 'enable':
                    pym.Item_Channel_Edit(channel, 'enable')
            lx.eval('edit.apply')


    # set OCIO configuration
    configOCIO()


    # tag the scene
    tagScene()



# check if the scene has already been prepared, if not, start the preparation
tagNames = pym.Scene_Get_Item_Tags_All()
count = 0
lx.eval('dialog.msg "Scene already prepared"')

for t in tagNames:
    if t == 'prep sha OK':
        count += 1
        lx.eval('dialog.open')

if count == 0:
    prepScene()
