import bpy;
from animatrickery_core import FrameRangeSelector;

bpy.types.Curve.animatrickery_frame_ranges = bpy.props.CollectionProperty(type=FrameRangeSelector)

bl_info = {
    "name": "Animatrickery - Curve Controller",
    "blender": (3, 0, 0),
    "category": "Animation",
}

class CurveController(bpy.types.Panel):
    bl_idname = "animatrickery.curve_controller"
    bl_label = "Curve Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout;
        if(context.active_object.type != 'CURVE'):
            row = layout.row()
            row.label(text="Select a curve to add frame data")
            return
        
        curve = context.active_object.data
        for frame_range in curve.animatrickery_frame_ranges:
            row = layout.row()
            
            column1 = row.column()
            column2 = row.column()

            column1.prop(frame_range, "start_frame")
            column2.prop(frame_range, "end_frame")
        row_add_range = layout.row()
        row_add_range.operator('animatrickery.add_frame_range')


class AddRange(bpy.types.Operator):
    bl_idname = "animatrickery.add_frame_range"
    bl_label = "Add Frame Range"

    def execute(self, context):
        frame_current = context.scene.frame_current
        curve_active = context.active_object
        
        curve_active.data.animatrickery_frame_ranges.add()

        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(AddRange)
    bpy.utils.register_class(CurveController)

      
def unregister():
    bpy.utils.unregister_class(CurveController)
    bpy.utils.unregister_class(AddRange)