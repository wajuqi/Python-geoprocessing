##convert kmeans result (geotiff) produced from SNAP to binary, and convert to utm
##put all geotiff kmeans results in rootdir
from osgeo import gdal
import numpy as np
import os
from PIL import Image
import ogr
import subprocess
import glob

def rename(dir, pattern, code):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir, 'H2O.CGI.KMEANS.SENT1.V01.' + title[17:25] + '.' + code + ext))

def convert_kmeans(filename, output_path):
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    head, tail = os.path.split(filename)
    date = tail[25:32]
    
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    
    result = np.zeros((rows, cols), dtype=np.float)
    for i in range(0, rows):
        for j in range(0, cols):
            r, g, b = rgb_im.getpixel((j,i))
            if (r,g,b)==(0,0,0):                #floating ice
                result[i,j] = np.NAN
            elif (r,g,b)==(0,0,255):            #grounded ice
                result[i,j] = 1
            elif (r,g,b)==(0,255,255):
                result[i,j] = 2
            else:
                print ('ERROR:')
                print ('col:',col, 'row:',row)
                print ('RGB:',r,g,b)
                err = err+1
                
    grounded = np.count_nonzero(result == 1)
    floating = np.count_nonzero(result == 2)
    percent_g = round(grounded/(grounded+floating), 4)
    percent_f = round(floating/(grounded+floating), 4)
    print ("grounded ice%: ", percent_g)
    print ("floating ice%: ", percent_f)       
                
    ##write the image             
  
    percent = output_path + "\\Percentage.txt"            
    with open(percent, "a") as file:
        file.write('KMEANS\n'+'Date\tGrounded ice\tFloating ice'+'\n') 
        file.write(date +'\t'+str(percent_g)+'\t'+str(percent_f)+'\n')
    
    outfile = output_path + '\\' + tail
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
    outband.WriteArray(result)
    #outband.SetNoDataValue(0)
    outband.FlushCache() ##saves to disk!!
    outdata = None
    outband = None
    ds = None


def main():
        # C01: Barrow (Alaska, USA)
        # C03: Teshekpuk (Alaska, USA)
        # C04: Mackenzie Delta (Canada)
        # C06: Kytalyk (Russia)
        # C07: Lena Delta, Russia
        # C08: Yamal (Russia)
        # CS12_1: Cape Espenberg Lowland (Alaska, USA)
        # CS12_2: Central Seward Peninsula (Alaska, USA)
    code = 'CS12_2'
    rootdir = r'D:\GlobPermafrost\raw images\C12_Central_Seward_Peninsula\EW\KMEANS\rename'
    rename(rootdir, r'*.tif', code)
    output_convert = rootdir + '\\' +'convert'
    if not os.path.exists(output_convert):
        os.makedirs(output_convert)
    for file in os.listdir(rootdir):
        if file.endswith(".tif"):
            print (os.path.join(rootdir, file))
            convert_kmeans(os.path.join(rootdir, file), output_convert)
    output_path = output_convert + '\\' + 'UTM'
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
    for file in os.listdir(output_convert):
        if file.endswith(".tif"):
            print(os.path.join(output_convert, file))
            subprocess.call(
                ['gdalwarp', '-t_srs', "+proj=utm +zone=3 +datum=WGS84 +units=m +no_defs", os.path.join(output_convert, file),
                 os.path.join(output_path, file)], shell=True)

if __name__== "__main__":
    main()

