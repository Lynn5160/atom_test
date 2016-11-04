#SP2M v1.01b author 戴巍
#http://weibo.com/david376

#### for maya2014



import maya.cmds as mc
import maya.cmds as cmds
import os

def connectUVNodeToTextureNode(UVnode,textureNode):
    cmds.connectAttr(UVnode +'.outUV',textureNode + '.uvCoord',force = 1)
    cmds.connectAttr(UVnode +'.outUvFilterSize',textureNode + '.uvFilterSize',force = 1)
    attr_list = ["coverage","translateFrame","rotateFrame","mirrorU","mirrorV","wrapU","wrapV","repeatUV","vertexUvOne","vertexUvTwo","vertexUvThree","vertexCameraOne","noiseUV","offset","rotateUV"]
    for attr in attr_list:
        cmds.connectAttr(UVnode +'.'+attr,textureNode + '.'+attr,force = 1)

#get all file names will be used in the sourceimages folder
def getFileNames(materialName):
    projectPath =mc.textField('tagPath',q=True,fileName=True)
    allFileNames = os.listdir(projectPath)
    fileNamesUsing = []
    for fileName in allFileNames:
        if materialName in fileName:
            fileNamesUsing.append(fileName)
    return fileNamesUsing

#udim bool used to judge weather to use udim
udim = False
def UDIM_on(*argus):
    global udim
    udim = True
def UDIM_off(*argus):
    global udim
    udim = False
def UDIM_judge(fileNode):
    global udim
    if udim:
        mc.setAttr(fileNode + '.uvTilingMode',3)
        mc.setAttr(fileNode + '.uvTileProxyQuality',4)
        
    
#create a dict which containts all the textures that having the materialName
#the keys of the dict are the texture's name
#the values of the dict are the file nodes which ref to the texture 
def createTexturesUsing(fileNamesUsing):
    #print fileNamesUsing
    texturesUsing = {}
    targetFileExist = False
    for fileName in fileNamesUsing:
        tempFile = mc.createNode('file')
        texturesUsing[fileName] = tempFile
        mc.setAttr(tempFile + '.fileTextureName',os.path.join(mc.textField('tagPath',q=True,fileName=True),fileName).replace(os.sep,"/"),type = 'string')
        targetFileExist = True
    if not targetFileExist:
        mc.error('写错名字了吧小伙子，检查一下')
    return texturesUsing


def createVrayShadingNetwork(materialName,texturesUsing):
    #get current version of maya
    version = mc.about(version = 1)
    version = int(version)
    #if the version is newer than 2016 ,we can use the colormanagement directly
    if version >= 2016:
        #create vray mtl
        vrayMtl = mc.shadingNode('VRayMtl',asShader = 1,n = materialName)
        mc.setAttr(vrayMtl + '.bumpMapType',1)
        try:
            mc.setAttr(vrayMtl + '.brdfType' , 3)
        except:
            mc.warning('当前版本vray没有ggx_brdf，效果可能不好，请注意')

        #create place2dtexture
        UVnode = mc.shadingNode('place2dTexture',au =1)
        #connect textures to material
        for textureUsing in texturesUsing.keys():
            
            if 'Diffuse' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.diffuseColor')
                mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','sRGB',type = 'string')
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Reflection' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.reflectionColor')
                mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','sRGB',type = 'string')
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Glossiness' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outAlpha',vrayMtl + '.reflectionGlossiness')
                mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','Raw',type = 'string')
                mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'ior' in textureUsing:
                mc.setAttr(vrayMtl + '.lockFresnelIORToRefractionIOR',0)
                mc.connectAttr(texturesUsing[textureUsing] + '.outAlpha',vrayMtl + '.fresnelIOR')
                mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','Raw',type = 'string')
                mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Normal' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.bumpMap')
                mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','Raw',type = 'string')
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            
    else:
        #create vray mtl
        vrayMtl = mc.shadingNode('VRayMtl',asShader = 1,n = materialName)
        mc.setAttr(vrayMtl + '.bumpMapType',1)
        try:
            mc.setAttr(vrayMtl + '.brdfType' , 3)
        except:
            mc.warning('当前版本vray没有ggx_brdf，效果可能不好，请注意')
        #create place2dtexture
        UVnode = mc.shadingNode('place2dTexture',au =1)
        #connect textures to material
        for textureUsing in texturesUsing.keys():
            if 'Diffuse' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.diffuseColor')
                cmds.vray("addAttributesFromGroup",texturesUsing[textureUsing],"vray_file_gamma",1)
                mc.setAttr(texturesUsing[textureUsing] + '.vrayFileColorSpace',2)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Reflection' in textureUsing:
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.reflectionColor')
                cmds.vray("addAttributesFromGroup",texturesUsing[textureUsing],"vray_file_gamma",1)
                mc.setAttr(texturesUsing[textureUsing] + '.vrayFileColorSpace',2)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Glossiness' in textureUsing:
                '''
                gammaCorret = mc.shadingNode('gammaCorrect',au = 1)
                mc.setAttr(gammaCorret + '.gammaX',2.2)
                mc.setAttr(gammaCorret + '.gammaY',2.2)
                mc.setAttr(gammaCorret + '.gammaZ',2.2)
                '''
                cmds.vray("addAttributesFromGroup",texturesUsing[textureUsing],"vray_file_gamma",1)
                mc.setAttr(texturesUsing[textureUsing] + '.vrayFileColorSpace',0)
                mc.connectAttr(texturesUsing[textureUsing] + '.outAlpha',vrayMtl + '.reflectionGlossiness')
                mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'ior' in textureUsing:
                cmds.vray("addAttributesFromGroup",texturesUsing[textureUsing],"vray_file_gamma",1)
                mc.setAttr(texturesUsing[textureUsing] + '.vrayFileColorSpace',0)
                mc.setAttr(vrayMtl + '.lockFresnelIORToRefractionIOR',0)
                '''
                gammaCorret = mc.shadingNode('gammaCorrect',au = 1)
                mc.setAttr(gammaCorret + '.gammaX',2.2)
                mc.setAttr(gammaCorret + '.gammaY',2.2)
                mc.setAttr(gammaCorret + '.gammaZ',2.2)
                '''
                mc.connectAttr(texturesUsing[textureUsing] + '.outAlpha',vrayMtl + '.fresnelIOR')
                mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
            elif 'Normal' in textureUsing:
                '''
                gammaCorret = mc.shadingNode('gammaCorrect',au = 1)
                mc.setAttr(gammaCorret + '.gammaX',2.2)
                mc.setAttr(gammaCorret + '.gammaY',2.2)
                mc.setAttr(gammaCorret + '.gammaZ',2.2)
                '''
                mc.connectAttr(texturesUsing[textureUsing] + '.outColor',vrayMtl + '.bumpMap')
                connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])

def createArnoldShadingNetwork(materialName,texturesUsing):
    
    #create aistandard mtl
    aiStandard = mc.shadingNode('aiStandard',asShader = 1,n = materialName)
    mc.setAttr(aiStandard + '.Kd',1)
    mc.setAttr(aiStandard + '.Ks',1)
    try:
        mc.setAttr(aiStandard + '.specularDistribution' ,1 )
    except:
        mc.warning('你使用的arnold版本没有ggx_brdf，效果可能不好')
    
    #create place2dtexture
    UVnode = mc.shadingNode('place2dTexture',au =1)
    
    #connect textures to material
    for textureUsing in texturesUsing.keys():
        if 'Diffuse' in textureUsing:
            mc.connectAttr(texturesUsing[textureUsing] + '.outColor',aiStandard + '.color')
            mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','sRGB',type = 'string')
            connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
        elif 'Specular' in textureUsing:
            mc.connectAttr(texturesUsing[textureUsing] + '.outColor',aiStandard + '.KsColor')
            mc.setAttr(texturesUsing[textureUsing] + '.colorSpace','sRGB',type = 'string')
            connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
        elif 'Roughness' in textureUsing:
            gammaCorret = mc.shadingNode('gammaCorrect',au = 1)
            mc.setAttr(gammaCorret + '.gammaX',2.2)
            mc.setAttr(gammaCorret + '.gammaY',2.2)
            mc.setAttr(gammaCorret + '.gammaZ',2.2)
            mc.connectAttr(texturesUsing[textureUsing] + '.outColor',gammaCorret + '.value')
            mc.connectAttr(gammaCorret + '.outValueX',aiStandard + '.specularRoughness')
            mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
            connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
        elif 'f0' in textureUsing:
            mc.setAttr(aiStandard + '.specularFresnel',1)
            gammaCorret = mc.shadingNode('gammaCorrect',au = 1)
            mc.setAttr(gammaCorret + '.gammaX',2.2)
            mc.setAttr(gammaCorret + '.gammaY',2.2)
            mc.setAttr(gammaCorret + '.gammaZ',2.2)
            mc.connectAttr(texturesUsing[textureUsing] + '.outColor',gammaCorret + '.value')
            mc.connectAttr(gammaCorret + '.outValueX',aiStandard + '.Ksn')
            mc.setAttr(texturesUsing[textureUsing] + '.alphaIsLuminance', 1)
            connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
        elif 'Normal' in textureUsing:
            bumpNode = mc.shadingNode('bump2d',au = 1)
            mc.setAttr(bumpNode + '.bumpInterp', 1)
            mc.connectAttr(texturesUsing[textureUsing] + '.outAlpha',bumpNode + '.bumpValue')
            mc.connectAttr(bumpNode + '.outNormal',aiStandard + '.normalCamera')
            connectUVNodeToTextureNode(UVnode,texturesUsing[textureUsing])
    
        
def main(materialName):
    #get all file names in the sourceimages folder
    targetFileNames = getFileNames(materialName)
    
    textureNamesUsing =[]

    if udim:
        for targetFileName01 in targetFileNames:
            textureRepeated = False
            for textureUsing in textureNamesUsing:
                if targetFileName01[:-9] == textureUsing[:-9]:
                    textureRepeated = True
                    break
            if textureRepeated:
                continue
            for targetFileName02 in targetFileNames:
                if (not targetFileName01 == targetFileName02) and (targetFileName01[:-9] == targetFileName02[:-9]):
                    
                    textureNamesUsing.append(targetFileName01)
                    break
                    
        #print textureNamesUsing
    else:
        textureNamesUsing = targetFileNames
        #print textureNamesUsing

    #get a dict contains all the textures will be used
    texturesUsing = createTexturesUsing(textureNamesUsing)
        
    #judge every texture using, whether is a udim texture,if yes,change the settings
    for textureUsing in texturesUsing.values():
        UDIM_judge(textureUsing)
    
    

    if cmds.radioCollection('renderer_rc',q=True,select=True) == "VRay_RB":
        createVrayShadingNetwork(materialName,texturesUsing)
    else:
        createArnoldShadingNetwork(materialName,texturesUsing)

    if cmds.checkBox("rep_PreName_CB",q=True,value=True):
        prefix_name = mc.textField('repalce_prefix_name',q=True,fileName=True)
        root_path = mc.textField('tagPath',q=True,fileName=True)
        for tex in texturesUsing:
            Old_path = os.path.join(root_path,tex).replace(os.sep,"/")
            New_path = os.path.join(root_path,prefix_name+tex.rsplit("_",1)[1]).replace(os.sep,"/")
            os.rename(Old_path,New_path)
            cmds.setAttr(texturesUsing[tex]+".fileTextureName",New_path,type="string")
            
def PickUpExportSelectionPath(*args):
        Q_cachePath=cmds.textField('tagPath',q=True,fileName=True)
        return (cmds.fileDialog2(fileMode=1,okCaption='Select the SubPTex path.',cancelCaption='Deselect the path.',startingDirectory=Q_cachePath))
    
def pickUpCachePathButton(*args):
    PickUpCP=PickUpExportSelectionPath()
    if PickUpCP is not None:
        cmds.textField('tagPath',e=True,fileName=os.path.dirname(PickUpCP[0]).replace(os.sep,"/"))
        cmds.textField('material_name',e=True,fileName=os.path.basename(PickUpCP[0]).rsplit("_",1)[0])

def replace_on_command():
    if not mc.text("rep_PreName_text",q=True,enable=True):
        mc.text("rep_PreName_text",e=True,enable=True)
        mc.textField('repalce_prefix_name',e=True,enable=True)
    else:
        mc.text("rep_PreName_text",e=True,enable=False)
        mc.textField('repalce_prefix_name',e=True,enable=False)

if __name__ == "__main__":
    if mc.window('SP2Maya',ex = 1):
        mc.deleteUI('SP2Maya')
    mc.window('SP2Maya',t = 'SP2Maya for Maya2014(VRay)',w=200,h=40 )
    mc.columnLayout()

    cmds.rowLayout(numberOfColumns=6)
    cmds.separator( w=140,h=5, style='none' )
    cmds.text( label='Renderer: ' )
    cmds.radioCollection('renderer_rc')
    cmds.radioButton('VRay_RB', label='VRay',select=True)
    cmds.radioButton('Arnold_RB', label='Arnold',enable=False)
    cmds.setParent('..')
    
    mc.rowLayout(numberOfColumns=4)
    cmds.separator( w=140,h=5, style='none' )
    mc.checkBox(l = 'udim textures',onc = UDIM_on,ofc = UDIM_off,align = 'right')
    cmds.setParent('..')
    
    mc.rowLayout('Tag_Path',numberOfColumns=4)
    cmds.separator( w=140,h=5, style='none' )
    mc.text( label='Path: ' )
    mc.textField('tagPath',width=235,fileName='')
    mc.button(w=18,h=18,l='',c=lambda *args:pickUpCachePathButton())
    mc.setParent('..')
    
    mc.rowLayout(numberOfColumns=4)
    cmds.separator( w=140,h=5, style='none' )
    mc.text( label='MaterialName: ' )
    mc.textField('material_name',width=215,fileName='')
    mc.setParent("..")
    
    mc.rowLayout(numberOfColumns=4)
    cmds.separator( w=140,h=5, style='none' )
    cmds.checkBox("rep_PreName_CB",l='',changeCommand="replace_on_command()")
    mc.text("rep_PreName_text",label='Replace Prefix Name: ',enable=False )
    mc.textField('repalce_prefix_name',width=165,fileName='<Prefix_>',enable=False)
    mc.setParent("..")
    
    mc.rowLayout(numberOfColumns=4)
    cmds.separator( w=140,h=5, style='none' )
    cmds.button(w=290,l='excute',c='main(cmds.textField("material_name",q = 1,fileName =1 ))')
    mc.setParent("..")
    cmds.separator( w=570,h=5, style='none' )
    mc.setParent("..")
    '''
    mc.separator(style = 'none',h = 20)
    mc.separator()
    mc.text(l = 'sp2m v1.01b',w =230,al = 'right',hyperlink = 1,ww = 1,ann = 'the version of the script')
    '''
    mc.showWindow()
    
    
    
