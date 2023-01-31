# Global Subsurf
A Global Subsurf Modifier settings tool for blender

This blender add-on tool is for changing various Subsurf Modifier settings for any/all objects with a Subsurf modifier on them.

## Installation:  

From blender's Edit->Preferences menu, in the Add-ons tab, left-click the 'Install...' button and use the file browser to select the .zip or .py add-on file.  
   
Now the add-on will be installed, however not automatically enabled. The search field will be set to the add-on’s name (to avoid having to look for it), Enable the add-on by checking the enable checkbox.

Once enabled, the add-on will appear in the 3D viewport's tools area.

![alt text](https://github.com/revolt-randy/Global-Subsurf/blob/main/global_subsurf_screenshot.png "Screenshot")

## Usage:
The header has four icons just like the Subsurf modifier has. It also has Viewport and Render levels and an 'Optimal Display' check box. Changes to these setting will be applied to Subsurf modifiers when the tool is executed. The 'Apply to:' dropdown menu allows a user to set what objects will have changes made to thier Subsurf modifier. The options are:  
  * All Objects - works on all objects with Subsurf modifiers.
  * Selected Objects - works on all currently selected objects with Subsurf modifiers.
  * Visible Objects - work on all objects that are currently visible in the 3D viewport.

Clicking on the 'Apply SubSurf Settings' button executes the tool, changing the Subsurf Modifier settings on
