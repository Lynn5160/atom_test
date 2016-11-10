vray addAttributesFromGroup file7 vray_file_gamma 1;
'vrayFileColorSpace'

#gamma correct
import maya.cmds as cmds
if cmds.objExists('file7'+'.'+'vrayFileColorSpace'):
    cmds.setAttr('file7'+'.'+'vrayFileColorSpace',1)
else:
    cmds.vray('addAttributesFromGroup','file7','vray_file_gamma' ,1)
    cmds.setAttr('file7'+'.'+'vrayFileColorSpace',1)
    
    
