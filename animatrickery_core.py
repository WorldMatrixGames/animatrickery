import bpy;

bl_info = {
    "name": "Animatrickery - Core",
    "blender": (3, 0, 0),
    "category": "Animation",
}

class FrameRangeSelector(bpy.types.PropertyGroup):
    start_frame: bpy.props.IntProperty(name="Start Frame")
    end_frame: bpy.props.IntProperty(name="End Frame")


def register():
    bpy.utils.register_class(FrameRangeSelector)


def unregister():
    bpy.utils.unregister_class(FrameRangeSelector)