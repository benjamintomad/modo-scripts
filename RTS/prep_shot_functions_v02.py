# python

import lx
import os
import re
import modo
# import tank
# reload(tank)

scene = modo.scene.current()



def create_render_pass_character(character):
    polyrender = scene.renderItem
    outputgroups = []
    passgroup = scene.addRenderPassGroup(name="RN_%s" % character)

    # creates all the passes
    finalpass = passgroup.addPass(name="%s" % character)
    bakepass = passgroup.addPass(name="%s_bake" % character)

    # identifies the output groups
    for grp in scene.items(itype='mask'):
        if grp.name == "Outputs":
            outputs_fin = grp
            outputgroups.append(grp)
        if grp.name == "Outputs_bake":
            outputs_bke = grp
            outputgroups.append(grp)

    # adds channels to the passes
    for group in outputgroups:
        passgroup.addChannel("enable", item=group)

    for channel in polyrender.channels():
        passgroup.addChannel(channel, item=polyrender)

    # sets the effects per pass
    finalpass.active = True
    outputs_bke.channel("enable").set(False)
    outputs_fin.channel("enable").set(True)
    lx.eval('edit.apply')

    bakepass.active = True
    outputs_bke.channel("enable").set(True)
    outputs_fin.channel("enable").set(False)
    bakepass.enabled = False
    lx.eval('edit.apply')

    return passgroup


def create_render_pass_ground(ground):
    polyrender = scene.renderItem
    outgrps = []
    passgroup = scene.addRenderPassGroup(name="RN_%s" % ground)

    # creates all the passes
    finalpass = passgroup.addPass(name="%s" % ground)

    # identifies the output groups
    for grp in scene.items(itype='mask'):
        if grp.name == "Outputs":
            outputs_fin = grp
            outgrps.append(grp)
        if grp.name == "Outputs_bake":
            outputs_bke = grp
            outgrps.append(grp)

    # adds channels to the passes
    for group in outgrps:
        passgroup.addChannel("enable", item=group)

    for channel in polyrender.channels():
        passgroup.addChannel(channel, item=polyrender)

    # sets the effects per pass
    finalpass.active = True
    outputs_bke.channel("enable").set(False)
    outputs_fin.channel("enable").set(True)
    lx.eval('edit.apply')

    return passgroup


def create_render_pass_shadow(ground):
    outgrps = []
    passgroup = scene.addRenderPassGroup(name="RN_%s" % ground)

    # creates all the passes
    shadowpass = passgroup.addPass(name="%s" % ground)

    # identifies the output groups
    for grp in scene.items(itype='mask'):
        if grp.name == "Outputs_fin":
            outputs_fin = grp
            outgrps.append(grp)
        if grp.name == "Outputs_bake":
            outputs_bke = grp
            outgrps.append(grp)

    # adds channels to the passes
    for group in outgrps:
        passgroup.addChannel("enable", item=group)

    # sets the effects per pass
    shadowpass.active = True
    outputs_bke.channel("enable").set(False)
    outputs_fin.channel("enable").set(False)
    lx.eval('edit.apply')

    return passgroup


def create_overrides(passgroups):

    overridegroup = []

    upgroups = []
    for grp in scene.items('mask'):
        if grp.parent == scene.renderItem:
            upgroups.append(grp)
    index = len(upgroups)+1

    for currentgroup in passgroups:
        # adds the override main group, the one whose visibility will be affected by the render passes
        groupname = currentgroup.name.strip('RN_') + ' (override)'
        uppergroup = scene.addMaterial('mask', groupname)
        overridegroup.append(uppergroup)

        for othergroup in passgroups:
            if othergroup != currentgroup:
                othergroupname = othergroup.name.strip('RN_')
                lowergroup = scene.addMaterial('mask', othergroupname)

                for grp in scene.items('groupLocator'):
                    if grp.name == "CHARACTERS":
                        for child in grp.children(recursive=True, itemType='groupLocator'):
                            if othergroupname in child.name:
                                scene.select(lowergroup)
                                lx.eval('mask.setMesh %s' % child.name)

                lowergroup.setParent(newParent=uppergroup)

        uppergroup.channel('enable').set(False)
        uppergroup.setParent(newParent=scene.renderItem, index=index-2)
        scene.select(uppergroup)

    return overridegroup


def set_overrides_visibility(passgroups, overrides):

    for group in passgroups:
        for mask in overrides:
            group.addChannel("enable", item=mask)

    # get all action clips (passes)
    for clip in scene.items('actionclip'):
        clip.active = True
        clipname = clip.name
        clipname = clipname.strip('_bake')
        masks = []
        for mask in overrides:
            if clipname not in mask.name:
                masks.append(mask)
            elif clipname in mask.name:
                mask.channel('enable').set(True)

        for msk in masks:
            msk.channel('enable').set(False)
        lx.eval('edit.apply')
        clip.active = False

    for grp in overrides:
        grp.channel('enable').set(False)


def create_passgroups_from_grounds(grounds):
    passgroups = []
    for grd in grounds:
        passname = 'RN_' + grd.name.strip(' (grd)')
        passe = scene.addRenderPassGroup(passname)
        passgroups.append(passe)
    return passgroups


def create_base_shaders(overrides):
    shaders = []
    for group in overrides:
        for child in group.children():
            baseshader = scene.addMaterial('defaultShader')
            baseshader.setParent(newParent=child)
            shaders.append(baseshader)
    return shaders


def shadow_pass_baseshader_invisible():
    dict = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': '', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'none', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}
    return dict


def invisible_baseshader_settings():
    dict = {'shadCast': 0L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': 'fullShade', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'ic', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 0L, 'blend': 'normal', 'alphaType': 'opacity'}
    return dict


def shadow_pass_baseshader():
    dict = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 1L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': '', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'none', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}
    return dict


def get_characters():
    characters = []
    for grp in scene.items('groupLocator'):
        if grp.name == "CHARACTERS":
            for c in grp.children():
                characters.append(c.name)
    return characters
