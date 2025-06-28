#Coding a simple addon myself without copy and pasting.

#    MAIN LEARNING FROM THIS
 
# 1-Make sure everything is registered and unregistered.
# 2-Always check for spelling mistakes.


bl_info = {
    "name": "Johnny's coded addon",
    "blender": (4, 2, 1),
    "category": "Simple Add Buttons",
    "author": "JPG",
    "description": "This addon is helping me learn how to code. This addon provides a panel with two simple buttons that add a cube and a sphere",
}

import bpy

#Creating a panel in the UI
class JohnPanel(bpy.types.Panel):
    bl_label = "Johnny's Panel"
    bl_idname = "VIEW3D_PT_JohnPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Johnnys Addon"

    def draw(self, context):#I think this is the layout for the menu.
        layout = self.layout
        layout.operator("object.cube_operator")#This is for the first button.
        layout.operator("object.sphere_operator")#This is for the second button.

class CubeOperator(bpy.types.Operator):#this code is for the first button to execute the action/task.
    bl_idname = "object.cube_operator"#Still not sure what this means.
    bl_label = "Add a Cube"#this is for what the button is called.

    def execute(self, context):#this is the executing code if the button is clicked.
        bpy.ops.mesh.primitive_cube_add()
        return {'FINISHED'}

class SphereOperator(bpy.types.Operator):
    bl_idname = "object.sphere_operator"
    bl_label = "Add a Sphere"

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(JohnPanel)
    bpy.utils.register_class(CubeOperator)
    bpy.utils.register_class(SphereOperator)

def unregister():
    bpy.utils.unregister_class(JohnPanel)
    bpy.utils.unregister_class(CubeOperator)
    bpy.utils.unregister_class(SphereOperator)

if __name__ == "__main__":
    register()