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
    "version": (1, 0, 3),
    "blender": (3, 4, 1),
    "location": "View3D > Tools > Global Subsurf",
    "description": "Changes subsurf modifier level settings",
    "warning": "Beta release",
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


class SubsurfSettingsPanel(bpy.types.Panel):
    bl_label = "Global Subsurf"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod
    def poll(self, context):
        try:
           return (context.mode == 'OBJECT' or conext.mode == 'EDIT')
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
              
        # levels settings sub box
        sub_box = box.box()      
        sub_box.label(text="Subdivison Levels:") 
                
        row = sub_box.row()
        
        split = row.split()
        col = split.column()
        col.label(text='Viewport')
        col.label(text='Render')
        
        col = split.column(align=True)
        col.prop(settings, 'view_level', text = '')
        col.prop(settings, 'render_level', text = '')

        row = sub_box.row()
        row.prop(settings, 'opt_display', text = 'Optimal Display')
        
        sub_box.prop(settings, 'object_sel', text="Apply to")
              
        # operator
        box.operator('subsurf.settings')
# end of - class SubsurfSettingsPanel(bpy.types.Panel): 


class SubsurfSettingsOP(bpy.types.Operator):
    bl_idname = "subsurf.settings"
    bl_label = "Apply Subsurf Settings"
    bl_description = "Apply these settings to objects with subsurf modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        print("SubsurfSettingsOP - started")
        obj = bpy.data.objects
        settings = bpy.context.scene.subsurf_settings        
        
        obj_list = [] # define obj_list list - a list of all objects
        # that can have subsurf modifiers 
            
        # from UI
        view_levels = settings.view_level # define view levels for subsurf 
        render_levels = settings.render_level # define render levels for subsurf
        optimal_display = settings.opt_display # flag for optimal display            
        show_render = settings.show_render # show modifier while rendering
        show_view = settings.show_view # show modifier while viewing in 3d view
        show_edit = settings.show_edit # show modifier while in edit mode
        show_cage = settings.show_cage # show modifier on edit cage
        select = settings.object_sel # define select - this is what 
        #objects will be worked on. ALL, SEL, or VIS
        
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
                if select == 'ALL':
                    obj_list.append(index)
                elif select == 'SEL' and index in bpy.context.selected_objects:
                    obj_list.append(index)
                elif select == 'VIS' and index.visible_get():
                    obj_list.append(index)       
        
        # loop thru all objects
        for object in obj_list:
            obj_modifiers = object.modifiers
            
            # loop thru all modifiers on object
            for mod in obj_modifiers:
                # check for subsurf modifier & set levels/settings
                if mod.type == "SUBSURF": 
                    
                    mod.levels = view_levels
                    mod.render_levels = render_levels
                                        
                    # set render, object, edit, cage mode, optimal display
                    # for modifier
                    mod.show_render = show_render
                    mod.show_viewport = show_view
                    mod.show_in_editmode = show_edit 
                    mod.show_on_cage = show_cage
                    mod.show_only_control_edges = optimal_display
                                                                    
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
            description="Skip displaying interior subdivided endges.", \
            default=False)      
                
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
    bpy.utils.register_class(SubsurfSettingsOP)
    bpy.utils.register_class(SubsurfSettingsPanel)
    bpy.utils.register_class(subsurf_settings)

def unregister():
    bpy.utils.unregister_class(SubsurfSettingsOP)
    bpy.utils.unregister_class(SubsurfSettingsPanel)
    bpy.utils.unregister_class(subsurf_settings)    
    
if __name__ == "__main__":
    register()
    
