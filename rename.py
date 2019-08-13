import glob, os

def rename(dir, pattern, code):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, 'H2O.CGI.KMEANS.SENT1.V01.'+ title[17:25] + code + ext))

    #C01: Barrow (Alaska, USA)
    #C03: Teshekpuk (Alaska, USA)
    #C04: Mackenzie Delta (Canada)
    #C06: Kytalyk (Russia)
    #C07: Lena Delta, Russia
    #C08: Yamal (Russia)
    #CS12_1: Cape Espenberg Lowland (Alaska, USA)
    #CS12_2: Central Seward Peninsula (Alaska, USA)
code = '.C07'
rename(r'D:\GlobPermafrost\raw images\C07_Lena Delta\EW\KMEANS\New folder', r'*.tif',code)

# import os
# dir = r'D:\GlobPermafrost\raw images\Deliverable_Dec2018\CGI\C12_2_Central_Seward_Peninsula\KMEANS'
# for filename in os.listdir(dir):
#     NewName = filename.replace('CS12_2', 'C12_2')
#     os.rename(os.path.join(dir, filename), os.path.join(dir, NewName))