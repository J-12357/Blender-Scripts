bl_info = {
    "name": "Object Adder",
    "author": "JPG",
    "version": (1, 0),
    "blender": (4, 2, 1),
    "location": "View3D > Tool",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy

# -------------------------- PANEL 1 --------------------------
class OBJECT_PT_TestPanel(bpy.types.Panel):
    bl_label = "Object Adder"
    bl_idname = "OBJECT_PT_TestPanel"  # ✅ Fixed naming
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2

        row = layout.row()
        row.label(text="Addon Object", icon='OBJECT_ORIGIN')
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon='CUBE')
        row.operator("mesh.primitive_uv_sphere_add", icon='SPHERE')
        row = layout.row()
        row.operator("object.text_add", icon='FILE_FONT', text="Font Button")


# -------------------------- PANEL 2 --------------------------
class OBJECT_PT_PanelA(bpy.types.Panel):
    bl_label = "Scale"
    bl_idname = "OBJECT_PT_PanelA"  # ✅ Fixed naming
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    bl_parent_id = 'OBJECT_PT_TestPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        obj = context.object  # ✅ Fix: Avoid errors if no object is selected

        row = layout.row()
        row.label(text="Select an option to scale", icon='FONT_DATA')
        row = layout.row()
        row.operator("transform.resize")

        if obj:  # ✅ Prevents error if no object is selected
            layout.prop(obj, "scale")
        else:
            layout.label(text="No object selected", icon='ERROR')


# -------------------------- PANEL 3 --------------------------
class OBJECT_PT_PanelB(bpy.types.Panel):
    bl_label = "Specials"
    bl_idname = "OBJECT_PT_PanelB"  # ✅ Fixed naming
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    bl_parent_id = 'OBJECT_PT_TestPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Select a Special Option", icon='COLOR_BLUE')
        row = layout.row()
        row.operator("object.shade_smooth", icon='MOD_SMOOTH', text="Set Smooth Shading")
        row = layout.row()
        row.operator("object.subdivision_set")
        row = layout.row()
        row.operator("object.modifier_add")


# -------------------------- REGISTER / UNREGISTER --------------------------
classes = [OBJECT_PT_TestPanel, OBJECT_PT_PanelA, OBJECT_PT_PanelB]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # ✅ Register classes properly

def unregister():
    for cls in reversed(classes):  # ✅ Unregister in reverse order
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
