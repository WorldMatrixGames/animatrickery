
if "bpy" in locals():
    import importlib
    importlib.reload(bone_controller_types)
    importlib.reload(bone_controller_ui)
else:
    from . import bone_controller_types
    from . import bone_controller_ui

import bpy

bl_info = {
    "name": "Animatrickery - Bone Controller",
    "blender": (3, 0, 0),
    "category": "Animation",
}

def register():
    bpy.utils.register_class(bone_controller_types.FrameRangeSelectionForBoneRotation)
    bpy.types.PoseBone.animatrickery_rotation_settings = bpy.props.CollectionProperty(type=bone_controller_types.FrameRangeSelectionForBoneRotation)
    bpy.utils.register_class(bone_controller_ui.BoneControllerPanel)

    print("Bone controller module registered")

def unregister():
    bpy.utils.unregister_class(bone_controller_ui.BoneControllerPanel)
    bpy.utils.unregister_class(bone_controller_types.FrameRangeSelectionForBoneRotation)