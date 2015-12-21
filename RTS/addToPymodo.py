__author__ = 'btomad'

from pyModo import pyModo as pym



def Render_Pass_ID_All():
    strItemType = 'Action Clip'
    asVariant = 'all'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Render_Pass_ID_Selected():
    strItemType = 'Action Clip'
    asVariant = 'selected'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Render_Pass_ID_UnSelected():
    strItemType = 'Action Clip'
    asVariant = 'unselected'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Render_Pass_Name_All():
    strItemType = 'Action Clip'
    asVariant = 'all'
    return __fn_pyModo_Item_Name(strItemType, asVariant)

def Render_Pass_Name_Selected():
    strItemType = 'Action Clip'
    asVariant = 'selected'
    return __fn_pyModo_Item_Name(strItemType, asVariant)

def Render_Pass_Name_UnSelected():
    strItemType = 'Action Clip'
    asVariant = 'unselected'
    return __fn_pyModo_Item_Name(strItemType, asVariant)

def Deferred_Mesh_ID_All():
    strItemType = 'Deferred Mesh'
    asVariant = 'all'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Deferred_Mesh_ID_Selected():
    strItemType = 'Deferred Mesh'
    asVariant = 'selected'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Deferred_Mesh_ID_UnSelected():
    strItemType = 'Deferred Mesh'
    asVariant = 'unselected'
    return __fn_pyModo_Item_ID(strItemType, asVariant)

def Deferred_Mesh_Name_All():
    strItemType = 'Deferred Mesh'
    asVariant = 'all'
    return __fn_pyModo_Item_Name(strItemType, asVariant)

def Deferred_Mesh_Name_Selected():
    strItemType = 'Deferred Mesh'
    asVariant = 'selected'
    return __fn_pyModo_Item_Name(strItemType, asVariant)

def Deferred_Mesh_Name_UnSelected():
    strItemType = 'Deferred Mesh'
    asVariant = 'unselected'
    return __fn_pyModo_Item_Name(strItemType, asVariant)



pym.Render_Pass_ID_All()