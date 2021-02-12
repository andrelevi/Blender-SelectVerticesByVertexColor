bl_info = {
    "name": "Select Vertices by Vertex Color",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class select_red_vertices(bpy.types.Operator):
    bl_idname = "object.select_red_vertices"
    bl_label = "Select Vertices - Red"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        select_vertices_with_color(0, 0.5)
        return {'FINISHED'}

class select_green_vertices(bpy.types.Operator):
    bl_idname = "object.select_green_vertices"
    bl_label = "Select Vertices - Green"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        select_vertices_with_color(1, 0.5)
        return {'FINISHED'}

class select_blue_vertices(bpy.types.Operator):
    bl_idname = "object.select_blue_vertices"
    bl_label = "Select Vertices - Blue"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        select_vertices_with_color(2, 0.5)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(select_red_vertices)
    bpy.utils.register_class(select_green_vertices)
    bpy.utils.register_class(select_blue_vertices)

def unregister():
    bpy.utils.unregister_class(select_red_vertices)
    bpy.utils.unregister_class(select_green_vertices)
    bpy.utils.unregister_class(select_blue_vertices)

def select_vertices_with_color(color_channel, threshold):
    ob = bpy.context.object

    if ob == None:
        return

    if ob.type != 'MESH':
        return

    print('Selecting vertex colors for channel: ' + str(color_channel) + ' with threshold: ' + str(threshold))

    bpy.ops.object.mode_set(mode="OBJECT")

    loops = len(ob.data.loops)
    verts = len(ob.data.vertices)
    visited_vertices = verts * [False]
    
    # Go through each vertex color layer.
    for vcol in ob.data.vertex_colors:
        # Look into each loop's vertex.
        for l in range(loops):
            vertex_index = ob.data.loops[l].vertex_index
            color = vcol.data[l].color

            if not visited_vertices[vertex_index]:
                visited_vertices[vertex_index] = True

                # Test if the vertex's color channel is above the threshold.
                if color[color_channel] >= threshold:
                    print('Selecting vertex index: ' + str(vertex_index) + ' with channel value of: ' + str(color[color_channel]))
                    ob.data.vertices[vertex_index].select = True
                else:
                    ob.data.vertices[vertex_index].select = False

    bpy.ops.object.mode_set(mode="EDIT")

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()