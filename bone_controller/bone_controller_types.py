import bpy

from animatrickery_core import FrameRangeSelector

class FrameRangeSelectionForBoneRotation(FrameRangeSelector):
    start_angle: bpy.props.IntVectorProperty()
    end_angle: bpy.props.IntVectorProperty()

def define_types_on_pose_bone():
    bpy.types.PoseBone.animatrickery_rotation_settings = bpy.props.CollectionProperty(type=FrameRangeSelectionForBoneRotation)

def register_types():
    bpy.utils.register_class(FrameRangeSelectionForBoneRotation)
    define_types_on_pose_bone()
    print("Registered bone controller related types")


def unregister_types():
    bpy.utils.unregister_class(FrameRangeSelectionForBoneRotation)

