bl_info = {
    "name": "Parametric Brick Wall",
    "blender": (4, 2, 1),
    "category": "Mesh",
    "author": "JPG",
    "description": "Creates a customizable parametric brick wall.",
    "version": (1, 2),
}

import bpy
import bmesh
import math
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty


class ParametricBrickWallProperties(bpy.types.PropertyGroup):
    wall_length: FloatProperty(name="Wall Length", default=5.0, min=0.5)
    wall_height: FloatProperty(name="Wall Height", default=5.0, min=0.5)
    brick_width: FloatProperty(name="Brick Width", default=0.7, min=0.1)
    brick_height: FloatProperty(name="Brick Height", default=0.35, min=0.1)
    brick_depth: FloatProperty(name="Brick Depth", default=0.3, min=0.1)
    brick_gap: FloatProperty(name="Brick Gap (Mortar)", default=0.05, min=0.0)
    stagger_rows: BoolProperty(name="Stagger Rows", default=True)
    
    # New Features
    curved_wall: BoolProperty(name="Curved Wall", default=False)
    wall_radius: FloatProperty(name="Wall Radius", default=3.0, min=1.0)
    angled_wall: BoolProperty(name="Angled Wall", default=False)
    wall_angle: FloatProperty(name="Wall Angle (°)", default=0.0, min=-45.0, max=45.0)
    
    # Materials
    brick_color: FloatVectorProperty(
        name="Brick Color", subtype="COLOR", default=(0.6, 0.2, 0.1, 1), min=0, max=1, size=4
    )
    mortar_color: FloatVectorProperty(
        name="Mortar Color", subtype="COLOR", default=(0.8, 0.8, 0.8, 1), min=0, max=1, size=4
    )


class ParametricBrickWallOperator(bpy.types.Operator):
    bl_idname = "mesh.parametric_brick_wall"
    bl_label = "Generate Brick Wall"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.parametric_brick_wall
        self.create_brick_wall(context, props)
        return {'FINISHED'}

    def create_brick_wall(self, context, props):
        # Delete old wall if it exists
        old_wall = bpy.data.objects.get("BrickWall")
        if old_wall:
            bpy.data.objects.remove(old_wall, do_unlink=True)

        # Calculate rows and columns
        cols = int(props.wall_length / (props.brick_width + props.brick_gap))
        rows = int(props.wall_height / (props.brick_height + props.brick_gap))

        # Create a new mesh and object
        mesh = bpy.data.meshes.new("BrickWallMesh")
        obj = bpy.data.objects.new("BrickWall", mesh)
        context.collection.objects.link(obj)

        bm = bmesh.new()

        # Create bricks
        for row in range(rows):
            for col in range(cols):
                angle_offset = 0
                if props.curved_wall:
                    angle_offset = (col / cols) * (math.pi * 2 * (props.wall_length / (2 * math.pi * props.wall_radius)))
                    x_offset = props.wall_radius * math.sin(angle_offset)
                    y_offset = props.wall_radius * math.cos(angle_offset) - props.wall_radius
                else:
                    x_offset = col * (props.brick_width + props.brick_gap)
                    y_offset = 0
                
                z_offset = row * (props.brick_height + props.brick_gap)

                # Stagger every other row
                if props.stagger_rows and row % 2 == 1:
                    x_offset += (props.brick_width + props.brick_gap) / 2

                # Apply inclination if angled wall is enabled
                if props.angled_wall:
                    z_offset += math.tan(math.radians(props.wall_angle)) * x_offset

                # Create a single brick
                self.create_brick(bm, x_offset, y_offset, z_offset, props)

        # Finalize mesh
        bm.to_mesh(mesh)
        bm.free()
        obj.select_set(True)
        context.view_layer.objects.active = obj

        # Apply materials
        self.apply_material(obj, props)

    def create_brick(self, bm, x, y, z, props):
        """Creates a single brick at position (x, y, z)"""
        d = props.brick_depth
        w = props.brick_width
        h = props.brick_height

        verts = [
            bm.verts.new((x, y, z)),       # Bottom left front
            bm.verts.new((x + w, y, z)),   # Bottom right front
            bm.verts.new((x + w, y + d, z)),   # Bottom right back
            bm.verts.new((x, y + d, z)),       # Bottom left back
            bm.verts.new((x, y, z + h)),   # Top left front
            bm.verts.new((x + w, y, z + h)),  # Top right front
            bm.verts.new((x + w, y + d, z + h)),  # Top right back
            bm.verts.new((x, y + d, z + h)),      # Top left back
        ]

        # Create faces
        faces = [
            [0, 1, 2, 3],  # Bottom
            [4, 5, 6, 7],  # Top
            [0, 1, 5, 4],  # Front
            [1, 2, 6, 5],  # Right
            [2, 3, 7, 6],  # Back
            [3, 0, 4, 7],  # Left
        ]

        for face in faces:
            bm.faces.new([verts[i] for i in face])

    def apply_material(self, obj, props):
        """Creates and applies materials for bricks and mortar"""
        mat = bpy.data.materials.new(name="BrickMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = props.brick_color

        obj.data.materials.append(mat)


class ParametricBrickWallPanel(bpy.types.Panel):
    bl_label = "Parametric Brick Wall"
    bl_idname = "VIEW3D_PT_parametric_brick_wall"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Parametric Wall"

    def draw(self, context):
        layout = self.layout
        props = context.scene.parametric_brick_wall

        layout.prop(props, "wall_length")
        layout.prop(props, "wall_height")
        layout.prop(props, "brick_width")
        layout.prop(props, "brick_height")
        layout.prop(props, "brick_depth")
        layout.prop(props, "brick_gap")
        layout.prop(props, "stagger_rows")

        layout.separator()
        layout.prop(props, "curved_wall")
        if props.curved_wall:
            layout.prop(props, "wall_radius")

        layout.prop(props, "angled_wall")
        if props.angled_wall:
            layout.prop(props, "wall_angle")

        layout.separator()
        layout.prop(props, "brick_color")
        layout.prop(props, "mortar_color")

        layout.operator("mesh.parametric_brick_wall", text="Generate Brick Wall")


classes = [
    ParametricBrickWallProperties,
    ParametricBrickWallOperator,
    ParametricBrickWallPanel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.parametric_brick_wall = bpy.props.PointerProperty(type=ParametricBrickWallProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.parametric_brick_wall


if __name__ == "__main__":
    register()
