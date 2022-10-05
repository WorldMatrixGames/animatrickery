import bpy
from mathutils import Matrix, Euler

from math import pi

from .bone_controller_listeners import animatrickery_bone_rotator


class BoneControllerPanel(bpy.types.Panel):
    bl_idname = "animatrickery.bone_controller"
    bl_label = "Bone Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone"

    def draw(self, context):
        layout = self.layout
        active_pose_bone = context.active_pose_bone

        if not active_pose_bone:
            layout.label(text="Go into pose bone to view settings")
            return

        if not active_pose_bone.name in [registered_bone.name for registered_bone in context.scene.animatrickery_registered_pose_bones]:
            register_props = layout.operator(
                'animatrickery.manage_bone_rotaion_settings', text="Register Bone")
            register_props.action = 'REGISTER'
            register_props.bone_name = active_pose_bone.name
            return

        row0 = layout.row()
        row1 = layout.row()
        row2 = layout.row()

        row0.column().prop(context.scene,
                           'animatrickery_bone_controller_start_frame', text="Start Frame")
        row0.column().prop(context.scene,
                           'animatrickery_bone_controller_stop_frame', text="Stop Frame")

        row1.label(text="Keyframe rotation(euler)")
        record_props = row1.operator(
            'animatrickery.manage_bone_rotaion_settings', text="Play")
        record_props.action = 'PLAY'

        row2.label(text="Keyframe rotation(euler)")
        record_props = row2.operator(
            'animatrickery.manage_bone_rotaion_settings', text="Record")
        record_props.action = 'RECORD'

        data_grid = layout.grid_flow(columns=2).split(factor=0.8)
        data_column = data_grid.column()
        op_column = data_grid.column()

        offset_row = layout.row()
        offset_row.column().label(text="Offset")
        offset_row.column().prop(active_pose_bone, 'animatrickery_bone_controller_frame_offset')
        offset_row.column().operator('animatrickery.copy_bone_rotation_settings').offset = active_pose_bone.animatrickery_bone_controller_frame_offset
        info_row = layout.row().split(factor=.9)
        info_row.column().label(text="No. of items " +
                                str(len(active_pose_bone.animatrickery_rotation_settings)))
        op_add_props = info_row.column().operator(
            'animatrickery.manage_bone_rotaion_settings', text="+")
        op_add_props.action = 'ADD'

        for (idx, bone_settings) in enumerate(active_pose_bone.animatrickery_rotation_settings):
            column = data_column.row().split(factor=.1)
            column.label(text=str(bone_settings.frame))
            column.row().prop(bone_settings, 'rotation')

            op_grid = op_column.grid_flow(columns=2)
            op_props = op_grid.column().operator(
                'animatrickery.manage_bone_rotaion_settings', text="Set Frame")
            op_props.action = 'SET_FRAME'
            op_props.idx = idx

            op_remove_props = op_grid.column().operator(
                'animatrickery.manage_bone_rotaion_settings', text="-")
            op_remove_props.action = 'REMOVE'
            op_remove_props.idx = idx

        layout.prop(context.scene, "frame_current")
        layout.prop(context.active_pose_bone, "rotation_euler")
        set_rotation_props = layout.operator(
            'animatrickery.manage_bone_rotaion_settings', text="Set Frame Rotation")
        set_rotation_props.action = 'SET_ROTATION'
        set_rotation_props.idx = len(
            active_pose_bone.animatrickery_rotation_settings) - 1


class ManageBoneRotationSettings(bpy.types.Operator):
    bl_idname = 'animatrickery.manage_bone_rotaion_settings'
    bl_label = "Manager Bone Rotation Settings"

    action: bpy.props.StringProperty()
    idx: bpy.props.IntProperty()
    bone_name: bpy.props.StringProperty()

    def execute(self, context):
        if self.action == 'SET_FRAME':
            context.active_pose_bone.animatrickery_rotation_settings[
                self.idx].frame = context.scene.frame_current

        elif self.action == 'ADD':
            context.active_pose_bone.animatrickery_rotation_settings.add()

        elif self.action == 'REMOVE':
            context.active_pose_bone.animatrickery_rotation_settings.remove(
                self.idx)

        elif self.action == 'PLAY':
            context.scene.animatrickery_bone_controller_record = False
            context.scene.animatrickery_bone_controller_play = not context.scene.animatrickery_bone_controller_play
            toggle_bone_controller_listener(
                context.scene.animatrickery_bone_controller_play)
            context.scene.frame_current = context.scene.animatrickery_bone_controller_start_frame

        elif self.action == 'RECORD':
            context.scene.animatrickery_bone_controller_record = not context.scene.animatrickery_bone_controller_record
            context.scene.frame_current = context.scene.animatrickery_bone_controller_start_frame
            toggle_bone_controller_listener(
                context.scene.animatrickery_bone_controller_record)

        elif self.action == 'SET_ROTATION':
            active_pose_bone = context.active_pose_bone
            setting = context.active_pose_bone.animatrickery_rotation_settings[self.idx]
            print(setting)
            setting.rotation[0] = active_pose_bone.rotation_euler.x * 180 / pi
            setting.rotation[1] = active_pose_bone.rotation_euler.y * 180 / pi
            setting.rotation[2] = active_pose_bone.rotation_euler.z * 180 / pi

        elif self.action == 'REGISTER':
            if self.bone_name in [registered_bone.name for registered_bone in context.scene.animatrickery_registered_pose_bones]:
                return {'FINISHED'}
            context.scene.animatrickery_registered_pose_bones.add()
            context.scene.animatrickery_registered_pose_bones[-1].name = self.bone_name

        return {'FINISHED'}


class CopyRotationSettings(bpy.types.Operator):
    bl_idname = 'animatrickery.copy_bone_rotation_settings'
    bl_label = "Copy Bone Rotation Settings"

    offset: bpy.props.FloatProperty()

    def execute(self, context):
        active_pose_bone = context.active_pose_bone

        if (len(context.selected_pose_bones) < 2 or not active_pose_bone):
            return {'CANCELLED'}

        for bone in context.selected_pose_bones:
            if bone == active_pose_bone:
                continue

            bpy.ops.animatrickery.manage_bone_rotaion_settings(
                action='REGISTER', bone_name=bone.name)
            print("Registered(Copy)::" + bone.name)

            bone.animatrickery_rotation_settings.clear()

            if self.offset == 0:
                bone.animatrickery_rotation_settings = [
                    setting for setting in active_pose_bone.animatrickery_rotation_settings]
            else:
                start_frame = context.scene.animatrickery_bone_controller_start_frame
                end_frame = context.scene.animatrickery_bone_controller_stop_frame

                settings_with_offset = [
                    add_offset_to_rotation_setting(setting, self.offset) for setting in active_pose_bone.animatrickery_rotation_settings if (setting.frame + self.offset) <= end_frame
                ]
                setting_wrap_around = [
                    wrap_around(add_offset_to_rotation_setting(
                        setting, self.offset), end_frame - start_frame)
                    for (idx, setting) in enumerate(active_pose_bone.animatrickery_rotation_settings) if (setting.frame + self.offset) > end_frame and not idx == len(active_pose_bone.animatrickery_rotation_settings) - 1
                ]
                setting_wrap_around.extend(settings_with_offset)
            
            
            bone.animatrickery_rotation_settings.add()
            bone.animatrickery_rotation_settings[0].frame = 0
                
            for setting in setting_wrap_around:
                bone.animatrickery_rotation_settings.add()
                bone.animatrickery_rotation_settings[-1].frame = setting['frame']
                bone.animatrickery_rotation_settings[-1].rotation = setting['rotation']

            if not setting_wrap_around[-1]['frame'] == end_frame:
                split_fraction = (end_frame - setting_wrap_around[-1]['frame']) / ((end_frame - setting_wrap_around[-1]['frame']) + setting_wrap_around[0]['frame'])
                bone.animatrickery_rotation_settings.add()
                bone.animatrickery_rotation_settings[-1].frame = end_frame
                rotation_end = setting_wrap_around[0]['rotation']
                rotation_start = setting_wrap_around[-1]['rotation']
                rotation_first_split = Euler((
                    (rotation_end[0] + rotation_start[0]) * (1-split_fraction),
                    (rotation_end[1] + rotation_start[1]) * (1-split_fraction),
                    (rotation_end[2] + rotation_start[2]) * (1-split_fraction)
                ))
                bone.animatrickery_rotation_settings[-1].rotation = rotation_first_split
                bone.animatrickery_rotation_settings[0].rotation = rotation_first_split
            else:
                rotation_end = setting_wrap_around[-1]['rotation']
                bone.animatrickery_rotation_settings[0].rotation = Euler((
                    (rotation_end[0]),
                    -(rotation_end[1]),
                    -(rotation_end[2])
                ))

        return {'FINISHED'}


def add_offset_to_rotation_setting(setting, offset):
    temp = {}
    temp['frame'] = setting.frame + offset
    temp['rotation'] = Euler((setting.rotation[0], -setting.rotation[1], -setting.rotation[2]))
    return temp


def wrap_around(setting, range):
    temp = {}
    temp['frame'] = setting['frame'] - range
    temp['rotation'] = Euler((setting['rotation'][0], setting['rotation'][1], setting['rotation'][2]))
    return temp


def toggle_bone_controller_listener(switch):
    if switch:
        try:
            bpy.app.handlers.frame_change_pre.index(animatrickery_bone_rotator)
        except:
            bpy.app.handlers.frame_change_pre.append(
                animatrickery_bone_rotator)

        bpy.ops.screen.animation_play()
    else:
        try:
            bpy.app.handlers.frame_change_pre.index(animatrickery_bone_rotator)
            bpy.app.handlers.frame_change_pre.remove(
                animatrickery_bone_rotator)
        except:
            pass
        bpy.ops.screen.animation_cancel()
