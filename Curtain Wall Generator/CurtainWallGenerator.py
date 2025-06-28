bl_info = {
    "name": "Curtain Wall Generator",
    "blender": (4, 2, 1),
    "category": "Object",
    "author": "Your Name",
    "description": "Generate a curtain wall with one panel and two mullions",
    "version": (1, 0, 0),
    "support": "COMMUNITY",
}

import bpy
import math

# Define the curtain wall operator
class OBJECT_OT_create_curtain_wall(bpy.types.Operator):
    bl_idname = "object.create_curtain_wall"
    bl_label = "Create Curtain Wall"
    
    # Define properties to adjust
    panel_width: bpy.props.FloatProperty(name="Panel Width", default=2.0, min=0.1)
    panel_height: bpy.props.FloatProperty(name="Panel Height", default=4.0, min=0.1)
    mullion_width: bpy.props.FloatProperty(name="Mullion Width", default=0.15, min=0.01)
    
    def execute(self, context):
        # Create curtain wall
        self.create_curtain_wall(context)
        return {'FINISHED'}
    
    def create_curtain_wall(self, context):
        scene = context.scene
        
        # Define the total width and height of the curtain wall
        total_width = self.panel_width + 2 * self.mullion_width  # Two mullions on either side
        total_height = self.panel_height
        
        # Create the left mullion (on the left side of the panel)
        left_x_position = -self.panel_width / 2 - self.mullion_width / 2  # Place the left mullion to the left of the panel
        bpy.ops.mesh.primitive_cube_add(size=1, location=(left_x_position, 0, total_height / 2))
        left_mullion = bpy.context.object
        # Scale the left mullion to the correct dimensions
        left_mullion.scale = (self.mullion_width / 2, total_height / 2, self.mullion_width / 2)
        
        # Create the right mullion (on the right side of the panel)
        right_x_position = self.panel_width / 2 + self.mullion_width / 2  # Place the right mullion to the right of the panel
        bpy.ops.mesh.primitive_cube_add(size=1, location=(right_x_position, 0, total_height / 2))
        right_mullion = bpy.context.object
        # Scale the right mullion to the correct dimensions
        right_mullion.scale = (self.mullion_width / 2, total_height / 2, self.mullion_width / 2)
        
        # Create the panel in between the mullions
        x_position = 0  # Place the panel in the center
        y_position = 0  # Panels will sit at the base level
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x_position, y_position, 0))
        panel = bpy.context.object
        # Scale the panel to the correct size
        panel.scale = (self.panel_width / 2, self.panel_height / 2, 1)
        # Rotate the panel so it faces upward along the Z-axis
        panel.rotation_euler = (math.radians(90), 0, 0)
        
        # Center the curtain wall to make it easier to work with
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')


# Panel and mullion UI settings
class OBJECT_PT_curtain_wall_panel(bpy.types.Panel):
    bl_label = "Curtain Wall Generator"
    bl_idname = "OBJECT_PT_curtain_wall"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        operator = layout.operator("object.create_curtain_wall", text="Create Curtain Wall")
        
        # Panel parameters
        layout.prop(operator, "panel_width")
        layout.prop(operator, "panel_height")
        layout.prop(operator, "mullion_width")


# Register classes
def register():
    bpy.utils.register_class(OBJECT_OT_create_curtain_wall)
    bpy.utils.register_class(OBJECT_PT_curtain_wall_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_curtain_wall)
    bpy.utils.unregister_class(OBJECT_PT_curtain_wall_panel)

if __name__ == "__main__":
    register()
