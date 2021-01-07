# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName = "Renderer Type",
            name = "Renderer_Type",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )
        param0.filter.list = ['Unique Value Renderer', 'Graduated Colors Renderer']

        param1 = arcpy.Parameter(
            displayName = "Input ArcGIS Pro Project File",
            name = "Input_ArcGIS_Pro_Project_File",
            datatype = "DEFile",
            parameterType = "Required",
            direction = "Input"
        )
        param1.filter.list = ['aprx']

        param2 = arcpy.Parameter(
            displayName = "Layer Name",
            name = "Layer_Name",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )

        param3 = arcpy.Parameter(
            displayName = "Output ArcGIS Pro Project File",
            name = "Output_ArcGIS_Pro_Project_File",
            datatype = "DEFile",
            parameterType = "Required",
            direction = "Output"
        )
        param3.filter.list = ['aprx']

        params = [param0, param1, param2, param3]
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
        # Define our progressor variables
        readTime = 2.5
        start = 0
        maximum = 100
        step = 50

        # Setup the progressor
        arcpy.SetProgressor("step", "Creating Color Map...", start, maximum, step)
        time.sleep(readTime)
        # Add message to the results pane
        arcpy.AddMessage("Creating Color Map...")

        renderer_type = parameters[0].valueAsText
        if renderer_type == 'Unique Value Renderer':
            # DO UNIQUE ...
            # Reference to our .aprx
            project = arcpy.mp.ArcGISProject(parameters[1].valueAsText)

            # Increment the progressor and change the label; add message to the results pane
            arcpy.SetProgressorPosition(start + step)
            arcpy.SetProgressorLabel("Loading ArcGIS Pro Project File...")
            time.sleep(readTime)
            arcpy.AddMessage("Loading ArcGIS Pro Project File...")

            # Grab the first map in the .aprx
            campus = project.listMaps('Map')[0]
            # Loop through available layers in the map
            for layer in campus.listLayers():
                # Check that the layer is a feature layer
                if layer.isFeatureLayer:
                    # Obtain a copy of the layer's symbology
                    symbology = layer.symbology
                    # Makes sure symbology has an attribute "renderer"
                    if hasattr(symbology, 'renderer'):
                        # Check if the layer's name is "GarageParking"
                        if layer.name == parameters[2].valueAsText:
                            # Update the copy's renderer to be "UniqueValueRenderer"
                            symbology.updateRenderer('UniqueValueRenderer')
                            # Tells arcpy that we want to use "Type" as our unique value
                            symbology.renderer.fields = ["LotType"]
                            # Set the layer's actual symbology equal to the copy's
                            layer.symbology = symbology # Very important step
                        
                            # Increment the progressor and change the label; add message to the results pane
                            arcpy.SetProgressorPosition(start + step)
                            arcpy.SetProgressorLabel("Coloring...")
                            time.sleep(readTime)
                            arcpy.AddMessage("Coloring...")
                        else:
                            print("NOT GarageParking")
            project.saveACopy(parameters[3].valueAsText)
        if renderer_type == 'Graduated Colors Renderer':
            # DO GRADUATED ...
            # Reference to our .aprx
            project = arcpy.mp.ArcGISProject(parameters[1].valueAsText)

            # Increment the progressor and change the label; add message to the results pane
            arcpy.SetProgressorPosition(start + step)
            arcpy.SetProgressorLabel("Loading ArcGIS Pro Project File...")
            time.sleep(readTime)
            arcpy.AddMessage("Loading ArcGIS Pro Project File...")

            # Grab the first map in the .aprx
            campus = project.listMaps('Map')[0]
            # Loop through available layers in the map
            for layer in campus.listLayers():
                # Check if layer is a feature layer
                if layer.isFeatureLayer:
                    # Obtain a copy of the layer's symbology
                    symbology = layer.symbology
                    # Check if it has a 'renderer' attribute
                    if hasattr(symbology, 'renderer'):
                        # Check if the layer's name is 'GarageParking'
                        if layer.name == parameters[2].valueAsText:
                            # Update the copy's renderer to be 'GraduatedColorsRenderer'
                            symbology.updateRenderer('GraduatedColorsRenderer')
                            # Tell arcpy which field we want to base our choropleth off of
                            symbology.renderer.classificationField = "Shape_Area"
                            # Set how many classes we'll have 
                            symbology.renderer.breakCount = 5
                            # Set the color ramp
                            symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                            # Set the layer's actual symbology equal to the copy's
                            layer.symbology = symbology # Very important step
                            
                            # Increment the progressor and change the label; add message to the results pane
                            arcpy.SetProgressorPosition(start + step)
                            arcpy.SetProgressorLabel("Coloring...")
                            time.sleep(readTime)
                            arcpy.AddMessage("Coloring...")
                        else:
                            print("NOT GarageParking")
            project.saveACopy(parameters[3].valueAsText)
        return
