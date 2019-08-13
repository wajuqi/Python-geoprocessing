from pyproj import Proj, transform
from osgeo import gdal
import ogr

ds = gdal.Open(r'H:\FINLAND_MODIS\Data\IM\MOD.A2010001.0725.IM.tif', gdal.GA_ReadOnly)
ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
lrx = ulx + (ds.RasterXSize * xres)
lry = uly + (ds.RasterYSize * yres)  # ulx, uly is the upper left corner, lrx, lry is the lower right corner

shp = 'H:\FINLAND_MODIS\shp\Finland_lakes.shp'
shp_ds = ogr.Open(shp)
source_layer = shp_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

inProj = Proj(init='epsg:4230')
outProj = Proj(init='epsg:32662')

x_min, y_max = transform(inProj, outProj, x_min, y_max)
x_max, y_min = transform(inProj, outProj, x_max, y_min)

xmin = max(x_min, ulx)
xmax = min(x_max, lrx)
ymin = max(y_min, lry)
ymax = min(y_max, uly)

print ("x_min, y_max, x_max, y_min: ", x_min, y_max, x_max, y_min)
print ("ulx, uly, lrx, lry: ", ulx, uly, lrx, lry)
print ("xmin, ymax, xmax, ymin: ", xmin, ymax, xmax, ymin)

