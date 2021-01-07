
import arcpy

# RS composite bands
source = r"C:\Users\belys\Documents\Class_Files\Fall_2020\GEOG_392\Lab7_important\LT05_L1TP_026039_20110819_20160831_01_T1_Elyse"
band1 = arcpy.sa.Raster(source + "\LT05_L1TP_026039_20110819_20160831_01_T1_B1.TIF") # blue
band2 = arcpy.sa.Raster(source + "\LT05_L1TP_026039_20110819_20160831_01_T1_B2.TIF") # green
band3 = arcpy.sa.Raster(source + "\LT05_L1TP_026039_20110819_20160831_01_T1_B3.TIF") # red
band4 = arcpy.sa.Raster(source + "\LT05_L1TP_026039_20110819_20160831_01_T1_B4.TIF") # NIR
composite = arcpy.CompositeBands_management([band1, band2, band3, band4], source + "\combined_Elyse.tif")

# Hillshade
source = r"C:\Users\belys\Documents\Class_Files\Fall_2020\GEOG_392\Lab7_important\DEM"
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + r"\n30_w097_1arc_v3_Elyse.tif", source + r"\n30_w097_1arc_v3_Elyse_hillshade.tif", azimuth, altitude, shadows, z_factor)

# Slope
source = r"C:\Users\belys\Documents\Class_Files\Fall_2020\GEOG_392\Lab7_important\DEM"
output_measurement = "DEGREE"
z_factor = 1
method = "PLANAR"
z_unit = "METER"
arcpy.ddd.Slope(source + r"\n30_w097_1arc_v3_Elyse.tif", source + r"\n30_w097_1arc_v3_Elyse_slopes.tif", output_measurement, z_factor, method, z_unit)
