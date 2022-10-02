
if "bpy" in locals():
    import importlib
    importlib.reload(bone_controller_types)
    importlib.reload(bone_controller_ui)
    importlib.reload(bone_controller_listeners)
else:
    from . import bone_controller_types
    from . import bone_controller_ui
    from . import bone_controller_listeners

import bpy

bl_info = {
    "name": "Animatrickery - Bone Controller",
    "blender": (3, 0, 0),
    "category": "Animation",
}

def register():
    bpy.types.Scene.animatrickery_bone_controller_play = bpy.props.BoolProperty()
    bpy.types.Scene.animatrickery_bone_controller_record = bpy.props.BoolProperty()
    bpy.types.Scene.animatrickery_bone_controller_start_frame = bpy.props.IntProperty()
    bpy.types.Scene.animatrickery_bone_controller_stop_frame = bpy.props.IntProperty()
    bpy.utils.register_class(bone_controller_types.FrameRangeSelectionForBoneRotation)
    bpy.utils.register_class(bone_controller_types.AnimatrickeryBoneRegistrationDetails)
    bpy.types.Scene.animatrickery_registered_pose_bones = bpy.props.CollectionProperty(type=bone_controller_types.AnimatrickeryBoneRegistrationDetails)
    bpy.utils.register_class(bone_controller_ui.ManageBoneRotationSettings)
    bpy.types.PoseBone.animatrickery_rotation_settings = bpy.props.CollectionProperty(type=bone_controller_types.FrameRangeSelectionForBoneRotation)
    bpy.utils.register_class(bone_controller_ui.BoneControllerPanel)

    print("Bone controller module registered")

def unregister():
    bpy.utils.unregister_class(bone_controller_ui.BoneControllerPanel)
    bpy.utils.unregister_class(bone_controller_ui.ManageBoneRotationSettings)
    bpy.utils.unregister_class(bone_controller_types.AnimatrickeryBoneRegistrationDetails)
    bpy.utils.unregister_class(bone_controller_types.FrameRangeSelectionForBoneRotation)