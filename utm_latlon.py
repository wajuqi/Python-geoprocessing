import utm
import osr

# Option 1: using utm package
easting, northing = utm.from_latlon(66.58, -165.0)[0], utm.from_latlon(66.58, -165.0)[1]
lat, lon = utm.to_latlon(629712.663788628, 7396078.817061811, 3, 'W')

def transform_utm_to_wgs84(easting, northing, zone):
    utm_coordinate_system = osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS("WGS84") # Set geographic coordinate system to handle lat/lon
    is_northern = northing > 0
    utm_coordinate_system.SetUTM(zone, is_northern)

    wgs84_coordinate_system = utm_coordinate_system.CloneGeogCS() # Clone ONLY the geographic coordinate system

    # create transform component
    utm_to_wgs84_transform = osr.CoordinateTransformation(utm_coordinate_system, wgs84_coordinate_system) # (<from>, <to>)
    return utm_to_wgs84_transform.TransformPoint(easting, northing, 0) # returns lon, lat, altitude

# Option 2: WGS84 to UTM function
def transform_wgs84_to_utm(lon, lat, zone):
    # def get_utm_zone(longitude):
    #     return (int(1+(longitude+180.0)/6.0))

    def is_northern(latitude):
        """
        Determines if given latitude is a northern for UTM
        """
        if (latitude < 0.0):
            return 0
        else:
            return 1

    utm_coordinate_system = osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS("WGS84") # Set geographic coordinate system to handle lat/lon
    # utm_coordinate_system.SetUTM(get_utm_zone(lon), is_northern(lat))
    utm_coordinate_system.SetUTM(zone, is_northern(lat))

    wgs84_coordinate_system = utm_coordinate_system.CloneGeogCS() # Clone ONLY the geographic coordinate system

    # create transform component
    wgs84_to_utm_transform = osr.CoordinateTransformation(wgs84_coordinate_system, utm_coordinate_system) # (<from>, <to>)
    return wgs84_to_utm_transform.TransformPoint(lon, lat, 0) # returns easting, northing, altitude

easting_1, northing_1, altitude = transform_wgs84_to_utm(-165.0, 66.58, 3)