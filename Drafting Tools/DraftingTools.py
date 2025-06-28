bl_info = {
    "name": "Drafting Tools",
    "blender": (2, 82, 0),  # Adjust this based on your version
    "category": "3D View",
    "author": "Your Name",
    "description": "A set of basic drafting tools like AutoCAD.",
    "version": (1, 0, 0),
    "support": "COMMUNITY",
    "tracker_url": "https://example.com/issues",  # Optional
}

import bpy
from mathutils import Vector

# Utility function to create a line between two points
def create_line(start, end):
    mesh = bpy.data.meshes.new("Line")
    obj = bpy.data.objects.new("Line Object", mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata([start, end], [(0, 1)], [])
    mesh.update()

# Define a new class for properties (No angle needed anymore)
class DraftingToolsProperties(bpy.types.PropertyGroup):
    pass

# Operator to create a line using mouse and X-Y axis control
class DraftingToolsLineOperator(bpy.types.Operator):
    bl_idname = "drafting_tools.create_line"
    bl_label = "Create Line with Mouse"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}
    
    start_x: bpy.props.FloatProperty(name="Start X", default=0.0)
    start_y: bpy.props.FloatProperty(name="Start Y", default=0.0)
    
    start_point = None
    current_point = None
    dragging = False  # Track if the mouse is being dragged
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE' and self.dragging:
            # Get the mouse position in screen coordinates (2D)
            mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y
            region = context.region
            rv3d = context.region_data

            # Convert mouse position to 3D view space (X, Y plane only)
            view_vector = rv3d.view_rotation @ Vector((0.0, 0.0, -1.0))  # View direction
            ray_origin = rv3d.view_matrix.inverted() @ Vector((mouse_x, mouse_y, 0))
            ray_end = ray_origin + view_vector * 10

            # Calculate the difference in X and Y coordinates, keeping Z fixed
            delta_x = ray_end.x - ray_origin.x
            delta_y = ray_end.y - ray_origin.y

            # The line is constrained to the X and Y axes
            self.current_point = self.start_point + Vector((delta_x, delta_y, 0))

            # Update the line in real-time
            create_line(self.start_point, self.current_point)
            return {'RUNNING_MODAL'}
        
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Store the initial position when left-click is pressed
            self.dragging = True
            self.start_point = Vector((self.start_x, self.start_y, 0))
            self.current_point = self.start_point
            return {'RUNNING_MODAL'}
        
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            # Finalize the line when left-click is released
            self.dragging = False
            create_line(self.start_point, self.current_point)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            # Cancel the operation if right-click or escape is pressed
            self.dragging = False
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if event.type == 'LEFTMOUSE':
            # Initialize the start point with the current view coordinates
            self.start_point = Vector((self.start_x, self.start_y, 0))
            self.current_point = self.start_point

            # Add the operator as a modal to track mouse movements
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

        return {'CANCELLED'}

# Addon Panel to hold the buttons and properties
class DraftingToolsPanel(bpy.types.Panel):
    bl_label = "Drafting Tools"
    bl_idname = "VIEW3D_PT_drafting_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Drafting Tools'

    def draw(self, context):
        layout = self.layout
        tool = context.scene.drafting_tools

        # Line Tool button (no angle modifier anymore)
        layout.operator("drafting_tools.create_line", text="Draw Line")

# Register and Unregister functions
def register():
    bpy.utils.register_class(DraftingToolsProperties)  # Register the properties class
    bpy.utils.register_class(DraftingToolsLineOperator)
    bpy.utils.register_class(DraftingToolsPanel)
    
    # Add property to store angle (not needed anymore, but kept for future use)
    bpy.types.Scene.drafting_tools = bpy.props.PointerProperty(type=DraftingToolsProperties)

def unregister():
    bpy.utils.unregister_class(DraftingToolsProperties)  # Unregister the properties class
    bpy.utils.unregister_class(DraftingToolsLineOperator)
    bpy.utils.unregister_class(DraftingToolsPanel)
    
    # Remove property from scene
    del bpy.types.Scene.drafting_tools

if __name__ == "__main__":
    register()
