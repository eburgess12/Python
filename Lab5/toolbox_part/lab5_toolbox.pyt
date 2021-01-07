# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarageTool]


class GarageTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "GarageTool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName = "GDB Folder",
            name = "GDB_Folder",
            datatype = "DEFolder",
            parameterType = "Required",
            direction = "Input"
        )
        param1 = arcpy.Parameter(
            displayName = "GDB Name",
            name = "GDB_Name",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )
        param2 = arcpy.Parameter(
            displayName = "Garage CSV File",
            name = "Garage_CSV_File",
            datatype = "DEFile",
            parameterType = "Required",
            direction = "Input"
        )
        param3 = arcpy.Parameter(
            displayName = "Garage Layer Name",
            name = "Garage_Layer_Name",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )
        param4 = arcpy.Parameter(
            displayName = "Campus GDB",
            name = "Campus_GDB",
            datatype = "DEType",
            parameterType = "Required",
            direction = "Input"
        )
        param5 = arcpy.Parameter(
            displayName = "Garage Name for Search",
            name = "Garage_Name_for_Search",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )
        param6 = arcpy.Parameter(
            displayName = "Buffer Distance",
            name = "Buffer_Distance",
            datatype = "GPDouble",
            parameterType = "Required",
            direction = "Input"
        )

        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # create a new database
        gdb_folder = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        # if you want to run this code again, comment the following line
        arcpy.CreateFileGDB_management(gdb_folder, gdb_name)

        # import garage csv file
        csv_file = parameters[2].valueAsText
        x_field = 'X'
        y_field = 'Y'
        garage_layer_name = parameters[3].valueAsText
        garage_layer = arcpy.MakeXYEventLayer_management(csv_file, x_field, y_field, garage_layer_name)

        # gdb_lab5_path = r'C:\GEOG392\Lab5\lab5_gdb.gdb'
        gdb_lab5_path = gdb_folder + '\\' + gdb_name 
        arcpy.FeatureClassToGeodatabase_conversion(garage_layer, gdb_lab5_path)

        # Copy "Structures" layer
        campus_gdb = parameters[4].valueAsText
        structures_campus = campus_gdb + '\\' + 'Structures'
        buildings_lab5_gdb = gdb_lab5_path + '\\' + 'Buildings'
        arcpy.Copy_management(structures_campus, buildings_lab5_gdb)

        # Re-projection
        garage_points_gcs = gdb_lab5_path + '\\' + garage_layer_name
        spatial_ref = arcpy.Describe(buildings_lab5_gdb).spatialReference
        arcpy.Project_management(garage_points_gcs, gdb_lab5_path + '\\' + 'Garage_Points_Reprojected', spatial_ref)


        ################# something new ################# 
        garagename_input = parameters[5].valueAsText
        buffer_distance_input = parameters[6].valueAsText

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
            arcpy.TableToTable_conversion(gdb_lab5_path + '\\' + 'Garage_Single_Buffer_Intersect.dbf', r'C:\GEOG392\Lab5\toolbox_part', 'nearbyBuildings.csv')
        else:
            messages.AddErrorMessage('That garage does not exist')
            raise arcpy.ExecuteError

        ################# something new #################

        return None