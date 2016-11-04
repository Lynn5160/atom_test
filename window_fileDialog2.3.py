import maya.cmds as mc
if mc.window('SP2M',ex = 1):
	mc.deleteUI('SP2M')
mc.window('SP2M',t = 'SP2M',w=200,h=40 )
mc.columnLayout()

mc.rowLayout(numberOfColumns=5)
mc.text('Render:')
cmds.radioCollection()
mc.radioButton(label="VRay")
mc.radioButton(label="Arnold")
mc.setParent('..')

mc.rowLayout(numberOfColumns=2)
#mc.separator(h = 50) 
#mc.separator(style = 'out') 
mc.checkBox(l = 'udim textures',onc = UDIM_on,ofc = UDIM_off,align = 'right')
mc.setParent('..')

mc.rowLayout(numberOfColumns=3)
mc.text('path:')
mc.textField("PATH",w=200)
mc.button(l='imagepath',c='cmds.textField("PATH",w=200,e=True,text=mc.fileDialog2(fileMode=1)[0]) and mc.textField("material",w=200,e=True,text=name(materialName))')
mc.setParent('..')

mc.rowLayout(numberOfColumns=3)
mc.text('materialName:')
mc.textField('material',w=200)
mc.button(l='excute')
mc.setParent('..')
mc.showWindow()
print mc.textField(material,q=True)
def name(materialName):
	path=mc.textField("PATH",q=True,text=True)
	tagName=path.rsplit('/',1)[1] 
	materialName=tagName.rsplit('_',1)[0]
	return materialName
