#!/usr/bin/env python3

import csv
import ogr
import os
import osr
import sys

## use cmd: python file.py <Input File> <Output File>
# if len(sys.argv)!=3:
#   print("Syntax: {0} <Input File> <Output File>".format(sys.argv[0]))
#   sys.exit(-1)
#
# input_file  = sys.argv[1]
# output_file = sys.argv[2]

spatialref = osr.SpatialReference()  # Set the spatial ref.
# spatialref.ImportFromProj4('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,-0,-0,-0,0 +units=m +no_defs')
spatialref.SetWellKnownGeogCS('WGS84')  # WGS84 aka ESPG:4326

wkt_dir = r'D:\MODIS_Lake boundary\CLMS4k'
out_dir = r'D:\MODIS_Lake boundary\CLMS4k_shp'
for file in os.listdir(wkt_dir):
    print(file)
    input_file = os.path.join(wkt_dir, file)
    # output_file = out_dir + '\\' + os.path.splitext(file)[0] +'.shp'
    output_file = os.path.join(out_dir, os.path.splitext(file)[0] +'.shp')

    layer_name  = os.path.splitext(os.path.basename(output_file))[0]

    driver = ogr.GetDriverByName("ESRI Shapefile")
    dstfile = driver.CreateDataSource(output_file)  # Your output file

    # Please note that it will fail if a file with the same name already exists
    dstlayer = dstfile.CreateLayer(layer_name, spatialref, geom_type=ogr.wkbMultiPolygon)

    # Add the other attribute fields needed with the following schema :
    fielddef = ogr.FieldDefn("ID", ogr.OFTInteger)
    fielddef.SetWidth(10)
    fielddef2 = ogr.FieldDefn("Name", ogr.OFTString)
    fielddef2.SetWidth(50)
    dstlayer.CreateField(fielddef)
    dstlayer.CreateField(fielddef2)

    # Read the feature in your csv file:
    with open(input_file) as fin:
      for nb, row in enumerate(fin.readlines()):
        # WKT is in the second field in my test file :
        poly = ogr.CreateGeometryFromWkt(row)
        feature = ogr.Feature(dstlayer.GetLayerDefn())
        feature.SetGeometry(poly)
        feature.SetField("ID", nb) # A field with an unique id.
        feature.SetField("Name", os.path.splitext(file)[0])
        dstlayer.CreateFeature(feature)
        feature.Destroy()
    dstfile.Destroy()