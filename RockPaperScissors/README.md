## Introduction
This project uses a pre-trained YOLO v8 nano model to recognise hand gestures. Three specific hand gestures are trained upon
to enable the users to play a game of rock-paper-scissors with the model classifying the hand gestures appropriately.
## Dependencies
* `ultralytics (YOLO)`
* `torch`
* `cv2`
* `roboflow (Roboflow)`
## Project Structure
* Acquired pre-trained model - `./yolov8.pt`
* Trained models - `./runs/detect/hand_gesture_model/weights/best.pt`
* Training and running - `./rock_paper_scissors_code.ipynb`
## Methodology 
This object detection model has been trained upon YOLOv8 nano architecture. 
* **Dataset** Pictures of hands in three postures, rock, paper, scissors, were extracted from Roboflow's publicly available datasets.(https://universe.roboflow.com/r-rishee-keshavan/rock-paper-scissors-bwev7-mfcrk)
* **Preprocessing & Augmentation** Images were annotated by three classes (rock, paper, scissors) and augmentations including random rotations and grayscaling were applied.
## Observation 
* The model works sufficiently fine when hands are visible sideways but not as good when hands are towards the front.
* Initially, the model usually recognised faces as rock, to correct this, the model was further trained on negative samples of people's faces.
