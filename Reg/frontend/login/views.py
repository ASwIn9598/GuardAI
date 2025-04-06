from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
import threading
import os
import cv2
import torch
from pathlib import Path
from login.models import AnalyzedVideo 
from django.conf import settings
from .models import *
import torch
from yolov5 import YOLOv5
from Dl.test import *
from django.views.decorators.csrf import csrf_exempt
import time
from django.http import StreamingHttpResponse
import pycurl
from urllib.parse import urlencode
from .utils import save_video_to_database




# Existing sends_mail function
def sends_mail(mail, msg):
    try:
        crl = pycurl.Curl()
        crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')  # Replace with your API URL
        data = {'email': mail, 'msg': msg}
        pf = urlencode(data)
        crl.setopt(crl.POSTFIELDS, pf)
        crl.perform()
        crl.close()
        print("Mail sent successfully")
    except Exception as e:
        print(f"Error sending mail: {e}")

detection_result = {"status": "Idle", "detections": []}

def check_detection(request):
    global detection_result
    return JsonResponse(detection_result)

def reset_detection(request):
    global detection_result
    detection_result = {"status": "Idle", "detections": []}
    return JsonResponse({"status": "Reset"})


def home(request):
    return render(request, 'index.html')


def history(request):
    result = RecordedVideo.objects.all().order_by
    return render(request, 'history.html', {'result': result})


recording_thread = None
is_recording = threading.Event() 





def start_detection(user_email, detection_type):
    global detection_result
    video_path = "output_webcam.mp4"  # Path to recorded video

    try:
        while is_recording.is_set():
            result = run_yolo_webcam_detection([is_recording.is_set()], detection_type)
            print("Detection result:", result)

            if result.get("status") == "success" and result.get("detections"):
                detection_result = {
                    "status": "Detected",
                    "detections": result["detections"]
                }

                # Save the recorded video to the database
                save_result = save_video_to_database(video_path)
                print(save_result)

                if user_email:
                    message = f"An object has been detected: {result['detections']}"
                    sends_mail(user_email, message)
                else:
                    print("No email provided. Cannot send email.")

                is_recording.clear()
                break
            else:
                detection_result = {"status": "Pending", "detections": []}

            time.sleep(0.1)
    except Exception as e:
        print(f"Error during detection: {e}")
        detection_result = {"status": "Error", "detections": []}
        is_recording.clear()
    finally:
        is_recording.clear()




def control_detection(request):
    global recording_thread

    if request.method == 'POST':
        detection_type = request.POST.get("type") 
        print("hhhhhhhhhhhhhhhhhhhhhhh",detection_type)

        if not is_recording.is_set():  # Start only if not already recording
            is_recording.set()  # Set the event to indicate recording has started
            
            # Get the user's email
            user_email = request.user.email if request.user.is_authenticated else None

            # Start the thread with the user's email
            recording_thread = threading.Thread(target=start_detection, args=(user_email, detection_type))
            recording_thread.daemon = True  # Ensure the thread exits with the main process
            recording_thread.start()
            return JsonResponse({'status': 'Recording started'})
        else:
            is_recording.clear()  # Stop the recording if already in progress
            if recording_thread:
                recording_thread.join(timeout=2)  # Wait for the thread to finish
            return JsonResponse({'status': 'Recording stopped'})

    return JsonResponse({'status': 'Invalid request'})



# def start_detection(user_email):
#     global detection_result
#     try:
#         while is_recording.is_set():
#             result = run_yolo_webcam_detection([is_recording.is_set()])
#             print("Detection result:", result)

#             if result.get("status") == "success" and result.get("detections"):
#                 detection_result = {
#                     "status": "Detected",
#                     "detections": result["detections"]
#                 }

#                 if user_email:
#                     # Send mail using sends_mail
#                     message = f"An object has been detected: {result['detections']}"
#                     sends_mail(user_email, message)
#                 else:
#                     print("No email provided. Cannot send email.")

#                 is_recording.clear()
#                 break
#             else:
#                 detection_result = {"status": "Pending", "detections": []}

#             time.sleep(0.1)
#     except Exception as e:
#         print(f"Error during detection: {e}")
#         detection_result = {"status": "Error", "detections": []}
#         is_recording.clear()
#     finally:
#         is_recording.clear()




























# Signout view
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# User login view
def user_login(request):
    if request.method == "POST" and "login" in request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            # Redirect superuser to dashboard
            if user.is_superuser:
                return redirect("dashboard")  # URL name for dashboard.html
            else:
                return redirect("home")  # Redirect to homepage for regular users
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "register.html", {"active_form": "login"})


# Register view
def user_register(request):
    if request.method == "POST" and "signup" in request.POST:
        fname = request.POST.get("fname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html", {"active_form": "signup"})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "register.html", {"active_form": "signup"})

        # Create the user
        user = User.objects.create_user(first_name=fname, phone=phone, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")  # Redirect to the login page

    return render(request, "register.html", {"active_form": "signup"})


# Dashboard view for admins
def dashboard(request):
    result = User.objects.filter(is_superuser=False)
    return render(request, 'dashboard.html', {'result': result})
