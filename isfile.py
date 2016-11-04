
 

import maya.cmds as mc
import os
projectPath = 'E:/test_vray'
allFileNames=[]
tagFileNames = os.listdir(projectPath)
print tagFileNames
for FileName in tagFileNames:
    FileName=os.path.join('E:/test_vray', FileName).replace(os.sep,"/")
    if os.path.isfile(FileName):
        if  FileName.split('.')[1]=='mel' or 'mb':
            allFileNames.append(FileName)
            print allFileNames   

        
import maya.cmds as mc
import os
a='E:/test_vray/Sphere_Sphere_Diffuse.jpg'
if not print a.split('.')[1]=='jpg':
    print 
aa=a.split('.')
print aa[1]


if not FileName.split('.')[1]=='mel' or 'mb':
            allFileNames.append(FileName)