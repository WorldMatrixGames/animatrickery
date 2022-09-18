import bpy;
from animatrickery_core import FrameRangeSelector;

bpy.types.Curve.animatrickery_frame_ranges = bpy.props.CollectionProperty(type=FrameRangeSelector)

registered_curves_key = 'animatrickery_registered_curves'

bl_info = {
    "name": "Animatrickery - Curve Controller",
    "blender": (3, 0, 0),
    "category": "Animation",
}

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
        if registered_curves_key not in context.scene:
            row = layout.row()
            row.label(text="Activate Curve Controller")
            layout.row().operator('animatrickery.curve_controller_actions_manager').action = 'activate'
            return

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
            column1 = row.column()
            column2 = row.column()

            column1.prop(frame_range, "start_frame")
            column2.prop(frame_range, "end_frame")

        row_add_range = layout.row()
        row_add_range.operator('animatrickery.add_frame_range')

class CurveControllerActionsManager(bpy.types.Operator):
    bl_idname = 'animatrickery.curve_controller_actions_manager'
    bl_label = 'Curve Controller Actions Manager'
    
    action_enums = {
        ('activate', "Activate", "Activate Curve Controller for this scene"),
        ('deactivate', "Deactivate", "Deactivate Curve Controller for this scene")
    }

    action: bpy.props.EnumProperty(items=action_enums)

    def execute(self, context):
        if self.action == 'activate':
            context.scene.animatrickery_curves.add()
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        
        

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

def curve_controller_animation_handler(scene):
    pass

def register():
    bpy.utils.register_class(AddRange)
    bpy.utils.register_class(AnimatrickeryCurveDetails)
    bpy.utils.register_class(RegisterCurveWithController)
    bpy.utils.register_class(CurveControllerActionsManager)
    bpy.utils.register_class(CurveController)
    register_types()

      
def unregister():
    bpy.utils.unregister_class(CurveController)
    bpy.utils.unregister_class(CurveControllerActionsManager)
    bpy.utils.unregister_class(RegisterCurveWithController)
    bpy.utils.unregister_class(AnimatrickeryCurveDetails)
    bpy.utils.unregister_class(AddRange)

def register_types():
    bpy.types.Scene.animatrickery_curves = bpy.props.CollectionProperty(type=AnimatrickeryCurveDetails)