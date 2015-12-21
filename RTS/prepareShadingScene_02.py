# python

from pyModo import pyModo as pym
import lx
import os
import re
import modo
import tank

scene = modo.scene.current()
tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']


# define folder, version and character and set current scene
currentScene = modo.Scene()
pym.Scene_Current_Set(currentScene)

path = pym.Scene_Name(currentScene)[0]

folder = 'W:\\RTS\\Renders\\_Library\\sha\\Character'

pathPart = path.split('_')
asset = str(pathPart[0])

version = str(pathPart[-1].strip('.lxo'))

outputPath = str('%s\\%s\\work\\modo\\%s\\' % (folder, asset, version))
fullPath = outputPath + asset

outputPathBake = str('%s\\%s\\work\\modo\\bake\\%s\\' % (folder, asset, version))
fullPathBake = outputPathBake + asset

# identify the asset type
fileScenePath = pym.Scene_FilePath(currentScene)[0]
lx.out(fileScenePath)
if re.search('Character', fileScenePath):
    assetType = 'character'
if re.search('Prop', fileScenePath):
    assetType = 'prop'


def create_render_output():
    lx.eval('shader.create renderOutput')


def set_render_output_path():
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


def set_resolution():
    render = pym.Render_ID_All()
    pym.Item_Select(render)
    pym.Item_Channel_Set_Value("bakeX", 512)
    pym.Item_Channel_Set_Value("bakeY", 512)
    pym.Item_Channel_Set_Value("first", 0)
    pym.Item_Channel_Set_Value("last", 119)
    lx.eval('time.range scene out:4.9583')
    lx.eval('time.range current out:4.9583')
    lx.eval('time.range scene 0.0')
    lx.eval('time.range current 0.0')
    lx.eval("render.res 0 1724")
    lx.eval("render.res 1 936")


def create_render_passes_characters():
    lx.eval('group.create RN_passes pass empty')


def config_OCIO():
    ocioNames = pym.Scene_Get_Item_Names_All()
    for scn in ocioNames:
        if scn == 'Scene':
            pym.Item_Select(scn)
            pym.Item_Channel_Set_Value('ocioConfig', 'nuke-default')
            pym.Item_Channel_Set_Value('def8bitColorspace', 'nuke-default:sRGB')
            pym.Item_Channel_Set_Value('def16bitColorspace', 'nuke-default:sRGB')
            pym.Item_Channel_Set_Value('defFloatColorspace', 'nuke-default:linear')
    pym.Item_DeSelect()


def prepare_items():
    getI = pym.Scene_Get_Item_IDs_All()
    for it in getI:
        itemType = pym.Item_Type_Get(it)
        for t in itemType:
            if t == 'mesh' or t == 'locator':
                pym.Item_Select(it)
                pym.Item_Channel_Set_Value('visible', 'default')
                pym.Item_DeSelect()
            if t == 'mesh':
                lx.eval('select.Item %s add' % it)
    # lx.eval('mesh.cleanup true')
    pym.Item_DeSelect()


def tag_scene_characters():
    tagNames = pym.Scene_Get_Item_Tags_All()
    itemNames = pym.Scene_Get_Item_Names_All()
    check = int(0)

    for i in itemNames:
        if i == 'GRP_%s' % asset:
            id = pym.Item_ID_Get(i)

    for tag in tagNames:
        if tag == 'prep sha OK':
            check += 1
    if check == 0:
        pym.Item_Select(id)
        lx.eval('item.tagAdd CMMT')
        lx.eval('item.tag string CMMT "prep sha OK"')


def create_cameras():
    defaultCam = pym.Camera_ID_All()
    pym.Item_Name_Set(defaultCam, 'Camera_RN')
    pym.Item_Duplicate(defaultCam)
    newCam = pym.Item_ID_Get("Camera_RN (2)")
    pym.Item_Name_Set(newCam, 'Camera_CU')


def assign_cameras_to_passes():
    pym.Item_DeSelect()

    # get the id of the render cameras
    allCams = pym.Camera_ID_All()
    for cam in allCams:
        pym.Item_Select(cam)
        camName = pym.Camera_Name_Selected()[0]
        lx.out(camName)
        if camName == 'Camera_RN':
            cameraRN = pym.Camera_ID_Selected()[0]
        if camName == 'Camera_CU':
            cameraCU = pym.Camera_ID_Selected()[0]

    # get the id of the pass group
    allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
        itemName = pym.Item_Name_Get(i)
        if itemName == "RN_passes":
            passGroup = pym.Item_ID_Get(itemName)
            lx.out(passGroup)
            pym.Item_Select(passGroup)

    # add the render camera channel to the pass group
    render = pym.Render_ID_All()
    pym.Item_Channel_Select(render, 'cameraIndex')
    lx.eval('group.edit add chan item:%s' % passGroup)


    pym.Item_DeSelect()

    # assign the camera to the corresponding pass
    # allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
            name = pym.Item_Name_Get(i)
            if name == 'sha_CU':
                pym.Item_Select(i)
                lx.eval('layer.active %s type:pass' % i)
                lx.eval('render.camera %s' % cameraCU)
                lx.eval('edit.apply')
            if name == 'sha':
                pym.Item_Select(i)
                lx.eval('layer.active %s type:pass' % i)
                lx.eval('render.camera %s' % cameraRN)
                lx.eval('edit.apply')


def freeze_xform_clean_pivots():
    allMeshes = pym.Mesh_ID_All()
    for mesh in allMeshes:
        pym.Item_Select(mesh)
        lx.eval ('transform.freeze')
    allItems = pym.Scene_Get_Item_IDs_All()
    for item in allItems:
        name = pym.Item_Name_Get(item)
        if re.search("Pivot", name):
            pym.Item_Delete(item)


def prep_scene_characters():
    # prepare items : visibility and cleanup
    prepare_items()
    freeze_xform_clean_pivots()

    # change bake resolution to 512
    set_resolution()

    # create cameras
    allCams = pym.Camera_Name_All()
    for cam in allCams:
        if re.search("Camera_RN", cam):
            lx.out('camera exists')
        else:
            create_cameras()

    # delete existing pass groups
    lx.eval("select.itemPattern RN_passes")
    pym.Item_Delete(pym.Group_ID_Selected())

    # create bake group
    # lx.eval('group.create bake_GRP std empty')

    # select the render item first
    render = pym.Render_ID_All()
    pym.Item_Select(render)

    # set the output pattern
    pym.Item_Channel_Set_Value('outPat', "_[<pass>]_[<output>]_<FFFF>")

    # delete default render outputs
    oldOutputs = pym.Render_Output_ID_All()
    for out in oldOutputs:
        pym.Item_Delete(out)

    # delete existing output groups
    lx.eval("select.itemPattern Outputs_sha")
    pym.Item_Delete(pym.Group_ID_Selected())
    lx.eval("select.itemPattern Outputs_bke")
    pym.Item_Delete(pym.Group_ID_Selected())

    # create render output sha group
    pym.Group_Add_New()
    currentShaGroup = str(pym.Group_ID_Selected()[0])
    pym.Item_Name_Set(currentShaGroup, 'Outputs_sha')

    # create bty output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'BTY')
    set_render_output_path()

    # create lng output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'LNG')
    lx.eval('shader.setEffect driver.a')
    set_render_output_path()

    # create Z output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'Z')
    lx.eval('shader.setEffect depth')
    set_render_output_path()

    # create alpha output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'alpha')
    lx.eval('shader.setEffect shade.alpha')
    set_render_output_path()

    # create DIR output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'DIR')
    lx.eval('shader.setEffect shade.illumDir')
    set_render_output_path()

    # create SSS output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'SSS')
    lx.eval('shader.setEffect shade.subsurface')
    set_render_output_path()

    # create SPC output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'SPC')
    lx.eval('shader.setEffect shade.specular')
    set_render_output_path()

    pym.Item_DeSelect()

    # create render output bake group
    pym.Group_Add_New()
    currentShaGroup = str(pym.Group_ID_Selected()[0])
    pym.Item_Name_Set(currentShaGroup, 'Outputs_bke')

    # create alpha bake output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'bakeAlpha')
    lx.eval('shader.setEffect shade.alpha')
    set_render_output_path()

    # create bty bake output
    create_render_output()
    currentOutput = pym.Render_Output_ID_Selected()
    pym.Item_Name_Set(currentOutput, 'bake')
    set_render_output_path()


    # set render ouputs colorspace to default
    allOutputs = pym.Render_Output_ID_All()
    for out in allOutputs:
        pym.Item_Select(out)
        pym.Item_Channel_Set_Value('renderOutput$colorspace', 'auto')


    # create the render pass group and assign the outputs channels

    create_render_passes_characters()
    allItems = pym.Scene_Get_Item_IDs_All()

    for i in allItems:
        itemName = pym.Item_Name_Get(i)
        if itemName == "RN_passes":
            passGroup = pym.Item_ID_Get(itemName)
            pym.Item_Select(passGroup)
            lx.eval('group.layer name:sha transfer:false grpType:pass')
            lx.eval('group.layer name:sha_CU transfer:false grpType:pass')
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
                    pym.Item_Channel_Set_Value(channel, 'enable')
            lx.eval('edit.apply')


    # configure shading pass
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
                    pym.Item_Channel_Set_Value(channel, 'enable')
            lx.eval('edit.apply')



    for i in allItems:
        name = pym.Item_Name_Get(i)
        if name == 'sha_CU':
            pym.Item_Select(i)
            lx.eval('layer.active %s type:pass' % i)

    for output in allItems:
        outputName = pym.Item_Name_Get(output)
        if outputName == 'Outputs_bke':
            channelNames = pym.Item_Channel_Get_Names(output)
            for channel in channelNames:
                if channel == 'enable':
                    pym.Item_Channel_Set_Value(channel, 'enable')
            lx.eval('edit.apply')

    # create the camera switch for the render passes
    assign_cameras_to_passes()

    # set OCIO configuration
    config_OCIO()


    # tag the scene
    # _tag_scene_characters()


def prep_scene_prop():
    config_OCIO()
    prepare_items()
    set_resolution()
    freeze_xform_clean_pivots()





# check if the scene has already been prepared, if not, start the preparation
tagNames = pym.Scene_Get_Item_Tags_All()
count = 0
lx.eval('dialog.msg "Scene already prepared"')

for t in tagNames:
    if t == 'prep sha OK':
        count += 1
        lx.eval('dialog.open')

if count == 0 and assetType == 'character':
    prep_scene_characters()

if assetType == 'prop':
    prep_scene_prop()
