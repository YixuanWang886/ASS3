import cv2
from torchvision import transforms
from ultralytics import YOLO

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # Load the YOLOv8 model
        self.model = YOLO("models/best-2.pt")
        self.model.conf = 0.5  # Set the confidence threshold

        # Set input image size
        self.input_size = 800

    def __del__(self):
        self.video.release()

    def get_frame_with_detection(self):
    # Read frame from video
        success, frame = self.video.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = self.model(frame)
            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Convert the annotated frame to OpenCV format
            #annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

            # Convert the annotated frame to bytes
            ret, output_image = cv2.imencode('.jpg', annotated_frame)
            output_bytes = output_image.tobytes()

            return output_bytes, annotated_frame

        else:
            return None, None


    def get_frame_without_detection(self):
        success, image = self.video.read()
        outputs = image.copy()

        ret, output_image = cv2.imencode('.jpg', outputs)
        return output_image.tobytes(), outputs

def generate_frames(camera, AI):
    try:
        while True:
            if AI:
                frame, _ = camera.get_frame_with_detection()  # 获取带有检测的帧
            else:
                frame, _ = camera.get_frame_without_detection()  # 获取不带检测的帧
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except Exception as e:
         print(e)
    finally:
        print("Reached finally, detection stopped")
        cv2.destroyAllWindows()
