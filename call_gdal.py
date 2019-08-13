#from osgeo import gdal
#import os
##clip the image by shp (call gdalwarp utility)
##import subprocess
#shp = "Barrow_two.shp"
#INPUT = 'Barrow_msk_float32.tif'
#OUTPUT = 'gdal output5.tif'
##os.system ('gdalwarp -cutline %s -crop_to_cutline -dstalpha %s %s' %(shp, INPUT, OUTPUT))
#subprocess.call(['gdalwarp', '-cutline', shp, '-crop_to_cutline','-dstalpha', INPUT, OUTPUT])      #-dstalpha:add an alpha band to the output tiff which masks out the area falling outside the cutline.

from osgeo import gdal
import ogr
from numpy import *
import os
import subprocess

#get lake boundary extent
polygon = 'Barrow.shp'
source_ds = ogr.Open(polygon)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()
print("lake boundary extent:", x_min, x_max, y_min, y_max)


#subset the image
INPUT = 'subset_1_of_S1B_EW_GRDM_1SDH_20161206T032144_20161206T032244_003270_005937_8206.tif'
OUTPUT = "subset2.tif"
translate = 'gdal_translate -projwin %s %s %s %s %s %s' %(x_min, y_max, x_max, y_min, INPUT, OUTPUT)
os.system(translate)