## Converting formats for geospatial rasters
from osgeo import gdal

in_image = gdal.Open(r"C:\Users\Junqian Wang\Downloads\T10SFF_20180917T185019_B03.jp2")

driver = gdal.GetDriverByName("GTiff")

out_image = driver.CreateCopy(r"C:\Users\Junqian Wang\Downloads\test\T10SFF_20180917T185019_B03.tif", in_image, 0)

in_image = None
out_image = None