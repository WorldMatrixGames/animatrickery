import bpy

bl_info = {
    "name": "Animatrickery - Keyframe Inserter",
    "blender": (3, 0, 0),
    "category": "Animation",
}


class KeyframeInsertionPanel(bpy.types.Panel):
    bl_idname = "animatrickery.keyframe_insertion_panel"
    bl_label = "Keyframe Inserter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        frame_row = layout.row()
        start_frame_column = layout.column()
        start_frame_column.prop(context.scene, 'frame_start')
        start_frame_column.prop(context.scene, 'frame_end')

        rotaion_insert_ops_row = layout.row()
        rotaion_insert_ops_row.operator('animatrickery.insert_keyframes', text="Record rotations").type='rot'

        
        location_insert_ops_row = layout.row()
        rotaion_insert_ops_row.operator('animatrickery.insert_keyframes', text="Record locations").type='loc'

        
        rotaion_location_insert_ops_row = layout.row()
        rotaion_location_insert_ops_row.operator('animatrickery.insert_keyframes', text="Record location & rotations").type='locrot'

def check_animation_loop_completion(type):
    if bpy.context.scene.frame_current == bpy.context.scene.frame_end:
        bpy.ops.screen.animation_cancel()
        if type == 'loc':
            bpy.app.handlers.frame_change_post.remove(keyframeChangeLocListener)
        elif type == 'rot':
            bpy.app.handlers.frame_change_post.remove(keyframeChangeRotListener)
        elif type == 'locrot':
            bpy.app.handlers.frame_change_post.remove(keyframeChangeRotLocListener)

def keyframeChangeLocListener(scene):
    for bone in bpy.context.selected_pose_bones:
        bone.keyframe_insert('location', frame=scene.frame_current)
    check_animation_loop_completion('loc')

def keyframeChangeRotListener(scene):
    for bone in bpy.context.selected_pose_bones:
        bone.keyframe_insert('rotation_euler', frame=scene.frame_current)
    check_animation_loop_completion('rot')

def keyframeChangeRotLocListener(scene):
    for bone in bpy.context.selected_pose_bones:
        bone.keyframe_insert('location', frame=scene.frame_current)
        bone.keyframe_insert('rotation_euler', frame=scene.frame_current)
    check_animation_loop_completion('locrot')

class KeyframeInserter(bpy.types.Operator):
    bl_idname = 'animatrickery.insert_keyframes'
    bl_label = "Insert Keyframes"
    type: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.frame_current = context.scene.frame_start

        if self.type == 'loc':
            bpy.app.handlers.frame_change_post.append(keyframeChangeLocListener)
            bpy.ops.screen.animation_play()
        elif self.type == 'rot':
            bpy.app.handlers.frame_change_post.append(keyframeChangeRotListener)
            bpy.ops.screen.animation_play()
        elif self.type == 'locrot':
            bpy.app.handlers.frame_change_post.append(keyframeChangeRotLocListener)
            bpy.ops.screen.animation_play()

        return {'FINISHED'}
        


def register():
    bpy.utils.register_class(KeyframeInserter)
    bpy.utils.register_class(KeyframeInsertionPanel)

    
def unregister():
    bpy.utils.unregister_class(KeyframeInsertionPanel)
    bpy.utils.unregister_class(KeyframeInserter)

if __name__ == '__main__':
    register()