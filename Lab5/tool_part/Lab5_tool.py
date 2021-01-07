
import arcpy

# create a new database
gdb_folder = r'C:\GEOG392\Lab5\tool_part'
gdb_name = 'lab5_gdb.gdb'
# if you want to run this code again, comment the following line
arcpy.CreateFileGDB_management(gdb_folder, gdb_name)

# import garage csv file
csv_file = r'C:\GEOG392\Lab5\Lab5_data\garages.csv'
x_field = 'X'
y_field = 'Y'
garage_layer_name = 'Garage_Points'
garage_layer = arcpy.MakeXYEventLayer_management(csv_file, x_field, y_field, garage_layer_name)

# gdb_lab5_path = r'C:\GEOG392\Lab5\lab5_gdb.gdb'
gdb_lab5_path = gdb_folder + '\\' + gdb_name 
arcpy.FeatureClassToGeodatabase_conversion(garage_layer, gdb_lab5_path)

# Copy "Structures" layer
structures_campus = r'C:\GEOG392\Lab5\Lab5_data\Campus.gdb\Structures'
buildings_lab5_gdb = gdb_lab5_path + '\\' + 'Buildings'
arcpy.Copy_management(structures_campus, buildings_lab5_gdb)

# Re-projection
garage_points_gcs = gdb_lab5_path + '\\' + garage_layer_name
spatial_ref = arcpy.Describe(buildings_lab5_gdb).spatialReference
arcpy.Project_management(garage_points_gcs, gdb_lab5_path + '\\' + 'Garage_Points_Reprojected', spatial_ref)


################# something new ################# 
garagename_input = input('Please enter an abbreviation of garage:')
buffer_distance_input = input('Please enter a buffer distance:')

# define where_clause
where_clause = "Name = '%s'" % garagename_input

# check if this garage exists
cursor = arcpy.SearchCursor(gdb_lab5_path + '\\' + 'Garage_Points_Reprojected', where_clause=where_clause)
should_process = False

for row in cursor:
    if row.getValue('Name') == garagename_input:
        should_process = True

if should_process == True:
    # further process
    garage_single_layername = r'\garage_single_%s' % garagename_input
    garage_single_buffer_layername = r'\garage_single_%s_buffer_%s' % (garagename_input, buffer_distance_input)

    # selection
    arcpy.Select_analysis(gdb_lab5_path + '\\' + 'Garage_Points_Reprojected', gdb_lab5_path + garage_single_layername, where_clause)
    
    # Buffer
    buffer_layer = arcpy.Buffer_analysis(gdb_lab5_path + garage_single_layername, gdb_lab5_path + garage_single_buffer_layername, float(buffer_distance_input))

    # Intersect
    arcpy.Intersect_analysis([buildings_lab5_gdb, gdb_lab5_path + garage_single_buffer_layername], gdb_lab5_path + '\\' + 'Garage_Single_Buffer_Intersect', 'ALL')

    # Output CSV File
    arcpy.TableToTable_conversion(gdb_lab5_path + '\\' + 'Garage_Single_Buffer_Intersect.dbf', r'C:\GEOG392\Lab5\tool_part', 'nearbyBuildings.csv')
else:
    print('That garage does not exist')




################# something new #################

