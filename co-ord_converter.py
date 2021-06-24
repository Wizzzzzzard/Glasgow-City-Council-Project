import math

North = 666099.000 # Northing to be transformed
East = 253697.000 # Easting to be transformed

a = 6377563.396 # Semi-major axis for OGSB36
#a = 6378137.0000 # Semi-major axis for WGS84

b = 6356256.909 # Semi-minor axis for OGSB36
#b = 6356752.3142 # Semi-minor axis for WGS84

f0 = 0.9996012717 # Central Meridan Scale

e0 = 400000 # True origin Easting 
n0 = -100000 # True origin Northing

PHI0 = 0.855211333 # True origin latitude (Radians) i.e. N 49 0' 0''
DecimalPHI0 = 49.00000000 # True origin latitude (Degrees)

LAM0 = -0.034906585 # True origin longitude (Radians) i.e. W 2 0' 0''
DecimalLAM0 = -2.00000000 # True origin longitude (Degrees)

def InitialLat(North, n0, af0, PHI0, n, bf0):
    """
    'Compute initial value for Latitude (PHI) IN RADIANS.
    'Input:
     - northing of point (North) and northing of false origin (n0) in meters;
     - semi major axis multiplied by central meridian scale factor (af0) in meters;
     - latitude of false origin (PHI0) IN RADIANS;
     - n (computed from a, b and f0) and
     - ellipsoid semi major axis multiplied by central meridian scale factor (bf0) in meters.
    """
    #First PHI value (PHI1)
    PHI1 = ((North - n0) / af0) + PHI0

    def Marc(bf0, n, PHI0, PHI1):
        """
        Compute meridional arc.
        Input:
         - ellipsoid semi major axis multiplied by central meridian scale factor (bf0) in meters;
         - n (computed from a, b and f0);
         - lat of false origin (PHI0) and initial or final latitude of point (PHI) IN RADIANS.
        """
        Marc = bf0 * (((1 + n + ((5 / 4) * (n ** 2)) + ((5 / 4) * (n ** 3))) * (PHI1 - PHI0))
        - (((3 * n) + (3 * (n ** 2)) + ((21 / 8) * (n ** 3))) * (math.sin(PHI1 - PHI0)) * (math.cos(PHI1 + PHI0)))
        + ((((15 / 8) * (n ** 2)) + ((15 / 8) * (n ** 3))) * (math.sin(2 * (PHI1 - PHI0))) * (math.cos(2 * (PHI1 + PHI0))))
        - (((35 / 24) * (n ** 3)) * (math.sin(3 * (PHI1 - PHI0))) * (math.cos(3 * (PHI1 + PHI0)))))
        return Marc
    
    # Calculate M
    M = Marc(bf0, n, PHI0, PHI1)
    
    #Calculate new PHI value (PHI2)
    PHI2 = ((North - n0 - M) / af0) + PHI1
    
    #Iterate to get final value for InitialLat
    while abs(North - n0 - M) > 0.00001:
        PHI2 = ((North - n0 - M) / af0) + PHI1
        M = Marc(bf0, n, PHI0, PHI2)
        PHI1 = PHI2
    
    InitialLat = PHI2
    return InitialLat

def E_N_to_Lat(East, North, a, b, e0, n0, f0, PHI0, LAM0):
    """
    Un-project Transverse Mercator eastings and northings back to latitude.
    Input:
     - eastings (East) and northings (North) in meters; _
     - ellipsoid axis dimensions (a & b) in meters; _
     - eastings (e0) and northings (n0) of false origin in meters; _
     - central meridian scale factor (f0) and _
     - latitude (PHI0) and longitude (LAM0) of false origin in decimal degrees.
    """

    #Convert angle measures to radians
    Pi = math.pi
    RadPHI0 = PHI0 * (Pi / 180)
    RadLAM0 = LAM0 * (Pi / 180)
    
    # Compute af0, bf0, e squared (e2), n and Et
    af0 = a * f0
    bf0 = b * f0
    e2 = ((af0 ** 2) - (bf0 ** 2)) / (af0 ** 2)
    n = (af0 - bf0) / (af0 + bf0)
    Et = East - e0

    # Compute initial value for latitude (PHI) in radians
    PHId = InitialLat(North, n0, af0, RadPHI0, n, bf0)
    
    # Compute nu, rho and eta2 using value for PHId
    nu = af0 / (math.sqrt(1 - (e2 * ((math.sin(PHId)) ** 2))))
    rho = (nu * (1 - e2)) / (1 - (e2 * (math.sin(PHId)) ** 2))
    eta2 = (nu / rho) - 1
    
    # Compute Latitude
    VII = (math.tan(PHId)) / (2 * rho * nu)
    VIII = ((math.tan(PHId)) / (24 * rho * (nu ** 3))) * (5 + (3 * ((math.tan(PHId)) ** 2)) + eta2 - (9 * eta2 * ((math.tan(PHId)) ** 2)))
    IX = ((math.tan(PHId)) / (720 * rho * (nu ** 5))) * (61 + (90 * ((math.tan(PHId)) ** 2)) + (45 * ((math.tan(PHId)) ** 4)))
    
    E_N_Lat = (180 / Pi) * (PHId - ((Et ** 2) * VII) + ((Et ** 4) * VIII) - ((Et ** 6) * IX))
    return(E_N_Lat)

def E_N_to_Long(East, North, a, b, e0, n0, f0, PHI0, LAM0):
    """
    Un-project Transverse Mercator eastings and northings back to longitude.
    Input:
     - eastings (East) and northings (North) in meters;
     - ellipsoid axis dimensions (a & b) in meters;
     - eastings (e0) and northings (n0) of false origin in meters;
     - central meridian scale factor (f0) and
     - latitude (PHI0) and longitude (LAM0) of false origin in decimal degrees.
    """
    # Convert angle measures to radians
    Pi = 3.14159265358979
    RadPHI0 = PHI0 * (Pi / 180)
    RadLAM0 = LAM0 * (Pi / 180)
    
    # Compute af0, bf0, e squared (e2), n and Et
    af0 = a * f0
    bf0 = b * f0
    e2 = ((af0 ** 2) - (bf0 ** 2)) / (af0 ** 2)
    n = (af0 - bf0) / (af0 + bf0)
    Et = East - e0
    
    # Compute initial value for latitude (PHI) in radians
    PHId = InitialLat(North, n0, af0, RadPHI0, n, bf0)
    
    # Compute nu, rho and eta2 using value for PHId
    nu = af0 / (math.sqrt(1 - (e2 * ((math.sin(PHId)) ** 2))))
    rho = (nu * (1 - e2)) / (1 - (e2 * (math.sin(PHId)) ** 2))
    eta2 = (nu / rho) - 1
    
    # Compute Longitude
    X = ((math.cos(PHId)) ** -1) / nu
    XI = (((math.cos(PHId)) ** -1) / (6 * (nu ** 3))) * ((nu / rho) + (2 * ((math.tan(PHId)) ** 2)))
    XII = (((math.cos(PHId)) ** -1) / (120 * (nu ** 5))) * (5 + (28 * ((math.tan(PHId)) ** 2)) + (24 * ((math.tan(PHId)) ** 4)))
    XIIA = (((math.cos(PHId)) ** -1) / (5040 * (nu ** 7))) * (61 + (662 * ((math.tan(PHId)) ** 2)) + (1320 * ((math.tan(PHId)) ** 4)) + (720 * ((math.tan(PHId)) ** 6)))

    E_N_Long = (180 / Pi) * (RadLAM0 + (Et * X) - ((Et ** 3) * XI) + ((Et ** 5) * XII) - ((Et ** 7) * XIIA))
    return E_N_Long

E_N_to_Long(East,North,a,b,e0,n0,f0,DecimalPHI0,DecimalLAM0)

def E_N_to_Lat_Long(North, East):
    Lat = E_N_to_Lat(East,North,a,b,e0,n0,f0,DecimalPHI0,DecimalLAM0)
    Long = E_N_to_Long(East,North,a,b,e0,n0,f0,DecimalPHI0,DecimalLAM0)
    return [Lat, Long]

co_ords = E_N_to_Lat_Long(North, East)
print(co_ords)