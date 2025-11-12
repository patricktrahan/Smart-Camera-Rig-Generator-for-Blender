"""
Smart Camera Rig Generator for Blender
Creates professional camera rigs with empties, constraints, and custom properties
Perfect for animation, cinematics, and VFX work

To use: 
1. Open Blender's Text Editor
2. Paste this script
3. Click "Run Script" or press Alt+P
4. Find the panel in 3D View sidebar (N key) under "Camera Rigs"
"""

import bpy
import math
from mathutils import Vector, Euler

bl_info = {
    "name": "Smart Camera Rig Generator",
    "author": "Patrick Trahan",
    "version": (1, 0),
    "blender": (4, 5, 1),
    "location": "View3D > Sidebar > Camera Rigs",
    "description": "Creates professional camera rigs with automated controls",
    "category": "Camera",
}


class CameraRigGenerator:
    """Main class for generating camera rigs"""
    
    @staticmethod
    def create_basic_rig(name="Camera_Rig", focal_length=50):
        """Create a basic camera rig with aim and dolly controls"""
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        
        # Create camera
        cam_data = bpy.data.cameras.new(name + "_Camera")
        cam_data.lens = focal_length
        cam_obj = bpy.data.objects.new(name + "_Camera", cam_data)
        collection.objects.link(cam_obj)
        
        # Create aim target (what camera looks at)
        aim_empty = bpy.data.objects.new(name + "_Aim", None)
        aim_empty.empty_display_type = 'SPHERE'
        aim_empty.empty_display_size = 0.5
        aim_empty.location = (0, 0, 0)
        collection.objects.link(aim_empty)
        
        # Create dolly control (moves camera forward/back along aim direction)
        dolly_empty = bpy.data.objects.new(name + "_Dolly", None)
        dolly_empty.empty_display_type = 'SINGLE_ARROW'
        dolly_empty.empty_display_size = 1.0
        dolly_empty.location = (0, -5, 2)
        collection.objects.link(dolly_empty)
        
        # Create root control (master control)
        root_empty = bpy.data.objects.new(name + "_Root", None)
        root_empty.empty_display_type = 'CUBE'
        root_empty.empty_display_size = 1.5
        root_empty.location = (0, 0, 0)
        collection.objects.link(root_empty)
        
        # Setup hierarchy
        aim_empty.parent = root_empty
        dolly_empty.parent = root_empty
        cam_obj.parent = dolly_empty
        
        # Add Track To constraint (camera looks at aim)
        track_constraint = cam_obj.constraints.new('TRACK_TO')
        track_constraint.target = aim_empty
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'
        
        # Add custom properties for easy control
        root_empty["rig_version"] = "1.0"
        cam_obj["focal_length"] = focal_length
        cam_obj["dof_enabled"] = 0
        cam_obj["dof_distance"] = 5.0
        
        # Make camera active
        bpy.context.scene.camera = cam_obj
        
        return {
            'camera': cam_obj,
            'aim': aim_empty,
            'dolly': dolly_empty,
            'root': root_empty,
            'collection': collection
        }
    
    @staticmethod
    def create_crane_rig(name="Crane_Rig", arm_length=5, height=3):
        """Create a crane/jib camera rig"""
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        
        # Create camera
        cam_data = bpy.data.cameras.new(name + "_Camera")
        cam_obj = bpy.data.objects.new(name + "_Camera", cam_data)
        collection.objects.link(cam_obj)
        
        # Create crane base
        base_empty = bpy.data.objects.new(name + "_Base", None)
        base_empty.empty_display_type = 'CUBE'
        base_empty.empty_display_size = 1.0
        base_empty.location = (0, 0, 0)
        collection.objects.link(base_empty)
        
        # Create crane pivot (rotation point)
        pivot_empty = bpy.data.objects.new(name + "_Pivot", None)
        pivot_empty.empty_display_type = 'ARROWS'
        pivot_empty.empty_display_size = 0.8
        pivot_empty.location = (0, 0, height)
        pivot_empty.parent = base_empty
        collection.objects.link(pivot_empty)
        
        # Create crane arm
        arm_empty = bpy.data.objects.new(name + "_Arm", None)
        arm_empty.empty_display_type = 'SINGLE_ARROW'
        arm_empty.empty_display_size = 1.5
        arm_empty.location = (0, -arm_length, 0)
        arm_empty.parent = pivot_empty
        collection.objects.link(arm_empty)
        
        # Create aim target
        aim_empty = bpy.data.objects.new(name + "_Aim", None)
        aim_empty.empty_display_type = 'SPHERE'
        aim_empty.empty_display_size = 0.5
        aim_empty.location = (0, 0, 0)
        aim_empty.parent = base_empty
        collection.objects.link(aim_empty)
        
        # Parent camera to arm
        cam_obj.parent = arm_empty
        
        # Add Track To constraint
        track_constraint = cam_obj.constraints.new('TRACK_TO')
        track_constraint.target = aim_empty
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'
        
        # Add custom properties
        base_empty["crane_rotation"] = 0.0
        pivot_empty["crane_tilt"] = 0.0
        arm_empty["boom_height"] = 0.0
        
        # Add drivers for intuitive control
        CameraRigGenerator._add_rotation_driver(pivot_empty, base_empty, "crane_rotation", 'Z')
        CameraRigGenerator._add_rotation_driver(arm_empty, pivot_empty, "crane_tilt", 'X')
        
        bpy.context.scene.camera = cam_obj
        
        return {
            'camera': cam_obj,
            'base': base_empty,
            'pivot': pivot_empty,
            'arm': arm_empty,
            'aim': aim_empty,
            'collection': collection
        }
    
    @staticmethod
    def create_orbit_rig(name="Orbit_Rig", distance=5, height=2):
        """Create an orbit camera rig (rotates around a point)"""
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        
        # Create camera
        cam_data = bpy.data.cameras.new(name + "_Camera")
        cam_obj = bpy.data.objects.new(name + "_Camera", cam_data)
        collection.objects.link(cam_obj)
        
        # Create orbit center
        center_empty = bpy.data.objects.new(name + "_Center", None)
        center_empty.empty_display_type = 'SPHERE'
        center_empty.empty_display_size = 0.3
        center_empty.location = (0, 0, height)
        collection.objects.link(center_empty)
        
        # Create rotation control
        rotation_empty = bpy.data.objects.new(name + "_Rotation", None)
        rotation_empty.empty_display_type = 'CIRCLE'
        rotation_empty.empty_display_size = 1.0
        rotation_empty.location = (0, 0, height)
        collection.objects.link(rotation_empty)
        
        # Create distance control
        distance_empty = bpy.data.objects.new(name + "_Distance", None)
        distance_empty.empty_display_type = 'SINGLE_ARROW'
        distance_empty.empty_display_size = 1.0
        distance_empty.location = (0, -distance, 0)
        distance_empty.parent = rotation_empty
        collection.objects.link(distance_empty)
        
        # Parent camera
        cam_obj.parent = distance_empty
        
        # Add Track To constraint
        track_constraint = cam_obj.constraints.new('TRACK_TO')
        track_constraint.target = center_empty
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'
        
        # Add custom properties
        rotation_empty["orbit_angle"] = 0.0
        rotation_empty["orbit_height"] = height
        distance_empty["orbit_distance"] = distance
        
        bpy.context.scene.camera = cam_obj
        
        return {
            'camera': cam_obj,
            'center': center_empty,
            'rotation': rotation_empty,
            'distance': distance_empty,
            'collection': collection
        }
    
    @staticmethod
    def create_handheld_rig(name="Handheld_Rig", shake_amount=0.05):
        """Create a handheld camera rig with procedural shake"""
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        
        # Create camera
        cam_data = bpy.data.cameras.new(name + "_Camera")
        cam_obj = bpy.data.objects.new(name + "_Camera", cam_data)
        collection.objects.link(cam_obj)
        
        # Create shake controller
        shake_empty = bpy.data.objects.new(name + "_Shake", None)
        shake_empty.empty_display_type = 'ARROWS'
        shake_empty.empty_display_size = 0.5
        shake_empty.location = (0, -5, 2)
        collection.objects.link(shake_empty)
        
        # Create root
        root_empty = bpy.data.objects.new(name + "_Root", None)
        root_empty.empty_display_type = 'CUBE'
        root_empty.empty_display_size = 1.0
        root_empty.location = (0, 0, 0)
        collection.objects.link(root_empty)
        
        # Setup hierarchy
        shake_empty.parent = root_empty
        cam_obj.parent = shake_empty
        
        # Add custom properties
        shake_empty["shake_amount"] = shake_amount
        shake_empty["shake_speed"] = 1.0
        shake_empty["shake_enabled"] = 1
        
        # Add noise modifier via drivers (simplified approach)
        # In production, you'd use the Noise modifier on animation
        shake_empty["note"] = "Animate shake_amount to control intensity"
        
        bpy.context.scene.camera = cam_obj
        
        return {
            'camera': cam_obj,
            'shake': shake_empty,
            'root': root_empty,
            'collection': collection
        }
    
    @staticmethod
    def _add_rotation_driver(obj, control_obj, prop_name, axis):
        """Add a driver to control rotation via custom property"""
        driver = obj.driver_add('rotation_euler', 'XYZ'.index(axis)).driver
        var = driver.variables.new()
        var.name = "rotation_control"
        var.targets[0].id_type = 'OBJECT'
        var.targets[0].id = control_obj
        var.targets[0].data_path = f'["{prop_name}"]'
        driver.expression = f"radians({var.name})"
    
    @staticmethod
    def add_dof_controls(camera_obj, focus_distance=5.0):
        """Add depth of field controls to camera"""
        if camera_obj.type != 'CAMERA':
            return False
        
        cam_data = camera_obj.data
        
        # Enable DOF
        cam_data.dof.use_dof = True
        cam_data.dof.focus_distance = focus_distance
        cam_data.dof.aperture_fstop = 2.8
        
        # Create focus target
        focus_empty = bpy.data.objects.new(camera_obj.name + "_Focus", None)
        focus_empty.empty_display_type = 'SPHERE'
        focus_empty.empty_display_size = 0.2
        focus_empty.location = camera_obj.location + Vector((0, 0, -focus_distance))
        
        bpy.context.scene.collection.objects.link(focus_empty)
        
        # Link DOF to empty
        cam_data.dof.focus_object = focus_empty
        
        # Add custom properties
        camera_obj["fstop"] = 2.8
        camera_obj["focus_distance"] = focus_distance
        
        return focus_empty
    
    @staticmethod
    def add_camera_shake(camera_obj, amount=0.05, frequency=4.0):
        """Add procedural camera shake using noise modifiers"""
        if not camera_obj.animation_data:
            camera_obj.animation_data_create()
        
        # Add noise to location
        for i, axis in enumerate(['X', 'Y', 'Z']):
            fcurve = camera_obj.animation_data.drivers.from_existing(src_driver=None)
            if not fcurve:
                # Create keyframes first if no animation exists
                camera_obj.keyframe_insert(data_path="location", index=i, frame=1)
                camera_obj.keyframe_insert(data_path="location", index=i, frame=2)
                fcurve = camera_obj.animation_data.action.fcurves[i]
            
            # Add noise modifier
            noise_mod = fcurve.modifiers.new('NOISE')
            noise_mod.scale = frequency
            noise_mod.strength = amount
            noise_mod.phase = i * 100  # Offset each axis
        
        return True


class CAMERA_PT_RigPanel(bpy.types.Panel):
    """Panel in 3D View sidebar"""
    bl_label = "Camera Rig Generator"
    bl_idname = "CAMERA_PT_rig_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera Rigs'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Basic Rig
        box = layout.box()
        box.label(text="Basic Camera Rig", icon='CAMERA_DATA')
        row = box.row()
        row.prop(scene, "rig_name")
        row = box.row()
        row.prop(scene, "rig_focal_length")
        row = box.row()
        row.operator("camera.create_basic_rig", icon='ADD')
        
        # Crane Rig
        box = layout.box()
        box.label(text="Crane Camera Rig", icon='EMPTY_SINGLE_ARROW')
        row = box.row()
        row.prop(scene, "crane_arm_length")
        row = box.row()
        row.prop(scene, "crane_height")
        row = box.row()
        row.operator("camera.create_crane_rig", icon='ADD')
        
        # Orbit Rig
        box = layout.box()
        box.label(text="Orbit Camera Rig", icon='FORCE_MAGNETIC')
        row = box.row()
        row.prop(scene, "orbit_distance")
        row = box.row()
        row.prop(scene, "orbit_height")
        row = box.row()
        row.operator("camera.create_orbit_rig", icon='ADD')
        
        # Handheld Rig
        box = layout.box()
        box.label(text="Handheld Camera Rig", icon='ORIENTATION_VIEW')
        row = box.row()
        row.prop(scene, "shake_amount")
        row = box.row()
        row.operator("camera.create_handheld_rig", icon='ADD')
        
        # Utilities
        layout.separator()
        box = layout.box()
        box.label(text="Utilities", icon='TOOL_SETTINGS')
        row = box.row()
        row.operator("camera.add_dof_controls", icon='OUTLINER_OB_CAMERA')
        row = box.row()
        row.operator("camera.add_camera_shake", icon='FORCE_TURBULENCE')


class CAMERA_OT_CreateBasicRig(bpy.types.Operator):
    """Create a basic camera rig"""
    bl_idname = "camera.create_basic_rig"
    bl_label = "Create Basic Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        name = context.scene.rig_name
        focal = context.scene.rig_focal_length
        rig = CameraRigGenerator.create_basic_rig(name, focal)
        self.report({'INFO'}, f"Created camera rig: {name}")
        return {'FINISHED'}


class CAMERA_OT_CreateCraneRig(bpy.types.Operator):
    """Create a crane camera rig"""
    bl_idname = "camera.create_crane_rig"
    bl_label = "Create Crane Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        arm = context.scene.crane_arm_length
        height = context.scene.crane_height
        rig = CameraRigGenerator.create_crane_rig("Crane_Rig", arm, height)
        self.report({'INFO'}, "Created crane camera rig")
        return {'FINISHED'}


class CAMERA_OT_CreateOrbitRig(bpy.types.Operator):
    """Create an orbit camera rig"""
    bl_idname = "camera.create_orbit_rig"
    bl_label = "Create Orbit Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        distance = context.scene.orbit_distance
        height = context.scene.orbit_height
        rig = CameraRigGenerator.create_orbit_rig("Orbit_Rig", distance, height)
        self.report({'INFO'}, "Created orbit camera rig")
        return {'FINISHED'}


class CAMERA_OT_CreateHandheldRig(bpy.types.Operator):
    """Create a handheld camera rig"""
    bl_idname = "camera.create_handheld_rig"
    bl_label = "Create Handheld Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        shake = context.scene.shake_amount
        rig = CameraRigGenerator.create_handheld_rig("Handheld_Rig", shake)
        self.report({'INFO'}, "Created handheld camera rig")
        return {'FINISHED'}


class CAMERA_OT_AddDOF(bpy.types.Operator):
    """Add depth of field controls to selected camera"""
    bl_idname = "camera.add_dof_controls"
    bl_label = "Add DOF Controls"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if not context.active_object or context.active_object.type != 'CAMERA':
            self.report({'ERROR'}, "Please select a camera")
            return {'CANCELLED'}
        
        focus = CameraRigGenerator.add_dof_controls(context.active_object, 5.0)
        if focus:
            self.report({'INFO'}, "Added DOF controls")
            return {'FINISHED'}
        return {'CANCELLED'}


class CAMERA_OT_AddShake(bpy.types.Operator):
    """Add camera shake to selected camera"""
    bl_idname = "camera.add_camera_shake"
    bl_label = "Add Camera Shake"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if not context.active_object or context.active_object.type != 'CAMERA':
            self.report({'ERROR'}, "Please select a camera")
            return {'CANCELLED'}
        
        shake = context.scene.shake_amount
        success = CameraRigGenerator.add_camera_shake(context.active_object, shake, 4.0)
        if success:
            self.report({'INFO'}, "Added camera shake")
            return {'FINISHED'}
        return {'CANCELLED'}


# Registration
classes = (
    CAMERA_PT_RigPanel,
    CAMERA_OT_CreateBasicRig,
    CAMERA_OT_CreateCraneRig,
    CAMERA_OT_CreateOrbitRig,
    CAMERA_OT_CreateHandheldRig,
    CAMERA_OT_AddDOF,
    CAMERA_OT_AddShake,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add properties
    bpy.types.Scene.rig_name = bpy.props.StringProperty(
        name="Name",
        default="Camera_Rig"
    )
    bpy.types.Scene.rig_focal_length = bpy.props.FloatProperty(
        name="Focal Length",
        default=50.0,
        min=10.0,
        max=200.0
    )
    bpy.types.Scene.crane_arm_length = bpy.props.FloatProperty(
        name="Arm Length",
        default=5.0,
        min=1.0,
        max=20.0
    )
    bpy.types.Scene.crane_height = bpy.props.FloatProperty(
        name="Height",
        default=3.0,
        min=0.0,
        max=10.0
    )
    bpy.types.Scene.orbit_distance = bpy.props.FloatProperty(
        name="Distance",
        default=5.0,
        min=1.0,
        max=20.0
    )
    bpy.types.Scene.orbit_height = bpy.props.FloatProperty(
        name="Height",
        default=2.0,
        min=0.0,
        max=10.0
    )
    bpy.types.Scene.shake_amount = bpy.props.FloatProperty(
        name="Shake Amount",
        default=0.05,
        min=0.0,
        max=1.0
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.rig_name
    del bpy.types.Scene.rig_focal_length
    del bpy.types.Scene.crane_arm_length
    del bpy.types.Scene.crane_height
    del bpy.types.Scene.orbit_distance
    del bpy.types.Scene.orbit_height
    del bpy.types.Scene.shake_amount


if __name__ == "__main__":
    register()