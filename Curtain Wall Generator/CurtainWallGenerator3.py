bl_info = {
    "name": "Curtain Wall Generator",
    "blender": (4, 0, 0),
    "category": "Object",
    "author": "JPG",
    "version": (1, 3),
    "location": "View3D > Sidebar > Curtain Wall Generator",
    "description": "Generates a parametric curtain wall with adjustable settings",
}

import bpy
import bmesh

class CurtainWallProperties(bpy.types.PropertyGroup):
    width: bpy.props.FloatProperty(name="Width", default=5.0, min=1.0, description="Total width of the curtain wall")
    height: bpy.props.FloatProperty(name="Height", default=10.0, min=1.0, description="Total height of the curtain wall")
    columns: bpy.props.IntProperty(name="Columns", default=5, min=1, description="Number of panel columns")
    rows: bpy.props.IntProperty(name="Rows", default=5, min=1, description="Number of panel rows")
    mullion_thickness: bpy.props.FloatProperty(name="Mullion Thickness", default=0.1, min=0.01, description="Thickness of mullions")
    mullion_depth: bpy.props.FloatProperty(name="Mullion Depth", default=0.1, min=0.01, description="Depth of mullions")

def create_curtain_wall(width, height, columns, rows, mullion_thickness, mullion_depth):
    """Creates a 3D curtain wall with seamless mullions and panels."""

    # Cleanup old curtain wall objects
    for obj_name in ["CurtainWall_Panels", "CurtainWall_Mullions"]:
        if obj_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

    # Create new meshes
    panel_mesh = bpy.data.meshes.new("CurtainWall_Panels_Mesh")
    mullion_mesh = bpy.data.meshes.new("CurtainWall_Mullions_Mesh")

    panel_obj = bpy.data.objects.new("CurtainWall_Panels", panel_mesh)
    mullion_obj = bpy.data.objects.new("CurtainWall_Mullions", mullion_mesh)

    bpy.context.collection.objects.link(panel_obj)
    bpy.context.collection.objects.link(mullion_obj)

    # Create BMesh objects
    panel_bm = bmesh.new()
    mullion_bm = bmesh.new()

    # Compute panel and mullion dimensions
    panel_width = (width - (columns + 1) * mullion_thickness) / columns
    panel_height = (height - (rows + 1) * mullion_thickness) / rows

    # Ensure dimensions are valid
    if panel_width <= 0 or panel_height <= 0:
        print("Error: Panel size is negative. Reduce mullion thickness or columns/rows.")
        return

    for col in range(columns + 1):  # Add extra column for closing the frame
        for row in range(rows + 1):  # Add extra row for closing the frame
            x_offset = col * (panel_width + mullion_thickness)
            z_offset = row * (panel_height + mullion_thickness)

            # Create Panel (Skip last row/column since it's only for mullions)
            if col < columns and row < rows:
                panel_verts = [
                    (x_offset, 0, z_offset),
                    (x_offset + panel_width, 0, z_offset),
                    (x_offset + panel_width, 0, z_offset + panel_height),
                    (x_offset, 0, z_offset + panel_height)
                ]
                panel_faces = [panel_bm.verts.new(v) for v in panel_verts]
                panel_bm.faces.new(panel_faces)

            # Create Vertical Mullions
            mullion_verts = [
                (x_offset, 0, z_offset - mullion_thickness),  
                (x_offset + mullion_thickness, 0, z_offset - mullion_thickness),
                (x_offset + mullion_thickness, 0, z_offset + panel_height + mullion_thickness),
                (x_offset, 0, z_offset + panel_height + mullion_thickness),

                (x_offset, -mullion_depth, z_offset - mullion_thickness),
                (x_offset + mullion_thickness, -mullion_depth, z_offset - mullion_thickness),
                (x_offset + mullion_thickness, -mullion_depth, z_offset + panel_height + mullion_thickness),
                (x_offset, -mullion_depth, z_offset + panel_height + mullion_thickness)
            ]
            mullion_faces = [[0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7], [4, 5, 6, 7], [0, 1, 2, 3]]
            mullion_verts = [mullion_bm.verts.new(v) for v in mullion_verts]
            for face in mullion_faces:
                mullion_bm.faces.new([mullion_verts[i] for i in face])

    # Generate meshes
    panel_bm.to_mesh(panel_mesh)
    mullion_bm.to_mesh(mullion_mesh)

    # Free BMesh data
    panel_bm.free()
    mullion_bm.free()

    print("Curtain wall created successfully!")

class GenerateCurtainWall(bpy.types.Operator):
    bl_idname = "object.generate_curtain_wall"
    bl_label = "Generate Curtain Wall"
    
    def execute(self, context):
        props = context.scene.curtain_wall_props
        create_curtain_wall(
            props.width, props.height, props.columns, props.rows, props.mullion_thickness, props.mullion_depth
        )
        return {'FINISHED'}

class CurtainWallPanel(bpy.types.Panel):
    bl_label = "Curtain Wall Generator"
    bl_idname = "OBJECT_PT_curtain_wall"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Curtain Wall"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.curtain_wall_props

        layout.prop(props, "width")
        layout.prop(props, "height")
        layout.prop(props, "columns")
        layout.prop(props, "rows")
        layout.prop(props, "mullion_thickness")
        layout.prop(props, "mullion_depth")
        
        layout.operator("object.generate_curtain_wall")

def register():
    bpy.utils.register_class(CurtainWallProperties)
    bpy.utils.register_class(GenerateCurtainWall)
    bpy.utils.register_class(CurtainWallPanel)
    bpy.types.Scene.curtain_wall_props = bpy.props.PointerProperty(type=CurtainWallProperties)

def unregister():
    bpy.utils.unregister_class(CurtainWallProperties)
    bpy.utils.unregister_class(GenerateCurtainWall)
    bpy.utils.unregister_class(CurtainWallPanel)
    del bpy.types.Scene.curtain_wall_props

if __name__ == "__main__":
    register()
