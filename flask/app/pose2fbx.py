import time
from fbx2publish import notifyFbx2Publish

def startPose2Fbx(id: str, type: str):
    print(f"############ Starting Pose2FBX for {id} of type {type}")
    time.sleep(3)
    print("############ FBX created")
    notifyFbx2Publish(id, type)