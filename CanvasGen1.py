# Section 0 - Blender Addon Info
bl_info = {
    "name": "Canvas Gen",
    "blender": (4, 2, 1),
    "category": "Architecture",
    "author": "JPG",
    "description": "Addon provides a tab to input four specific verticies to create a plane. The plane then has cloth settings applied and the 4 corners of the plane are pinned in place",
    "version": (1, 0, 5),
}

# Section 1 - Imports
import bpy
import bmesh
import json
import os
from mathutils import Vector
from bpy.props import FloatProperty, IntProperty, PointerProperty, BoolProperty, EnumProperty

#Section 2 - File Path for Presets
PRESET_FILE_PATH = os.path.join(bpy.utils.user_resource('CONFIG'), "cloth_presets.json")

#Section 3 - Load and Save Presets
def load_presets():
    """This loads the fabric presets from JSON file."""
    if not os.path.exists(PRESET_FILE_PATH):
        return {}
    
    with open(PRESET_FILE_PATH, 'r') as file:
        return json.load(file)

def save_presets(presets):
    """Save fabric presets to JSON file"""
    with open(PRESET_FILE_PATH, 'w') as file:
        json.dump(presets, file, indent=4)

fabric_presets = load_presets()

# Section 4 - Property Group for Vertex Data  
class AncPoints(bpy.types.PropertyGroup):
    def update_plane(self, context):
        create_plane_from_anchors(context)
    
    def update_cloth_settings(self, context):
        obj = bpy.data.objects.get("Canvas1")
        if obj and obj.modifiers.get("Cloth"):
            cloth_mod = obj.modifiers["Cloth"]
            cloth_mod.settings.mass = self.cloth_mass
            cloth_mod.settings.bending_stiffness = self.cloth_bending_stiffness
            cloth_mod.settings.air_damping = self.cloth_air_damping
            cloth_mod.settings.use_self_collision =self.cloth_self_collision

    anc_pointsx_one: FloatProperty(name="Define Anchor Points 1 X", default=-1.0, update=update_plane)
    anc_pointsy_one: FloatProperty(name="Define Anchor Points 1 Y", default=-1.0, update=update_plane)
    anc_pointsz_one: FloatProperty(name="Define Anchor Points 1 Z", default=0.0, update=update_plane)

    anc_pointsx_two: FloatProperty(name="Define Anchor Points 2 X", default=1.0, update=update_plane)
    anc_pointsy_two: FloatProperty(name="Define Anchor Points 2 Y", default=-1.0, update=update_plane)
    anc_pointsz_two: FloatProperty(name="Define Anchor Points 2 Z", default=0.0, update=update_plane)

    anc_pointsx_three: FloatProperty(name="Define Anchor Points 3 X", default=1.0, update=update_plane)
    anc_pointsy_three: FloatProperty(name="Define Anchor Points 3 Y", default=1.0, update=update_plane)
    anc_pointsz_three: FloatProperty(name="Define Anchor Points 3 Z", default=0.0, update=update_plane)

    anc_pointsx_four: FloatProperty(name="Define Anchor Points 4 X", default=-1.0, update=update_plane)
    anc_pointsy_four: FloatProperty(name="Define Anchor Points 4 Y", default=1.0, update=update_plane)
    anc_pointsz_four: FloatProperty(name="Define Anchor Points 4 Z", default=0.0, update=update_plane)

    subdivision: IntProperty(name="Subdivision Levels", default=10, min=0, max=100, update=update_plane)

    cloth_mass: FloatProperty(name="Cloth Mass", default=1.0, min=0.1, max=10.0, update=update_cloth_settings)
    cloth_bending_stiffness: FloatProperty(name="Bending Stiffness", default=0.5, min=0.0, max=1.0, update=update_cloth_settings)
    cloth_air_damping: FloatProperty(name="Air Damping", default=5.0, min=0.0, max=10.0, update=update_cloth_settings)
    cloth_self_collision: BoolProperty(name="Enable Self Collision", default=False, update=update_cloth_settings)

    preset_name: bpy.props.StringProperty(name="Preset Name", default="NewPreset")
    available_presets: EnumProperty(
        name="Saved Presets",
        items=lambda self, context: [(k, k, "") for k in fabric_presets.keys()],
        description="Select a preset to load"
    )

# Section 5 - Operator to Save Presets
class MESH_OT_save_preset(bpy.types.Operator):
    bl_idname = "mesh.save_preset"
    bl_label = "Save Preset"
    bl_description = "Save the current cloth settings as a preset"

    def execute(self, context):
        props = context.scene.v_props
        fabric_presets[props.present_name] = {
            "mass": props.cloth_mass,
            "bending_stiffness": props.cloth_bending_stiffness,
            "air_damping": props.cloth_air_damping,
            "slef_collision": props.cloth_slef_collision
        }
        save_presets(fabric_presets)
        return {'FINISHED'}

# Section 6 - Operator to Load Presets
class MESH_OT_load_preset(bpy.types.Operator):
    bl_idname = "mesh.load_presets"
    bl_label = "Load Presets"
    bl_description = "Loads a saved fabric preset"

    def execute(self, context):
        props = context.scene.v_props
        preset_data = fabric_presets.get(props.available_presets)
        if preset_data:
            props.cloth_mass = preset_data["mass"]
            props.cloth_bending_stiffness = preset_data["bending_stiffness"]
            props.cloth_air_damping = preset_data["air_damping"]
            props.cloth_self_collision = preset_data["self_collision"]
        return {'FINISHED'}

# Section 7 - Function to Create Plane from Anchor Points and Applys Cloth and Pin Settings
def create_plane_from_anchors(context):
    props = context.scene.v_props
    obj_name = "Canvas1"

    old_obj = bpy.data.objects.get(obj_name)
    if old_obj:
        bpy.data.meshes.remove(old_obj.data)
        bpy.data.objects.remove(old_obj, do_unlink=True)

    mesh = bpy.data.meshes.new(name=obj_name)
    obj = bpy.data.objects.new(name=obj_name, object_data=mesh)
    context.collection.objects.link(obj)
    context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    v1 = bm.verts.new(Vector((props.anc_pointsx_one, props.anc_pointsy_one, props.anc_pointsz_one)))
    v2 = bm.verts.new(Vector((props.anc_pointsx_two, props.anc_pointsy_two, props.anc_pointsz_two)))
    v3 = bm.verts.new(Vector((props.anc_pointsx_three, props.anc_pointsy_three, props.anc_pointsz_three)))
    v4 = bm.verts.new(Vector((props.anc_pointsx_four, props.anc_pointsy_four, props.anc_pointsz_four)))

    bm.faces.new([v1, v2, v3, v4])
    bm.to_mesh(mesh)
    bm.free()

    if props.subdivision > 0:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=props.subdivision)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    vg_corners = obj.vertex_groups.new(name="Corners")

    mesh = obj.data
    corner_indices = [0, 1, 2, 3]
    vg_corners.add(corner_indices, 1.0, 'REPLACE')

    cloth_mod = obj.modifiers.new(name="Cloth", type='CLOTH')
    cloth_mod.settings.vertex_group_mass = vg_corners.name
    cloth_mod.settings.mass = props.cloth_mass
    cloth_mod.settings.bending_stiffness = props.cloth_bending_stiffness
    cloth_mod.settings.air_damping = props.cloth_air_damping
    cloth_mod.collision_settings.use_self_collision = props.cloth_self_collision

class MESH_OT_create_plane_from_anchors(bpy.types.Operator):
    bl_idname = "mesh.create_plane_from_anchors"
    bl_label = "Generate Canvas"
    bl_description = "Creates a cloth-simulated plane using four defined points"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_plane_from_anchors(context)
        return {'FINISHED'}

# Section 4 - UI Panel
class AncToPlane_Panel(bpy.types.Panel):
    bl_label = "Create Plane from Defined Points"
    bl_idname = "VIEW3D_PT_anc_plane"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vert to Plane"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Define Plane Verticies:")
        
        split = layout.split()

        col = split.column(align=True)
        col.label(text="Anchor 1")
        col.prop(scene.v_props, "anc_pointsx_one")
        col.prop(scene.v_props, "anc_pointsy_one")
        col.prop(scene.v_props, "anc_pointsz_one")

        col = split.column(align=True)
        col.label(text="Anchor 2")
        col.prop(scene.v_props, "anc_pointsx_two")
        col.prop(scene.v_props, "anc_pointsy_two")
        col.prop(scene.v_props, "anc_pointsz_two")

        col = split.column(align=True)
        col.label(text="Anchor 3")
        col.prop(scene.v_props, "anc_pointsx_three")
        col.prop(scene.v_props, "anc_pointsy_three")
        col.prop(scene.v_props, "anc_pointsz_three")

        col = split.column(align=True)
        col.label(text="Anchor 4")
        col.prop(scene.v_props, "anc_pointsx_four")
        col.prop(scene.v_props, "anc_pointsy_four")
        col.prop(scene.v_props, "anc_pointsz_four")

        box = layout.box()
        box.label(text="Subdivisions")
        box.prop(scene.v_props, "subdivision")

        box = layout.box()
        box.label(text="Cloth Settings")
        box.prop(scene.v_props, "cloth_mass")
        box.prop(scene.v_props, "cloth_bending_stiffness")
        box.prop(scene.v_props, "cloth_air_damping")
        box.prop(scene.v_props, "cloth_self_collision")

        box = layout.box()
        box.label(text="Fabric Presets")
        box.prop(scene.v_props, "preset_name")
        box.operator("mesh.save_preset")
        box.prop(scene.v_props, "available_presets")
        box.operator("mesh.load_preset")

        layout.operator("mesh.create_plane_from_anchors")

# Section 8 - Registration
classes = [AncPoints, MESH_OT_create_plane_from_anchors,AncToPlane_Panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.v_props = bpy.props.PointerProperty(type=AncPoints)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.v_props

if __name__ == "__main__":
    register()