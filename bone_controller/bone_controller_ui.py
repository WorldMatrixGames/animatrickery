import bpy
from mathutils import Matrix, Euler
from math import pi

class BoneControllerPanel(bpy.types.Panel):
    bl_idname = "animatrickery.bone_controller"
    bl_label = "Bone Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone"

    def draw(self, context):
        layout = self.layout

        if not context.active_pose_bone:
            layout.label(text="Go into pose bone to view settings")

        grid = layout.grid_flow(columns = 2)
        frame_range_column = grid.column()
        angle_change_range_column = grid.column()
        
        angle_change_range_column.label(text="Column 0")
        frame_range_column.label(text="Column 1")

        edit_section_grid = layout.grid_flow(columns = 2)
        frame_edit_section = edit_section_grid.column()
        angle_change_edit_section = edit_section_grid.column()

        for b in context.active_pose_bone.animatrickery_rotation_settings:
            row = layout.row()
            row.prop(b, 'start_angle')

        layout.prop(context.scene, "frame_current")


def register_ui_classes():
    bpy.utils.register_class(BoneControllerPanel)
    print("Registered bone controller panel related classes")

    
def unregister_ui_classes():
    bpy.utils.unregister_class(BoneControllerPanel)