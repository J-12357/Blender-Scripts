import bpy

def create_gold_ball():
    # Delete existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    sphere = bpy.context.object
    sphere.name = "GoldBall"
    
    # Apply smooth shading
    bpy.ops.object.shade_smooth()
    
    # Create a new material
    mat = bpy.data.materials.new(name="GoldMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    # Set gold color properties
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (1.0, 0.843, 0.0, 1)  # Gold color
        bsdf.inputs["Metallic"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.2  # Adjust for shininess

    # Assign material to the sphere
    sphere.data.materials.append(mat)

create_gold_ball()
