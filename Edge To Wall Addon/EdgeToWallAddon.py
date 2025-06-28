bl_info = {
    "name": "Parametric Brick Wall",
    "blender": (4, 2, 1),
    "category": "Object",
    "author": "JPG",
    "description": "Creates a wall from a pre-drawn edge.",
    "version": (1, 0),
}

#___________________________________________________________________

import bpy
import math
#___________________________________________________________________

class EdgeToWallPanel(bpy.types.Panel):
    bl_label = "Edge to Wall Panel"
    bl_idname = "PT_EdgeToWallPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edge To Wall Tab'
    
    def draw(self,context):
        layout = self.layout
        
        row = layout.row()
        row.label(text= "sample text")




#___________________________________________________________________
       
def register():
    bpy.utils.register_class(EdgeToWallPanel)


def unregister():
    bpy.utils.unregister_class(EdgeToWallPanel)

if __name__ == "__main__":
    register()