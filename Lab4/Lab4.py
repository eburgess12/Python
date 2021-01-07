
import arcpy

# create a new database
gdb_folder = r'C:\GEOG392\Lab4'
gdb_name = 'lab4_gdb.gdb'
# if you want to run this code again, comment the following line
arcpy.CreateFileGDB_management(gdb_folder, gdb_name)

# import garage csv file
csv_file = r'C:\GEOG392\Lab4\Lab4_data\garages.csv'
x_field = 'X'
y_field = 'Y'
garage_layer_name = 'Garage_Points'
garage_layer = arcpy.MakeXYEventLayer_management(csv_file, x_field, y_field, garage_layer_name)

# gdb_lab4_path = r'C:\GEOG392\Lab4\lab4_gdb.gdb'
gdb_lab4_path = gdb_folder + '\\' + gdb_name 
arcpy.FeatureClassToGeodatabase_conversion(garage_layer, gdb_lab4_path)

# Copy "Structures" layer
structures_campus = r'C:\GEOG392\Lab4\Lab4_data\Campus.gdb\Structures'
buildings_lab4_gdb = gdb_lab4_path + '\\' + 'Buildings'
arcpy.Copy_management(structures_campus, buildings_lab4_gdb)

# Re-projection
garage_points_gcs = gdb_lab4_path + '\\' + garage_layer_name
spatial_ref = arcpy.Describe(buildings_lab4_gdb).spatialReference
arcpy.Project_management(garage_points_gcs, gdb_lab4_path + '\\' + 'Garage_Points_Reprojected', spatial_ref)

# Buffer
buffer_layer = arcpy.Buffer_analysis(gdb_lab4_path + '\\' + 'Garage_Points_Reprojected', gdb_lab4_path + '\\' + 'Garage_Points_Reprojected_Buffer', 150)

# Intersect
# if you have defined a variable as the return of "arcpy.Buffer_analysis"
# arcpy.Intersect_analysis([buildings_lab4_gdb, buffer_layer], para2, para3)
# if you haven't defined it:
arcpy.Intersect_analysis([buildings_lab4_gdb, gdb_lab4_path + '\\' + 'Garage_Points_Reprojected_Buffer'], gdb_lab4_path + '\\' + 'Garage_Points_Reprojected_Buffer_Intersect', 'ALL')

# Output CSV File
arcpy.TableToTable_conversion(gdb_lab4_path + '\\' + 'Garage_Points_Reprojected_Buffer_Intersect.dbf', r'C:\GEOG392\Lab4', 'nearbyBuildings.csv')