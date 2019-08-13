##georeference output from MAGIC
#IRGS result colour: grounded ice (0,0,254), floating ice (0,254,254) (MAGIC automatically saves 255 to 254) 
#IRGS result (.bmp) should have the same name as the SAR image (.tif). 
#IRGS results and SAR images are in the same folder
#output in a separte folder
from osgeo import gdal
import numpy as np
import os
from PIL import Image
import subprocess

def georeference(filename,output_path,code,percent):
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    
    bmp = filename[:-4] + '.bmp'
    im = Image.open(bmp)
    p = np.array(im)
    data = np.zeros((rows, cols), dtype=np.float)
    landmask = filename[:-4] + '_landmask.bmp'
    mask_array = gdal.Open(landmask).ReadAsArray()
                
    for i in range(0, rows):
        for j in range(0, cols):
            if mask_array[i,j] == 0:
                data[i,j] = np.NAN
            elif np.all(p[i,j] == [0,254,254]):
                data[i,j] = 2
            elif np.all(p[i,j] == [0,0,254]):
                data[i,j] = 1
                
    grounded = np.count_nonzero(data == 1)
    floating = np.count_nonzero(data == 2)
    percent_g = round(grounded/(grounded+floating), 4)
    percent_f = round(floating/(grounded+floating), 4)
    print ("grounded ice%: ", percent_g)
    print ("floating ice%: ", percent_f)            
                
    ##write the image
    ##DATE
    d_start = filename.find('_EW_GRDM') + 14
    d_end = filename.find('T', d_start)
    date = filename[d_start:d_end] 
    #percent = output_path + "\\Percentage.txt"            
    with open(percent, "a") as file:
        #file.write('IRGSEM\n'+'Date\tGrounded ice\tFloating ice'+'\n') 
        file.write(date +'\t'+str(percent_g)+'\t'+str(percent_f)+'\n')        
    outfile = output_path + '\\' + 'H2O.CGI.IRGSEM.SENT1.V01.' + date + '.' + code + '.tif'
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outfile, cols, rows, 1, gdal.GDT_Byte) 
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
    outband = outdata.GetRasterBand(1)
    ct = gdal.ColorTable()
    #ct.SetColorEntry(0, (255,255,255,255)) #white background for NaN
    ct.SetColorEntry(0, (0,0,0,255))
    ct.SetColorEntry(1, (0,0,255,255))      #grounded ice color(0,0,255), used to be (0,0,102)
    ct.SetColorEntry(2, (0,255,255,255))    #floating ice color(0,255,255)
    outband.SetColorTable(ct)
    outband.WriteArray(data)
    #outband.SetNoDataValue(0)
    outband.FlushCache() ##saves to disk!!
    outdata = None
    outband = None
    ds = None


def main():
    rootdir = r'D:\GlobPermafrost\raw images\C12_Central_Seward_Peninsula\EW\IRGSEM'
    output_georef = rootdir + '\\' + 'georef'
    if not os.path.exists(output_georef):
        os.makedirs(output_georef)
    code = 'CS12_2'
    #C01: Barrow (Alaska, USA)
    #C03: Teshekpuk (Alaska, USA)
    #C04: Mackenzie Delta (Canada)
    #C06: Kytalyk (Russia)
    #C07: Lena Delta, Russia
    #C08: Yamal (Russia)
    #CS12_1: Cape Espenberg Lowland (Alaska, USA)
    #CS12_2: Central Seward Peninsula (Alaska, USA)
    percent = output_georef + "\\Percentage.txt"
    with open(percent, "a") as file:
        file.write('IRGSEM\n'+'Date\tGrounded ice\tFloating ice'+'\n')     
    for file in os.listdir(rootdir):
        if file.endswith(".tif"):
            print (os.path.join(rootdir, file))    
            georeference(os.path.join(rootdir, file), output_georef, code, percent)
    output_path = output_georef + '\\' + 'UTM'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ##UTM Zone
    # C01_Barrow: zone 4
    # C03_Teshekpuk: zone 5
    # C04_Mackenzie: zone 8
    # C06_Kytalyk: zone 55
    # C07_LenaDelta: zone 52
    # C08_Yamal: zone 42
    # CS12_1: Cape Espenberg Lowland (Alaska, USA):3
    # CS12_2: Central Seward Peninsula (Alaska, USA):3
    for file in os.listdir(output_georef):
        if file.endswith(".tif"):
            print(os.path.join(output_georef, file))
            subprocess.call(
                ['gdalwarp', '-t_srs', "+proj=utm +zone=3 +datum=WGS84 +units=m +no_defs", os.path.join(output_georef, file),
                 os.path.join(output_path, file)], shell=True)

if __name__== "__main__":
    main()