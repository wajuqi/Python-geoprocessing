import ogr
import sys

##get lake boundary extent
def lake_extent(shp):
    source_ds = ogr.Open(shp)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    return (x_min, x_max, y_min, y_max)

code = input("The study area is: ")
shp_dir = r'D:\GitHub\H2OGeomatics\Shapefiles'
    # C01: Barrow (Alaska, USA)
    # C03: Teshekpuk (Alaska, USA)
    # C04: Mackenzie Delta (Canada)
    # C06: Kytalyk (Russia)
    # C07: Lena Delta (Russia)
    # C08: Yamal (Russia)
    # CS12_1: Cape Espenberg Lowland (Alaska, USA)
    # CS12_2: Central Seward Peninsula (Alaska, USA)
if code == 'C01':
    shp = shp_dir + '\\Barrow.shp'
elif code == 'C03':
    shp = shp_dir + '\\Teshekpuk_Lake2c.shp'
elif code == 'C04':
    shp = shp_dir + '\\Mackenzie Delta_NWTcmodify.shp'
elif code == 'C06':
    shp = shp_dir + '\\Kytalyk_SiberiaC2.shp'
elif code == 'C07':
    shp = shp_dir + '\\Lena_delta2c.shp'
elif code == 'C08':
    shp = shp_dir + '\\Yamal_SiberiaC2.shp'
elif code == 'CS12_1':
    shp = shp_dir + '\\Cape_Espenberg_Lowland.shp'
elif code == 'CS12_2':
    shp = shp_dir + '\\Central_Seward_Peninsula.shp'
elif code == 'ALASKA':
    shp = shp_dir + '\\alaska_request_clip.shp'
elif code == 'FINLAND':
    shp = shp_dir + '\\Finland_lakes.shp'
else:
    print("Region code not defined.")

x_min, x_max, y_min, y_max = lake_extent(shp)
print("x_min:", x_min, "\nx_max:", x_max, "\ny_min:", y_min, "\ny_max:", y_max)
print("Mean Longitude:", (x_max+x_min)/2)
print("Mean Latitude:", (y_max+y_min)/2)

# print('ASF Geographic Region:')   #https://vertex.daac.asf.alaska.edu/#
# print(x_min, y_min, x_max, y_min, x_max, y_max, x_min, y_max, x_min, y_min, sep=',')
