import bpy;
from animatrickery_core import FrameRangeSelector;

registered_curves_key = 'animatrickery_registered_curves'

bl_info = {
    "name": "Animatrickery - Curve Controller",
    "blender": (3, 0, 0),
    "category": "Animation",
}


class FrameRangeSelectorForCurveRateSelection(FrameRangeSelector):
    rate: bpy.props.FloatProperty(name="Rate")

class AnimatrickeryCurveDetails(bpy.types.PropertyGroup):
    curve_name: bpy.props.StringProperty()

class CurveController(bpy.types.Panel):
    bl_idname = "animatrickery.curve_controller"
    bl_label = "Curve Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout
        active_object = context.active_object
        scene = context.scene
        
        row = layout.row()
        row.operator('animatrickery.toggle_frame_change_listeners')

        if(active_object.type != 'CURVE'):
            row = layout.row()
            row.label(text="Select a curve to add frame data")
            return
        
        registered_curves = context.scene.animatrickery_curves
        if active_object.name not in [_curve.curve_name for _curve in registered_curves]: 
            row = layout.row()
            row.label(text="Active Curve: " + active_object.name)
            layout.row().operator('animatrickery.register_curve_with_controller')
            return

        curve = active_object.data
        for frame_range in curve.animatrickery_frame_ranges:
            row = layout.row()
            column0 = row.column()
            column1 = row.column()
            column2 = row.column()

            column0.prop(frame_range, "rate")
            column1.prop(frame_range, "start_frame")
            column2.prop(frame_range, "end_frame")

        row_add_range = layout.row()
        row_add_range.operator('animatrickery.add_frame_range')

class AddRange(bpy.types.Operator):
    bl_idname = 'animatrickery.add_frame_range'
    bl_label = "Add Frame Range"

    def execute(self, context):
        frame_current = context.scene.frame_current
        curve_active = context.active_object
        
        curve_active.data.animatrickery_frame_ranges.add()

        return {'FINISHED'}


class RegisterCurveWithController(bpy.types.Operator):
    bl_idname = 'animatrickery.register_curve_with_controller'
    bl_label = "Register Curve with Controller"

    def execute(self, context):
        curve_active = context.active_object
        registered_curve = context.scene.animatrickery_curves.add()
        registered_curve.curve_name = curve_active.name
        

        return {'FINISHED'}

class ToggleFrameChangeListeners(bpy.types.Operator):
    bl_idname = 'animatrickery.toggle_frame_change_listeners'
    bl_label = "Toggle Frame Change Listeners"

    switch: bpy.props.BoolProperty()

    def execute(self, context):
        try:
            if context.scene.animatrickery_frame_change_pre_handler_running:
                bpy.app.handlers.frame_change_pre.remove(curve_controller_animation_handler)
        
            else:
                bpy.app.handlers.frame_change_pre.append(curve_controller_animation_handler)
        except:
            pass

        context.scene.animatrickery_frame_change_pre_handler_running = not context.scene.animatrickery_frame_change_pre_handler_running
        return {'FINISHED'}

def handle_currve_progression(scene, curve_data):
    
    frame_ranges = curve_data.animatrickery_frame_ranges
    init_frame = frame_ranges[0].start_frame
    frame_current = scene.frame_current

    if not len(curve_data.animatrickery_frame_ranges) or frame_current < init_frame:
        return
    
    active_range = None
    predecessor_range = None
    successor_range = None
    accumulated_eval_time = 0
    frame_range_len = len(frame_ranges)
    accP = 0
    accC = 0
    for (idx, range) in enumerate(frame_ranges):
        if range.end_frame < frame_current:
            accumulated_eval_time += (range.end_frame - range.start_frame) * range.rate

            if idx < frame_range_len - 1:
                next_range = frame_ranges[idx + 1]
                accumulated_eval_time += (range.end_frame - next_range.start_frame) * (next_range.rate - range.rate) / 2 
            accP = accumulated_eval_time
        else:
            active_range = range
            corrected_start_frame = max(active_range.start_frame, frame_ranges[idx - 1].end_frame)
            accumulated_eval_time += (frame_current - corrected_start_frame) * active_range.rate
            
            if idx < frame_range_len - 1:
                next_range = frame_ranges[idx + 1]

                if next_range.start_frame <= frame_current:
                    accumulated_eval_time += (frame_current - next_range.start_frame) * (next_range.rate - range.rate) * (frame_current - next_range.start_frame) / (2 * range.end_frame - next_range.start_frame)
            accC = accumulated_eval_time
            break
    print(accP, accC, accumulated_eval_time)
    curve_data.eval_time = accumulated_eval_time



def curve_controller_animation_handler(scene):
    for curve_details in scene.animatrickery_curves:
        print("Found", bpy.data.curves[curve_details.curve_name].name)
        handle_currve_progression(scene, bpy.data.curves[curve_details.curve_name])

def register():
    register_classes()
    register_types()

def unregister():
    unregister_classes()

def register_classes():
    bpy.utils.register_class(FrameRangeSelectorForCurveRateSelection)
    bpy.utils.register_class(AddRange)
    bpy.utils.register_class(AnimatrickeryCurveDetails)
    bpy.utils.register_class(RegisterCurveWithController)
    bpy.utils.register_class(CurveController)
    bpy.utils.register_class(ToggleFrameChangeListeners)

def unregister_classes():
    bpy.utils.register_class(ToggleFrameChangeListeners)
    bpy.utils.unregister_class(CurveController)
    bpy.utils.unregister_class(RegisterCurveWithController)
    bpy.utils.unregister_class(AnimatrickeryCurveDetails)
    bpy.utils.unregister_class(AddRange)
    bpy.utils.unregister_class(FrameRangeSelectorForCurveRateSelection)

def register_types():
    bpy.types.Curve.animatrickery_frame_ranges = bpy.props.CollectionProperty(type=FrameRangeSelectorForCurveRateSelection)
    bpy.types.Scene.animatrickery_curves = bpy.props.CollectionProperty(type=AnimatrickeryCurveDetails)
    bpy.types.Scene.animatrickery_frame_change_pre_handler_running = bpy.props.BoolProperty()
