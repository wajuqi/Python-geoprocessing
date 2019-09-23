# installing s2cloudless: https://github.com/sentinel-hub/sentinel2-cloud-detector
# reference: https://github.com/sentinel-hub/sentinel2-cloud-detector/issues/1
from s2cloudless import S2PixelCloudDetector
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from osgeo import gdal
import os
import skimage.transform as st

def trim_processed(shapefile_link, input_file_link, output_file_link):
    os.system('gdalwarp -overwrite -cutline ' + "'" + shapefile_link + "'" + '  -crop_to_cutline -of GTiff -r cubic ' + "'" + input_file_link + "' " + "'" + output_file_link + "'")

def cloud_detection(input_path, cloudmask, cloudprobs):
    for file in sorted(os.listdir(input_path)):
        if file.endswith("B01.jp2"):
            ds = gdal.Open(os.path.join(input_path, file), gdal.GA_ReadOnly)
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B01 = scl.read()
                tmparr = np.empty_like(B01)
                aff = scl.transform
                print(B01.shape)
        if file.endswith("B02.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B02 = scl.read()
                reproject(
                    B02, tmparr,
                    src_transform=scl.transform,
                    dst_transform=aff,
                    src_crs=scl.crs,
                    dst_crs=scl.crs,
                    resampling=Resampling.bilinear)
                B02 = tmparr
                print(B02.shape)
        if file.endswith("B04.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B04 = scl.read()
                reproject(
                   B04, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B04 = tmparr
                print(B04.shape)
        if file.endswith("B05.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B05 = scl.read()
                reproject(
                   B05, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B05 = tmparr
                print(B05.shape)
        if file.endswith("B08.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B08 = scl.read()
                reproject(
                   B08, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B08 = tmparr
                print(B08.shape)
        if file.endswith("B8A.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B8A = scl.read()
                reproject(
                   B8A, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B8A = tmparr
                print(B8A.shape)
        if file.endswith("B09.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B09 = scl.read()
        if file.endswith("B10.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B10 = scl.read()
        if file.endswith("B11.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B11 = scl.read()
                reproject(
                   B11, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B11 = tmparr
                print(B11.shape)
        if file.endswith("B12.jp2"):
            with rasterio.open(os.path.join(input_path, file)) as scl:
                B12 = scl.read()
                reproject(
                   B12, tmparr,
                   src_transform=scl.transform,
                   dst_transform=aff,
                   src_crs=scl.crs,
                   dst_crs=scl.crs,
                   resampling=Resampling.bilinear)
                B12 = tmparr
                print(B12.shape)
            print(B12.shape)

    bands = np.array([np.dstack((B01[0] / 10000.0, B02[0] / 10000.0, B04[0] / 10000.0, B05[0] / 10000.0, B08[0] / 10000.0,
                                B8A[0] / 10000.0, B09[0] / 10000.0, B10[0] / 10000.0, B11[0] / 10000.0,
                                B12[0] / 10000.0))])
    print(bands.shape)
    cloud_detector = S2PixelCloudDetector(threshold=0.4, average_over=4, dilation_size=2)
    cloud_probs = cloud_detector.get_cloud_probability_maps(bands)
    mask = cloud_detector.get_cloud_masks(bands)#.astype(rasterio.uint8)

    # write the cloud mask and cloud probability map
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(cloudmask, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_UInt16)
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
    outband = outdata.GetRasterBand(1)
    outband.WriteArray(mask[0])
    outband.FlushCache() ##saves to disk!!
    del outband
    del outdata
    trim_processed(shapefile_link, cloudmask, cloudmask_clipped)
    os.remove(cloudmask)
    outdata = driver.Create(cloudprobs, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
    outband = outdata.GetRasterBand(1)
    outband.WriteArray(cloud_probs[0])
    outband.FlushCache() ##saves to disk!!
    del outband
    del outdata
    trim_processed(shapefile_link, cloudprobs, cloudprobs_clipped)
    os.remove(cloudprobs)


def cloudmask_image(inputfile):
    ds = gdal.Open(inputfile, gdal.GA_ReadOnly)
    array = ds.GetRasterBand(1).ReadAsArray()
    ds_cloudmask = gdal.Open(cloudmask_clipped, gdal.GA_ReadOnly)
    # ds_cloudmask = gdal.Open(cloudmask, gdal.GA_ReadOnly)

    cloudmask_array = ds_cloudmask.GetRasterBand(1).ReadAsArray()
    cloudmask_array_resized = st.resize(cloudmask_array, array.shape, order=0, preserve_range=True,                                    mode='constant')
    array_cloudmasked = np.ma.masked_array(array, mask=cloudmask_array_resized.astype(bool)).filled(-5)
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(os.path.splitext(inputfile)[0] + '_cloudmasked.tif', ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
    outband = outdata.GetRasterBand(1)
    outband.WriteArray(array_cloudmasked)
    outband.FlushCache()  ##saves to disk!!

path = os.getcwd()
shapefile_link = "Waterloo Farm 1_geometry.geojson"
clipped = os.path.join(path, 'IMG_DATA', 'clipped')
if not os.path.exists(clipped):
    os.makedirs(clipped)
outpath = os.path.join(path, 'cloud')
if not os.path.exists(outpath):
    os.makedirs(outpath)
cloudmask = os.path.join(outpath, 'cloud_mask.tif')
cloudprobs = os.path.join(outpath, 'cloud_probs.tif')
cloudmask_clipped = os.path.join(outpath, 'cloud_mask_clipped.tif')
cloudprobs_clipped = os.path.join(outpath, 'cloud_probs_clipped.tif')
converted_file_link_ndvi = path + "/vegHealth/vegHealth_converted.tiff"
converted_file_link_msavi = path + "/soilNutri/soilNutri_converted.tiff"
converted_file_link_ndwi = path + '/soilMoist/soilMoist_converted.tiff'

for file in os.listdir(os.path.join(path, 'IMG_DATA')):
    if file.endswith(".jp2"):
        trim_processed(shapefile_link, os.path.join(path, 'IMG_DATA', file), os.path.join(clipped, file))

# generating cloud mask and cloud probability maps
cloud_detection(clipped, cloudmask, cloudprobs)
# cloud mask the images
cloudmask_image(converted_file_link_ndvi)
cloudmask_image(converted_file_link_msavi)
cloudmask_image(converted_file_link_ndwi)



