#GDAL Utilities is only installed for Python 3.4 (not anaconda) on this machine
#reproject the images to UTM OR UTM to WGS84
# output path has to be different from rootdir (bc output won't overwrite)
import os  
import subprocess

rootdir = r'D:\GlobPermafrost\raw images\C12_1_Cape_Espenberg_Lowland\EW\DOY_THRESH'
output_path = r'D:\GlobPermafrost\raw images\C12_1_Cape_Espenberg_Lowland\EW\DOY_THRESH\UTM'
if not os.path.exists(output_path):
    os.makedirs(output_path)    

##UTM Zone 
#C01_Barrow: zone 4
#C03_Teshekpuk: zone 5
#C04_Mackenzie: zone 8
#C06_Kytalyk: zone 55
#C07_LenaDelta: zone 52
#C08_Yamal: zone 42
#CS12_1: Cape Espenberg Lowland (Alaska, USA):3
#CS12_2: Central Seward Peninsula (Alaska, USA):3
for file in os.listdir(rootdir):
    if file.endswith(".tif"):
        print (os.path.join(rootdir, file))    
        subprocess.call(['gdalwarp','-t_srs', "+proj=utm +zone=3 +datum=WGS84 +units=m +no_defs", os.path.join(rootdir, file), os.path.join(output_path, file)], shell=True)
        # subprocess.call(['gdalwarp', '-of', 'GTiff', '-t_srs', 'EPSG:32604', os.path.join(rootdir, file),os.path.join(output_path, file)], shell=True)
        # subprocess.call(['gdalwarp', os.path.join(rootdir, file), os.path.join(output_path, file),'-t_srs', "+proj=longlat  +zone=4 +ellps=WGS84"], shell=True)
    