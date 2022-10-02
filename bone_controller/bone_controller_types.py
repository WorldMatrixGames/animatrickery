import bpy

from animatrickery_core import FrameRangeSelector

class FrameRangeSelectionForBoneRotation(bpy.types.PropertyGroup):
    rotation: bpy.props.FloatVectorProperty()
    frame: bpy.props.IntProperty()



class AnimatrickeryBoneRegistrationDetails(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()