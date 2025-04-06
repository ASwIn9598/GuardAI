import os
from .models import RecordedVideo
from django.core.files import File

def save_video_to_database(video_path):
    try:
        with open(video_path, 'rb') as f:
            video_file = File(f)
            new_video = RecordedVideo.objects.create(name=os.path.basename(video_path), video_file=video_file)
            return {"status": "success", "message": "Video saved successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to save video: {str(e)}"}





# import os
# import subprocess
# from django.core.files import File
# from .models import RecordedVideo

# import cv2

# def convert_avi_to_mp4(input_path):
#     """ Convert .avi to .mp4 using OpenCV """
#     try:
#         cap = cv2.VideoCapture(input_path)
        
#         # Get the video frame properties
#         frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = cap.get(cv2.CAP_PROP_FPS)
        
#         # Initialize VideoWriter for mp4 output
#         output_path = input_path.rsplit('.', 1)[0] + ".mp4"
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
#         out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             out.write(frame)
        
#         cap.release()
#         out.release()
#         return output_path
#     except Exception as e:
#         print(f"OpenCV conversion failed: {e}")
#         return None



# def save_video_to_database(video_path):
#     """ Save video to database, converting to .mp4 if needed """
#     try:
#         # Convert if the file is an .avi
#         if video_path.endswith('.avi'):
#             converted_path = convert_avi_to_mp4(video_path)
#             if converted_path:
#                 video_path = converted_path  # Use the converted .mp4 file

#         # Save the video to the database
#         with open(video_path, 'rb') as f:
#             video_file = File(f)
#             new_video = RecordedVideo(name=os.path.basename(video_path))
#             new_video.video_file.save(os.path.basename(video_path), video_file)  # Save explicitly
#             new_video.save()  # Ensure it is saved to DB

#         return {"status": "success", "message": "Video saved successfully"}
    
#     except Exception as e:
#         return {"status": "error", "message": f"Failed to save video: {str(e)}"}
