import numpy as np 
import time
import os

#imports from pyFVM. Eventually these will be added to __init__.py
from pyFVM.utilities.IO.Foam.cfdReadPolyMesh import cfdReadPolyMesh
from pyFVM.src.region.cfdSetupRegion import cfdSetupRegion
from pyFVM.utilities.print.cfdPrintMainHeader import cfdPrintMainHeader
from pyFVM.utilities.IO.Foam.cfdReadOpenFoamFiles import cfdReadOpenFoamFiles


#Prints the main header when the simulation is run
cfdPrintMainHeader()


#Creates an instance of the cfdSetupRegion class to hold simulations data
Region=cfdSetupRegion()


#Reads in the OpenFOAM file structure
cfdReadOpenFoamFiles(Region)



seeMesh=Region.mesh




#start = time.time()
#stop=time.time()
#print(stop-start)

"""
Development code to include in cfdReadTimeDirectory.py

Next step:
    
    continue on line 92 of cfdReadTimeDirectory
    
"""
from pyFVM.src.time.cfdGetTimeSteps import cfdGetTimeSteps
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary
from pyFVM.utilities.IO.File.cfdGetKeyValue import cfdGetKeyValue
from pyFVM.utilities.IO.File.cfdGetFoamFileHeader import cfdGetFoamFileHeader
from pyFVM.src.fields.cfdSetupMeshField import cfdSetupMeshField
from pyFVM.utilities.IO.File.cfdReadAllDictionaries import cfdReadAllDictionaries as uv



fluids=Region.fluid

    
"""Reads in field data from starting time folder.

Depending on user input in the controlDict startFrom field, will 
open the respective time directory and read in the fields. The newly read 
field data is stored in a sub-dictionary of Region.fluid, with the key being
the field's name (e.g. Region.fluid['phi']. Everything necessary to define 
the field is accessible from Region. fluid['fieldKey'].

Attributes:
    
   fieldName (str): name of field currently being loaded.
   timeDirectories (list): list of time directories in case.
   timeDirectory (str): path to initial time directory.
   
Example usage:
    
    Region = cfdReadTimeDirectory(Region)
    
TODO:
    Pretty much everything ....
"""


kwargs=[]

if len(kwargs) > 0:
    timeDirectory=kwargs['time']
    
    
elif Region.foamDictionary['controlDict']['startFrom']=='startTime':
    timeDirectory=str(int(Region.foamDictionary['controlDict']['startTime']))
    
    
elif Region.foamDictionary['controlDict']['startFrom']=='latestTime':
    timeDirectories=cfdGetTimeSteps(Region.caseDirectoryPath,Region)
    timeDirectory=max(timeDirectories)
    
    
elif Region.foamDictionary['controlDict']['startFrom']=='firstTime':   
    timeDirectory='0' 
    
else:
    print("Error in controlDict: startFrom is not valid!")
    
for root, directory,files in os.walk(Region.caseDirectoryPath + "\\"+timeDirectory):
    if not files:
        print('Fields are not found in the %s directory' % (Region.caseDirectoryPath + "\\"+timeDirectory+"!"))

for file in files:
    
    fieldName=file
    
    fieldFilePath=Region.caseDirectoryPath + "\\"+timeDirectory+"\\"+fieldName
    
    header=cfdGetFoamFileHeader(fieldFilePath)
    
    cfdSetupMeshField(Region,fieldName,header['class'])
    
    Region.fluid[fieldName]['dimensions']=cfdGetKeyValue('dimensions','dimensions',fieldFilePath)[2]

    internalField = cfdGetKeyValue('internalField','string',fieldFilePath)
    valueType=internalField[1]


    if Region.fluid[fieldName]['type']=='surfaceScalarField':
        
        print('surfaceScalarFields are not yet handled.')
        
        """
        TO-DO: add functionality for reading 'surfaceScalarField'. I couldn't find
        a test case to compare it to. All the tutorials have volScalar and volVector fields
        """

    else:
        
        #read either volScalarField or volVectorField

        if valueType == 'uniform':
            if Region.fluid[fieldName]['type']=='volScalarField':
                
                value_str = internalField[2][0]
                for subList in Region.fluid[fieldName]['phi']:
                    subList[0]=value_str
                    
            elif Region.fluid[fieldName]['type']=='volVectorField':
                
                value_str = internalField[2]
                for count, subList in enumerate(Region.fluid[fieldName]['phi']):
                    Region.fluid[fieldName]['phi'][count]=list(value_str)          
                              
        elif valueType == 'nonuniform':
            print('The function cfdReadNonuniformList() is not yet writen.')
            
            """
            TO-DO: translate the cfdReadNonuniformList function
            """
        
        #read and store cfdBoundary field
        theNumberOfBPatches = len(Region.mesh['cfdBoundaryPatchesArray'])
    
        for iBPatch, values in Region.mesh['cfdBoundaryPatchesArray'].items():
            
            
            
            numberOfBFaces=values['numberOfBFaces']
            iFaceStart=values['startFaceIndex']
            
            iElementStart = Region.mesh['numberOfElements'] + iFaceStart - Region.mesh['numberOfInteriorFaces'] 
            iElementEnd = iElementStart+numberOfBFaces-1
                
            """Next: translate cfdGetKeyValueFromBlock"""   

key='value'
blockName=['boundaryField', iBPatch]

bob=cfdGetKeyValueFromBlock(fieldFilePath)


"""
Function that returns all dictionaries and sub-dictionaries in a file
"""
fieldFilePath=Region.caseDirectoryPath + "\\"+"constant"+"\\"+"turbulenceProperties"

dictionaries = cfdReadAllDictionaries(fieldFilePath)




                
















