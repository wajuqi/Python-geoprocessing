import os

# gdalwarp https://gdal.org/programs/gdalwarp.html
def clip(shp, INPUT, OUTPUT):
    gdalwarp = 'gdalwarp -cutline %s -dstalpha %s %s' % (shp, INPUT, OUTPUT)
    os.system(gdalwarp)

def main():
    rootdir = r'H:\FINLAND_MODIS\Data\IM'
    output_path = rootdir + '\\clip'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # shp = r'G:\MODIS_Lake_boundary\lake-polygons-PML-wkt_to_shp\GLWD00000677_BEAR-Lake.shp'
    shp = r'G:\MODIS_Lake_boundary\CCI_Lakes_fixed.shp'

    for file in os.listdir(rootdir):
        if file.endswith(".tif"):
            print(os.path.join(rootdir, file))
            clip(shp, os.path.join(rootdir, file), os.path.join(output_path, file))

if __name__ == "__main__":
    main()