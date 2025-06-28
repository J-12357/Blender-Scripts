#Version 1.2

import bpy
import bmesh

def create_curtain_wall(width=5, height=10, columns=5, rows=5, mullion_thickness=0.1, mullion_depth=0.1):
    """Creates a 3D curtain wall with properly aligned and connected mullions."""

    # Cleanup: Delete existing objects with same name
    for obj_name in ["CurtainWall_Panels", "CurtainWall_Mullions"]:
        if obj_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

    # Create new mesh objects
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
    panel_width = (width - (columns - 1) * mullion_thickness) / columns
    panel_height = (height - (rows - 1) * mullion_thickness) / rows

    # Ensure dimensions are valid
    if panel_width <= 0 or panel_height <= 0:
        print("Error: Panel size is negative. Reduce mullion thickness or columns/rows.")
        return

    for col in range(columns):
        for row in range(rows):
            x_offset = col * (panel_width + mullion_thickness)
            z_offset = row * (panel_height + mullion_thickness)

            # Create Panel (Flat Surface)
            panel_verts = [
                (x_offset, 0, z_offset),
                (x_offset + panel_width, 0, z_offset),
                (x_offset + panel_width, 0, z_offset + panel_height),
                (x_offset, 0, z_offset + panel_height)
            ]
            panel_faces = [panel_bm.verts.new(v) for v in panel_verts]
            panel_bm.faces.new(panel_faces)

            # Create Vertical Mullion (Overlapping at intersections)
            if col <= columns:  # Extend last mullion at far right
                mullion_verts = [
                    (x_offset + panel_width, 0, z_offset - mullion_thickness),  # Extend past top
                    (x_offset + panel_width + mullion_thickness, 0, z_offset - mullion_thickness),
                    (x_offset + panel_width + mullion_thickness, 0, z_offset + panel_height + mullion_thickness),  # Extend past bottom
                    (x_offset + panel_width, 0, z_offset + panel_height + mullion_thickness),

                    (x_offset + panel_width, -mullion_depth, z_offset - mullion_thickness),
                    (x_offset + panel_width + mullion_thickness, -mullion_depth, z_offset - mullion_thickness),
                    (x_offset + panel_width + mullion_thickness, -mullion_depth, z_offset + panel_height + mullion_thickness),
                    (x_offset + panel_width, -mullion_depth, z_offset + panel_height + mullion_thickness)
                ]
                mullion_faces = [
                    [0, 1, 5, 4],  # Front face
                    [1, 2, 6, 5],  # Side face
                    [2, 3, 7, 6],  # Back face
                    [3, 0, 4, 7],  # Side face
                    [4, 5, 6, 7],  # Bottom face
                    [0, 1, 2, 3]   # Top face
                ]
                mullion_verts = [mullion_bm.verts.new(v) for v in mullion_verts]
                for face in mullion_faces:
                    mullion_bm.faces.new([mullion_verts[i] for i in face])

            # Create Horizontal Mullion (Overlapping at intersections)
            if row <= rows:  # Extend last mullion at the top
                mullion_verts = [
                    (x_offset - mullion_thickness, 0, z_offset + panel_height),
                    (x_offset + panel_width + mullion_thickness, 0, z_offset + panel_height),
                    (x_offset + panel_width + mullion_thickness, 0, z_offset + panel_height + mullion_thickness),
                    (x_offset - mullion_thickness, 0, z_offset + panel_height + mullion_thickness),

                    (x_offset - mullion_thickness, -mullion_depth, z_offset + panel_height),
                    (x_offset + panel_width + mullion_thickness, -mullion_depth, z_offset + panel_height),
                    (x_offset + panel_width + mullion_thickness, -mullion_depth, z_offset + panel_height + mullion_thickness),
                    (x_offset - mullion_thickness, -mullion_depth, z_offset + panel_height + mullion_thickness)
                ]
                mullion_faces = [
                    [0, 1, 5, 4],  # Front face
                    [1, 2, 6, 5],  # Side face
                    [2, 3, 7, 6],  # Back face
                    [3, 0, 4, 7],  # Side face
                    [4, 5, 6, 7],  # Bottom face
                    [0, 1, 2, 3]   # Top face
                ]
                mullion_verts = [mullion_bm.verts.new(v) for v in mullion_verts]
                for face in mullion_faces:
                    mullion_bm.faces.new([mullion_verts[i] for i in face])

    # Generate meshes
    panel_bm.to_mesh(panel_mesh)
    mullion_bm.to_mesh(mullion_mesh)

    # Free BMesh data
    panel_bm.free()
    mullion_bm.free()

    print("Curtain wall with seamless 3D mullions created successfully!")

# Call the function
create_curtain_wall()
