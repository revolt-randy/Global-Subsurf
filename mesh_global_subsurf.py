# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

import bpy

bl_info = {
    "name": "Global Subsurf Settings",
    "author": "revolt_randy",
    "version": (1, 5, 0),
    "blender": (3, 6, 5),
    "location": "View3D > Tools > Global Subsurf",
    "description": "Changes subsurf modifier level settings",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

# version history:
# 1st release as an addon: 9/16/2012
#   - initial release
# 2nd release: 7/5/2014
#   - originally only worked on mesh objects, now works on any object with
#       subsurf modifiers
#   - added controls to change subsurf modifier during render, view, and edit
#   - added checkbox to control if subsurf levels are changed or not
#   - tidy up the code a bit & add gpl license
# 3rd version: 1/30/2023
#   - updated to blender 3.4.1
#   - cleaned up UI/code
# 4th version: 9/30/2024
#   - fixed it to work in edit mode for any object that can have a subsurf mod
#   - set min blender version to 3.6.5
# 5th version: 3/31/2026
#   - created __init.py__ file to simpify installing from github.
#


class SUBSURF_SETTINGS_PT_Panel(bpy.types.Panel):
    bl_idname = "SUBSURF_SETTINGS_PT_Panel"
    bl_label = "Global Subsurf"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    valid_modes = ['OBJECT', 'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_TEXT']   # need to add all modes to this list
    
    
    @classmethod
    def poll(self, context):
        #print(context.mode)
        try:
            if context.mode in self.valid_modes:            
                return True
            else:
                return False
        except AttributeError:
            return 0
       
    def draw(self, context):
        settings = bpy.context.scene.subsurf_settings
        layout = self.layout
        #layout.label(text="Global Subsurf Modifier Settings:")
        box = layout.box()
        
        #header
        row = box.row(align = True)                        
        row.label(icon = 'MOD_SUBSURF', text = '  Subsurf')                
        row.prop(settings, 'show_cage', toggle = True, \
            icon = 'MESH_DATA', icon_only=True)
        row.prop(settings, 'show_edit', toggle = True,\
            icon = 'EDITMODE_HLT', icon_only = True)
        row.prop(settings, 'show_view', toggle = True,\
            icon = 'RESTRICT_VIEW_OFF', icon_only = True)        
        row.prop(settings, 'show_render', toggle = True,\
            icon = 'RESTRICT_RENDER_OFF', icon_only = True)
              
        row = box.row()
        
        split = row.split()
        col = split.column()
        col.label(text='Levels Viewport')
        col.label(text='Render')
        
        col = split.column(align=True)
        col.prop(settings, 'view_level', text = '')
        col.prop(settings, 'render_level', text = '')
        col.prop(settings, 'opt_display', text = 'Optimal Display')
        
        row = layout.row()
        row.prop(settings, 'object_sel', text="Apply to")
              
        # operator
        row = layout.row()
        row.operator('subsurf_settings.operator')
# end of - class SubsurfSettingsPanel(bpy.types.Panel): 


class SUBSURF_SETTINGS_OT_Operator(bpy.types.Operator):
    bl_idname = "subsurf_settings.operator"
    bl_label = "Apply Subsurf Settings"
    bl_description = "Apply these settings to objects with subsurf modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        #print("SubsurfSettingsOP - started")
        obj = bpy.data.objects
        settings = bpy.context.scene.subsurf_settings        
        
        obj_list = [] # define obj_list list - a list of all objects
        # that can have subsurf modifiers 
        
        # loop thru all objects, adding only objects that can have subsurf
        # modifiers on them to obj_list list
        for index in obj:
            
            if index.type == 'MESH' \
                or index.type == 'CURVE' \
                or index.type == 'SURFACE' \
                or index.type == 'META' \
                or index.type == 'FONT':                                   
                
                # object can have a subsurf modifier on it, now check to see
                # if it should be added to obj_list based on UI
                if settings.object_sel == 'ALL':
                    obj_list.append(index)
                elif settings.object_sel == 'SEL' and index in bpy.context.selected_objects:
                    obj_list.append(index)
                elif settings.object_sel == 'VIS' and index.visible_get():
                    obj_list.append(index)       
        
        # loop thru all objects to be worked on
        for object in obj_list:
            obj_modifiers = object.modifiers
            
            # loop thru all modifiers on object
            for mod in obj_modifiers:
                # check for subsurf modifier & set levels/settings
                if mod.type == "SUBSURF": 
                    
                    mod.levels = settings.view_level
                    mod.render_levels = settings.render_level
                                        
                    # set render, object, edit, cage mode, optimal display
                    # for modifier
                    mod.show_render = settings.show_render
                    mod.show_viewport = settings.show_view
                    mod.show_in_editmode = settings.show_edit 
                    mod.show_on_cage = settings.show_cage
                    mod.show_only_control_edges = settings.opt_display
                                                                    
        return{'FINISHED'}


# property group
class subsurf_settings(bpy.types.PropertyGroup):

    @classmethod
    def register(subsurf_settings):
            
        subsurf_settings.show_render = bpy.props.BoolProperty( \
            name="Render", \
            description="Use modifier during render", \
            default=True)

        subsurf_settings.show_view = bpy.props.BoolProperty( \
            name="Realtime", \
            description="Display modifier in viewport", \
            default=True)

        subsurf_settings.show_edit = bpy.props.BoolProperty( \
            name="Edit Mode", \
            description="Display modifier in Edit mode", \
            default=True)
        
        subsurf_settings.show_cage = bpy.props.BoolProperty( \
            name="On Cage", \
            description="Adjust edit cage to modifier result", \
            default=True)

        subsurf_settings.view_level = bpy.props.IntProperty( \
            name = "Levels", \
            description = "Number of subdivisions to perform", \
            default = 1, \
            min = 0, \
            max = 6)

        subsurf_settings.render_level = bpy.props.IntProperty( \
            name = "Render Levels", \
            description = "Number of subdivisions to perform when rendering", \
            default = 2, \
            min = 0, \
            max = 6) 
        
        subsurf_settings.opt_display = bpy.props.BoolProperty( \
            name="Optimal", \
            description="Skip displaying interior subdivided edges.", \
            default=True)      
                
        subsurf_settings.object_sel = bpy.props.EnumProperty( \
            name = "Objects", \
            items = [
            ("ALL", "All Objects", "Apply settings to all objects"),
            ("SEL", "Selected Objects", "Apply settings to only selected objects"),
            ("VIS", "Visible Objects", "Apply settings to only visible objects")
            ], \
            description = "Apply Subsurf Modifier settings to:")
            
        # pointer to property group
        bpy.types.Scene.subsurf_settings = \
            bpy.props.PointerProperty(type=subsurf_settings, \
                name="subsurf_settings", \
                description="Global Subsurf Settings")
   
            
def register():
    bpy.utils.register_class(SUBSURF_SETTINGS_OT_Operator)
    bpy.utils.register_class(SUBSURF_SETTINGS_PT_Panel)
    bpy.utils.register_class(subsurf_settings)

def unregister():
    bpy.utils.unregister_class(SUBSURF_SETTINGS_OT_Operator)
    bpy.utils.unregister_class(SUBSURF_SETTINGS_PT_Panel)
    bpy.utils.unregister_class(subsurf_settings)    
    
if __name__ == "__main__":
    register()
    
