##georeference output from MAGIC
#IRGS result colour: water (0,0,254), Ice (254,254,0) (MAGIC automatically saves 255 to 254) 
#IRGS result (.bmp) should have the same name as the SAR image (.tif). 
#IRGS results and SAR images are in the same folder
#output in a separte folder
from osgeo import gdal
import numpy as np
import os
from PIL import Image
import ntpath


Image.MAX_IMAGE_PIXELS = 1000000000         
def georeference(filename,output_path):
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    
    bmp = filename[:-4] + '.bmp'
    im = Image.open(bmp)
    p = np.array(im)
    data = np.zeros((rows, cols), dtype=np.float)
    landmask = filename[:-4] + '_landmask.bmp'
    mask_array = gdal.Open(landmask).ReadAsArray()
                
    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         if mask_array[i,j] == 0:
    #             data[i,j] = np.NAN
    #         elif np.all(p[i,j] == [254,254,0]):
    #             data[i,j] = 2   #ice
    #         elif np.all(p[i,j] == [0,0,254]):
    #             data[i,j] = 1   #water
    for i in range(0, rows):
        for j in range(0, cols):
            if mask_array[i,j] == 0:
                data[i,j] = np.NAN
            elif np.all(p[i,j] == [254,254,0]):
                data[i,j] = 1
            elif np.all(p[i,j] == [0,0,254]):
                data[i,j] = 2
            elif np.all(p[i,j] == [254,152,0]):
                data[i,j] = 3
            elif np.all(p[i,j] == [0,254,254]):
                data[i,j] = 4
            elif np.all(p[i,j] == [127,0,127]):
                data[i,j] = 5
            elif np.all(p[i,j] == [0,127,0]):
                data[i,j] = 6
                
#    water = np.count_nonzero(data == 1)
#    ice = np.count_nonzero(data == 2)
#    percent_w = round(water/(water+ice), 4)
#    percent_i = round(ice/(water+ice), 4)
#    print ("water%: ", percent_w)
#    print ("ice%: ", percent_i)            
                
    ##write the image   
#    with open(percent, "a") as file:
#        file.write(date +'\t'+str(percent_w)+'\t'+str(percent_i)+'\n') 
    outfile = output_path + '\\' + ntpath.basename(os.path.normpath(filename))[:-4] + '_IRGS.tif'
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outfile, cols, rows, 1, gdal.GDT_Byte) 
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
    outband = outdata.GetRasterBand(1)
    # ct = gdal.ColorTable()
    # #ct.SetColorEntry(0, (255,255,255,255)) #white background for NaN
    # ct.SetColorEntry(0, (0,0,0,255))
    # ct.SetColorEntry(1, (0,112,255,255))      #water color(0,112,255)
    # ct.SetColorEntry(2, (255,255,0,255))    #ice color(255,255,0)
    # outband.SetColorTable(ct)
    outband.WriteArray(data)
    #outband.SetNoDataValue(0)
    outband.FlushCache() ##saves to disk!!
    outdata = None
    outband = None
    ds = None


def main():
    rootdir = r'C:\Users\Junqian Wang\Downloads\New folder'
    output_path = r'C:\Users\Junqian Wang\Downloads\New folder\IRGS'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
#    percent = output_path + "\\Percentage.txt"  
#    with open(percent, "a") as file:
#        file.write('IRGSEM\n'+'Date\tWATER\tICE'+'\n')     
    for file in os.listdir(rootdir):
        if file.endswith(".tif"):
            print (os.path.join(rootdir, file))    
            georeference(os.path.join(rootdir, file), output_path)

if __name__== "__main__":
    main()