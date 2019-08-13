import ogr
from osgeo import gdal
import os
from pyproj import Proj, transform

def subset(INPUT, OUTPUT, xmin, xmax, ymin, ymax):
    translate = 'gdal_translate -projwin %s %s %s %s %s %s' %(xmin, ymax, xmax, ymin, INPUT, OUTPUT)
    os.system(translate)

def main():
    rootdir = r'H:\FINLAND_MODIS\Data\IM'
    output_path = rootdir + '\\Subset'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ##get lake boundary extent
    # shp = 'Barrow.shp'
    # shp = 'Kytalyk_SiberiaC2.shp'
    # shp = 'Lena_delta2c.shp'
    # shp = 'Mackenzie Delta_NWTcmodify.shp'
    # shp = 'Teshekpuk_Lake2c.shp'
    # shp = 'Yamal_SiberiaC2.shp'
    shp = 'H:\FINLAND_MODIS\shp\Finland_lakes.shp'
    shp_ds = ogr.Open(shp)
    source_layer = shp_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    print("lake boundary extent:", x_min, x_max, y_min, y_max)

    # ## if shp and image are in different coordinate system
    # inProj = Proj(init='epsg:4230')
    # outProj = Proj(init='epsg:32662')
    # x_min, y_max = transform(inProj, outProj, x_min, y_max)
    # x_max, y_min = transform(inProj, outProj, x_max, y_min)

    for file in os.listdir(rootdir):
        if file.endswith(".tif"):
            print (os.path.join(rootdir, file))
            # ds = gdal.Open(os.path.join(rootdir, file), gdal.GA_ReadOnly)
            # ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
            # lrx = ulx + (ds.RasterXSize * xres)
            # lry = uly + (ds.RasterYSize * yres)  # ulx, uly is the upper left corner, lrx, lry is the lower right corner
            # xmin = max(x_min, ulx)
            # xmax = min(x_max, lrx)
            # ymin = max(y_min, lry)
            # ymax = min(y_max, uly)
            # subset(os.path.join(rootdir, file), os.path.join(output_path, file), xmin, xmax, ymin, ymax)
            subset(os.path.join(rootdir, file), os.path.join(output_path, file), x_min, x_max, y_min, y_max)

if __name__== "__main__":
    main()