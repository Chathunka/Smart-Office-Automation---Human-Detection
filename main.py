import cv2
import torch
import imutils
import paho.mqtt.client as mqtt

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)

# Open video capture device
uri = 'rtsp://your ip cameara uri'
cap = cv2.VideoCapture(uri, cv2.CAP_FFMPEG)

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

# Create MQTT client instance
client = mqtt.Client("USERNAME")
client.username_pw_set("USERNAME", "PASSWORD")
client.on_connect = on_connect
client.on_publish = on_publish
print("Connecting to broker")
client.connect("ip")
client.loop_start()

# Initialize previous person count to 0
prev_person_count = 0

# Main loop
while True:
    try:
        # Read frame from video capture device
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from camera.")
            cap.release()
            cap = cv2.VideoCapture(uri, cv2.CAP_FFMPEG)
            continue

        # Resize frame for faster processing
        frame = imutils.resize(frame, width=640)

        # Detect objects in the frame using YOLOv5 model
        results = model(frame)
        list = []
        for index, row in results.pandas().xyxy[0].iterrows():
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            b = str(row['name'])
            if 'person' in b:
                list.append([x1, y1, x2, y2])

        # If person is detected in the frame
        if len(list) >= 0:
            person_count = len(list)
            print(f"Person detected in Location. Count: {person_count}")

            # Check if person count has changed
            if person_count != prev_person_count:
                try:
                    # Publish new person count to MQTT broker
                    client.publish("topic", person_count)
                except Exception as e:
                    print("MQTT publish error:", e)
                prev_person_count = person_count

            # Draw bounding boxes around detected persons
            for box in list:
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            print("No person detected in : Location")

        # Display the frame
        #cv2.imshow('FRAME',frame)

        # Exit if 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    except cv2.error as e:
        print(f"OpenCV Error: {e}")
        cap.release()
        cap = cv2.VideoCapture(uri, cv2.CAP_FFMPEG)
        continue

# Stop MQTT client and release video capture device
client.loop_stop()
client.disconnect()
cap.release()
#cv2.destroyAllWindows()
