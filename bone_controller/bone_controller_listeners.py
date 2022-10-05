import bpy
from mathutils import Matrix

from math import pi

def animatrickery_bone_rotator(scene):
    frame_current = scene.frame_current

    for registration in scene.animatrickery_registered_pose_bones:
        pose_bone = bpy.context.object.pose.bones[registration.name]
        
        if not len(pose_bone.animatrickery_rotation_settings):
            continue

        for (idx, rotation_setting) in enumerate(pose_bone.animatrickery_rotation_settings):
            if idx == len(pose_bone.animatrickery_rotation_settings) - 1:
                break

            if  frame_current >= rotation_setting.frame and  frame_current <= pose_bone.animatrickery_rotation_settings[idx+1].frame:
                frame_range = scene.animatrickery_bone_controller_stop_frame - scene.animatrickery_bone_controller_start_frame
                
                start_rotation = rotation_setting.rotation
                end_rotation = pose_bone.animatrickery_rotation_settings[idx+1].rotation
                
                start_frame =  rotation_setting.frame
                end_frame = pose_bone.animatrickery_rotation_settings[idx+1].frame
                
                # Pure calculation to reduce complexity
                pose_bone.matrix_basis = Matrix.Identity(4)

                start_mat_rot_x = Matrix.Rotation(start_rotation[0] * pi / 180, 4, 'X')
                start_mat_rot_y = Matrix.Rotation(start_rotation[1] * pi / 180, 4, 'Y')
                start_mat_rot_z = Matrix.Rotation(start_rotation[2] * pi / 180, 4, 'Z')

                end_mat_rot_x = Matrix.Rotation(end_rotation[0] * pi / 180, 4, 'X')
                end_mat_rot_y = Matrix.Rotation(end_rotation[1] * pi / 180, 4, 'Y')
                end_mat_rot_z = Matrix.Rotation(end_rotation[2] * pi / 180, 4, 'Z')

                start = start_mat_rot_x @ pose_bone.matrix_basis
                start = start_mat_rot_y @ start
                start = start_mat_rot_z @ start

                end = end_mat_rot_x @ pose_bone.matrix_basis
                end = end_mat_rot_y @ end
                end = end_mat_rot_z @ end


                new_rot = start.lerp(end, (frame_current - start_frame) / (end_frame - start_frame))

                pose_bone.matrix_basis = new_rot

                if scene.animatrickery_bone_controller_record:
                    pose_bone.keyframe_insert('rotation_euler', frame=frame_current)

                    if scene.animatrickery_bone_controller_record and frame_current == scene.animatrickery_bone_controller_stop_frame:
                        bpy.ops.screen.animation_cancel()
                        bpy.app.handlers.frame_change_pre.remove(animatrickery_bone_rotator)
                