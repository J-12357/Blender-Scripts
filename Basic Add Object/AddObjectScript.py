bl_info = {
    "name" : "Object Adder",
    "author" : "JPG",
    "version" : (1, 0),
    "blender" : (4, 2, 1),
    "location" : "View3d > Tool",
    "warning" : "None",
    "wiki_url" : "None",
    "Category" : "Add Mesh",

}    



import bpy

class TestPanel(bpy.types.Panel):
    bl_label = "Object Adder"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        
        row = layout.row()
        row.label(text= "Addon Object", icon= 'OBJECT_ORIGIN')
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon= 'CUBE')
        row.operator("mesh.primitive_uv_sphere_add", icon= 'SPHERE')
        row = layout.row()
        row.operator("object.text_add", icon= 'FILE_FONT', text= "Font Button")

class PanelA(bpy.types.Panel):
    bl_label = "Scale"
    bl_idname = "PT_PanelA"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    bl_parent_id = 'PT_TestPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context): 
        layout = self.layout
        obj = context.object
        
        row = layout.row()
        row.label(text= "Select an option to scale", icon= 'FONT_DATA')
        row = layout.row()
        row.operator("transform.resize")
        row = layout.row()
        layout.scale_y = 1.4
        
        col = layout.column()
        col.prop(obj, "scale")

class PanelB(bpy.types.Panel):
    bl_label = "Specials"
    bl_idname = "PT_PanelB"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    bl_parent_id = 'PT_TestPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context): 
        layout = self.layout
        
        row = layout.row()
        row.label(text= "Select a Special Option", icon= 'COLOR_BLUE')
        row = layout.row()
        row.operator("object.shade_smooth", icon= 'MOD_SMOOTH', text= "Set Smooth Shading")
        row = layout.row()
        row.operator("object.subdivision_set")
        row = layout.row()
        row.operator("object.modifier_add")
    
def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(PanelA)
    bpy.utils.register_class(PanelB)

def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(PanelB)
    
if __name__== "__main__":
    register()   