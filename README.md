📸 Smart Camera Rig Generator for Blender

The Smart Camera Rig Generator is a powerful Blender add-on that instantly creates professional, production-ready camera rigs with automated controls, constraints, and custom properties. Perfect for animators, cinematographers, and VFX artists looking to speed up their camera work.

✨ Features

This add-on provides four pre-built camera systems and two utility functions:

    Basic Rig: A standard Aim-and-Dolly rig with separate controls for movement and focus. Great for most shots.

    Crane Rig: Simulates a jib or crane shot with controls for base rotation (pan) and boom elevation (tilt). Ideal for sweeping or overhead movements.

    Orbit Rig: Creates a camera that perfectly orbits a central target, allowing for easy turntable shots or circular movements.

    Handheld Rig: Instantly adds procedural, controllable camera shake/noise to simulate realistic handheld footage.

    Utility: Add DOF Controls: Quickly adds an automatically linked Focus Target Empty and custom properties to any selected camera for easy Depth of Field control.

    Utility: Add Camera Shake: Applies procedural noise modifiers to the selected camera's location/rotation for quick shake effects.

📦 Installation (The Blender Add-on Method)

    Download: Download the latest version of the script file (smart_camera_rig_generator.py) from this repository.

    Open Blender: Go to Edit → Preferences → Add-ons.

    Install: Click the Install... button at the top right and navigate to the downloaded .py file.

    Enable: After installation, ensure the checkbox next to "Camera: Smart Camera Rig Generator" is selected.

🚀 How to Use

The generator is located in the 3D Viewport Sidebar (press the N key) under the "Camera Rigs" tab.

    Select a Rig: Choose the type of camera rig you want to create (Basic, Crane, Orbit, or Handheld).

    Adjust Settings: Modify the initial parameters (e.g., Focal Length, Arm Length, Shake Amount) in the panel.

    Create: Click the corresponding "Create [Rig Type] Rig" button.

💡 Rig Controls Overview

The created objects are grouped into a new Collection and linked via constraints and drivers for smooth animation:
     Control Object (Empty)	Purpose
    [Rig Name]_Root / _Base	Master control. Move this to position the entire camera setup.
    [Rig Name]_Aim / _Center	Controls what the camera looks at (focus/tracking target).
    [Rig Name]_Dolly / _Arm	Moves the camera relative to the root/pivot. Used for distance control.
    Custom Properties	Look for custom properties (e.g., orbit_angle, fstop) in the Item tab of the rig controls for simplified animation sliders.

<h3>UI</h3>
<img width="239" height="574" alt="UI" src="https://github.com/user-attachments/assets/bc8477ee-4c9d-4700-88a5-eb608e7cf457" />

<h3>Basic Rig</h3> 
<img width="2561" height="1393" alt="Basic Rig" src="https://github.com/user-attachments/assets/64b6522d-f6bf-400d-bbaf-50dfac1239b9" />

<h3>Crane Rig</h3> 
<img width="2561" height="1393" alt="Crane Rig" src="https://github.com/user-attachments/assets/45a821c2-7f7b-4910-8ed4-373deef9d9bd" />

<h3>Orbit Rig</h3> 
<img width="2561" height="1393" alt="Orbit Rig" src="https://github.com/user-attachments/assets/1f23dbbe-c5fd-4a45-a0f6-0a1d9a951782" />

<h3>Handheld Rig</h3> 
<img width="2561" height="1393" alt="Handheld Rig" src="https://github.com/user-attachments/assets/701dcfe9-5c06-44cf-8ad8-cb4455ee51a9" />
