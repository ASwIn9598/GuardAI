# import cv2
# import torch
# import numpy as np
# import pathlib
# import pandas as pd  # Ensure pandas is imported for handling DataFrame outputs

# def run_yolo_webcam_detection(is_recording):
#     # Temporary fix for PosixPath issue on Windows
#     temp = pathlib.PosixPath
#     pathlib.PosixPath = pathlib.WindowsPath

#     try:
#         # Load the trained YOLO model
#         model = torch.hub.load(
#             "D:\\django projects\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5",  
#             "custom",
#             path="D:\\django projects\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5\\runs\\train\\exp10\\weights\\best.pt",
#             source="local"
#         )
#     except Exception as e:
#         return {"status": "error", "message": f"Failed to load the YOLO model: {e}"}

#     # Initialize webcam (use 0 for default webcam)
#     print("******************************")
#     cap = cv2.VideoCapture(0)

#     # Check if the webcam is accessible
#     if not cap.isOpened():
#         return {"status": "error", "message": "Unable to access the webcam."}
    
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     if fps == 0:  # Fallback if FPS is not provided by the webcam
#         fps = 30  # Default to 30 FPS

#     # Set video writer to save output
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     # out = cv2.VideoWriter('output_webcam.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (frame_width, frame_height))
#     out = cv2.VideoWriter('output_webcam.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))


#     detection_results = []

#     while is_recording[0]:  # Access the mutable state in the loop
#         ret, frame = cap.read()
#         if not ret:
#             break

#         try:
#             # Perform object detection
#             results = model(frame)

#             # Process the detections
#             if hasattr(results, 'pandas'):  # Check if pandas() is supported
#                 detections = results.pandas().xyxy[0]  # Get detection data as DataFrame
#             else:
#                 detections = results.xyxy[0].cpu().numpy()  # Fallback to tensor output

#             # Render results on the frame
#             frame = np.squeeze(results.render())
#             out.write(frame)

#             # Extract objects with confidence greater than 60%
#             if isinstance(detections, pd.DataFrame):  # If detections are a DataFrame
#                 high_confidence_detections = detections[detections['confidence'] > 0.6]
#                 labels = high_confidence_detections['name'].tolist()
#             elif isinstance(detections, np.ndarray):  # If detections are a NumPy array
#                 high_confidence_detections = detections[detections[:, 4] > 0.6]
#                 labels = [model.names[int(det[5])] for det in high_confidence_detections]
#             else:
#                 labels = []

#             if labels:
#                 print(f"High-confidence object detected: {labels}")
#                 detection_results.extend(labels)
#                 print("Stopping camera...")

#                 # Set the recording flag to False to stop the loop
#                 is_recording[0] = False  # This will stop the loop

#                 # Break out of the loop after object is detected
#                 break

#         except Exception as e:
#             print(f"Error during detection: {e}")
#             is_recording[0] = False
#             break

#         # Display the frame
#         cv2.imshow("Webcam Detection", frame)

#         # Check for key press (press 'q' to quit the loop)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Graceful exit
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

#     return {"status": "success", "detections": detection_results}





import cv2
import torch
import numpy as np
import pathlib
import pandas as pd  # Ensure pandas is imported for handling DataFrame outputs

def run_yolo_webcam_detection(is_recording, result):
    # Temporary fix for PosixPath issue on Windows
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

    try:
        # Load the trained YOLO model
        if result == "fire":
            model = torch.hub.load(
            "D:\\project\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5",  
            "custom",
            path="D:\\project\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5\\runs\\train\\exp10\\weights\\yolov5s_best.pt",
            source="local"
            )
        else:
            model = torch.hub.load(
            "D:\\project\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5",  
            "custom",
            path="D:\\project\\GUARDAI\\GUARDAI\\Reg\\frontend\\Dl\\yolov5\\runs\\train\\exp10\\weights\\best2.pt",
            source="local"
            )
    except Exception as e:
        return {"status": "error", "message": f"Failed to load the YOLO model: {e}"}

    # Initialize webcam (use 0 for default webcam)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is accessible
    if not cap.isOpened():
        return {"status": "error", "message": "Unable to access the webcam."}

    # Get the FPS of the webcam
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:  # If FPS is not provided by the webcam, default to 30 FPS
        fps = 30  

    # Set video writer to save output in proper MP4 format
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(
        'output_webcam.mp4', 
        cv2.VideoWriter_fourcc(*'avc1'),  # H.264 codec for MP4
        fps, 
        (frame_width, frame_height)
    )

    detection_results = []

    # Set the window to fullscreen
    cv2.namedWindow("Webcam Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Webcam Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while is_recording[0]:  # Access the mutable state in the loop
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # Perform object detection
            results = model(frame)

            # Process the detections
            if hasattr(results, 'pandas'):  # Check if pandas() is supported
                detections = results.pandas().xyxy[0]  # Get detection data as DataFrame
            else:
                detections = results.xyxy[0].cpu().numpy()  # Fallback to tensor output

            # Render results on the frame
            frame = np.squeeze(results.render())
            out.write(frame)  # Save the frame to the video file

            if result == 'fire':
                confi_threshold = 0.35
            else:
                confi_threshold = 0.78

            # Extract objects with confidence greater than 60%
            if isinstance(detections, pd.DataFrame):  # If detections are a DataFrame
                high_confidence_detections = detections[detections['confidence'] > confi_threshold]
                labels = high_confidence_detections['name'].tolist()
            elif isinstance(detections, np.ndarray):  # If detections are a NumPy array
                high_confidence_detections = detections[detections[:, 4] > 0.8]
                labels = [model.names[int(det[5])] for det in high_confidence_detections]
            else:
                labels = []

            if labels:
                print(f"High-confidence object detected: {labels}")
                detection_results.extend(labels)
                print("Stopping camera...")

                # Set the recording flag to False to stop the loop
                is_recording[0] = False  # This will stop the loop

                # Break out of the loop after object is detected
                break

        except Exception as e:
            print(f"Error during detection: {e}")
            is_recording[0] = False
            break

        # Display the frame
        cv2.imshow("Webcam Detection", frame)

        # Check for key press (press 'q' to quit the loop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Graceful exit
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return {"status": "success", "detections": detection_results}



