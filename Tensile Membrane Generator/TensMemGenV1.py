bl_info = {
    "name": "Tensile Membrane Structure Generator",
    "blender": (4, 2, 1),
    "category": "Object",
    "author": "John",
    "description": "Generates a tensile membrane structure with cloth simulation.",
}

import bpy
import bmesh
from bpy.props import FloatProperty, IntProperty

class TensileGeneratorOperator(bpy.types.Operator):
    bl_idname = "object.tensile_membrane_generate"
    bl_label = "Generate Tensile Structure"
    
    size: FloatProperty(name="Size", default=5.0, min=1.0, max=10.0)
    resolution: IntProperty(name="Resolution", default=20, min=5, max=100)
    pole_height: FloatProperty(name="Pole Height", default=3.0, min=1.0, max=10.0)
    
    def execute(self, context):
        self.create_base_mesh()
        self.create_support_poles()
        return {'FINISHED'}
    
    def create_base_mesh(self):
        mesh = bpy.data.meshes.new("TensileMesh")
        obj = bpy.data.objects.new("TensileStructure", mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=self.resolution, y_segments=self.resolution, size=self.size)
        bm.to_mesh(mesh)
        bm.free()
        
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        self.apply_cloth_simulation(obj)
    
    def apply_cloth_simulation(self, obj):
        cloth = obj.modifiers.new(name="TensileCloth", type='CLOTH')
        cloth.settings.mass = 0.5
        cloth.settings.structural_stiffness = 15
        cloth.settings.bending_stiffness = 0.1
        cloth.settings.use_pressure = True
        cloth.settings.uniform_pressure_force = 5

    def create_support_poles(self):
        for x in [-self.size/2, self.size/2]:
            for y in [-self.size/2, self.size/2]:
                bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=self.pole_height, location=(x, y, self.pole_height / 2))

class TensilePanel(bpy.types.Panel):
    bl_label = "Tensile Membrane Generator"
    bl_idname = "OBJECT_PT_tensile_membrane"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tensile Membrane'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.tensile_membrane_generate")

classes = [TensileGeneratorOperator, TensilePanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()