# Smart-Office-Automation---Person-Detection
Person Detection and Counting with YOLOv5 and MQTT

  This is a Python script for detecting people in a video stream using the YOLOv5 object detection model and publishing the count of detected people to an MQTT broker. The script is written in Python 3 and requires some external libraries such as OpenCV, Torch, and Paho MQTT client.



Requirements:

  Python 3
  OpenCV (cv2)
  PyTorch
  imutils
  Paho MQTT client



Usage:

  To use this script, you need to provide the RTSP camera URL in the uri variable in the script.
  uri = 'rtsp://your_ip_camera_uri'
  You also need to provide your MQTT broker IP address, username, and password in the following lines of code:



To run the script in docker, simply execute the following command:

Build: 
docker build -t ipcam .

Run:
docker run --rm -it ipcam


Output:

The script displays the count of detected persons in the video stream and draws bounding boxes around the detected persons. It also publishes the count of detected persons to the specified MQTT topic.


Notes:

If the script encounters an error while reading frames from the video stream, it will release and reinitialize the video capture device to continue processing frames.

The script exits the while loop and stops the MQTT client and releases the video capture device when the 'Esc' key is pressed.

The script can be modified to use different YOLOv5 models (such as yolov5m, yolov5l, and yolov5x) depending on the performance and accuracy requirements.

The script can be modified to perform other tasks based on the detected objects (such as tracking and counting objects other than persons).

This script can be used for various applications such as monitoring crowded places, traffic analysis, and security systems.



