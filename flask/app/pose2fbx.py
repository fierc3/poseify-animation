import time
from fbx2publish import notifyFbx2Publish
import subprocess

def startPose2Fbx(id: str, type: str):
    print(f"############ Starting Pose2FBX for {id} of type {type}")
    
    # Converting original BVH to FBX
    convertBvhToFbx(f"{id}.bvh")

    # Converting T-pose BVH to FBX
    add_tpose_to_bvh(f"/poseify/{id}.bvh", f"/poseify/{id}.t.bvh")
    convertBvhToFbx(f"{id}.t.bvh")
    
    print("############ FBX created")
    notifyFbx2Publish(id, type)

def convertBvhToFbx(bvh_file_name: str):
    blender_command = ['/usr/local/blender', '--background', '--python', 'bvh2fbx.py', '--bvhFileLocation', f"/poseify/{bvh_file_name}"]
    # should equal => /usr/local/blender --background --python bvh2fbx.py --bvhFileLocation /workspaces/poseify-animation/flask/testdata/test.bvh

    try:
        result = subprocess.run(blender_command, check=True, capture_output=True, text=True)
        print("Blender executed successfully.")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running Blender:", e)
        print("Output:", e.stdout)
        print("Errors:", e.stderr)

def add_tpose_to_bvh(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()
    
    motion_index = next(i for i, line in enumerate(lines) if line.strip() == "MOTION")
    frames_index = motion_index + 1
    frame_time_index = motion_index + 2
    
    # Adjust frame count
    frames_line = lines[frames_index].strip().split(": ")
    if len(frames_line) == 2 and frames_line[0] == "Frames":
        frame_count = int(frames_line[1]) + 1
        lines[frames_index] = f"Frames: {frame_count}\n"
    
    # Generate a T-pose frame based on the number of values in the first original frame
    original_first_frame_values = len(lines[frame_time_index + 1].split())
    t_pose_frame = " ".join(["0.0"] * original_first_frame_values) + "\n"
    
    # Insert the T-pose frame
    lines.insert(frame_time_index + 1, t_pose_frame)
    
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(lines)
