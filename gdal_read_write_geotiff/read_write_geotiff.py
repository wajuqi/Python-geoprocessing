from osgeo import gdal

filename = r'D:\Python scripts\Threshold\subset_1_of_S1A_IW_GRDH_1SDV_20171205T165930_20171205T165959_019570_0213BE_1251_40.tif'
ds = gdal.Open(filename, gdal.GA_ReadOnly)
cols = ds.RasterXSize
rows = ds.RasterYSize
driver = ds.GetDriver().LongName
geotransform = ds.GetGeoTransform()
originX = geotransform[0]   #top left x
originY = geotransform[3]   # top left y
pixelWidth = geotransform[1]    #w-e pixel resolution
pixelHeight = -geotransform[5]   #n-s pixel resolution

#read in the first two bands into arrays
band1 = ds.GetRasterBand(1)
band2 = ds.GetRasterBand(2)
band1_array = band1.ReadAsArray()
band2_array = band2.ReadAsArray()

#apply some band math
result_array = band1_array - band2_array        #difference of the two bands

##write the image
outfile = r'D:\Python scripts\Threshold\output.tif'
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create(outfile, cols, rows, 1, gdal.GDT_Float32)
outdata.SetGeoTransform(geotransform)
outdata.SetProjection(ds.GetProjection())##sets same projection as input
outband = outdata.GetRasterBand(1)
outband.WriteArray(result_array)
outband.FlushCache() ##saves to disk!!
outdata = None
outband = None
ds = None
band_theta = None