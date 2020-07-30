import camera
from facenet_pytorch.models.mtcnn import MTCNN
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import torch.nn.functional as F

class EmotionCNN(torch.nn.Module):
    def __init__(self):
        super(EmotionCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, 3)
        self.conv2 = nn.Conv2d(64, 64, 3)

        self.maxpool = nn.MaxPool2d(2,2)

        self.conv3 = nn.Conv2d(64, 128, 3)
        self.conv4 = nn.Conv2d(128, 128, 3)
        self.conv5 = nn.Conv2d(128, 256, 3)
        self.conv6 = nn.Conv2d(256, 256, 3)

        self.fc1 = nn.Linear(12544, 1024)
        self.fc2 = nn.Linear(1024, 2)

        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.dropout(x)
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = F.relu(self.conv6(x))
        x = self.maxpool(x)
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)

        return F.softmax(self.fc2(x))


def take_image_classify_emotion():
    """
    Takes an image and classifies the face's emotion
    Returns
    -------
    0 if the model determines the image is negative and 1 if the model determines the image is positive
    """
    pic = camera.take_picture()
    mtcnn = MTCNN()
    faces = mtcnn.forward(pic.copy())

    model = EmotionCNN()
    model.load_state_dict(torch.load("emotion_model_new.pt"))
    model.eval()

    pre_process = transforms.Compose(
        [transforms.Resize(48), transforms.Grayscale(num_output_channels=1), transforms.ToTensor(),
         transforms.Normalize(mean=[0.5], std=[0.5])])

    classes = ["negative", "positive"]
    fig = plt.figure(figsize=(25, 4))
    ax = fig.add_subplot()

    image = np.transpose(faces.numpy(), (1, 2, 0))
    image = Image.fromarray((image * 255).astype(np.uint8))
    image = pre_process(image)

    plt.imshow(np.transpose(faces.numpy(), (1, 2, 0)))
    output = model(image.reshape(1, 1, 48, 48))
    prediction = torch.argmax(output, dim=1).item()

    ax.set_title(f"Predicted:{classes[prediction]}")

    return pic, prediction

def load_image_classify_emotion(path):
    """
    Loads an image from a path and classifies the face's emotion
    Parameters
    -------
    path the path of the image
    Returns
    -------
    0 if the model determines the image is negative and 1 if the model determines the image is positive
    """
    pic = plt.imread(path)
    mtcnn = MTCNN()
    faces = mtcnn.forward(pic.copy())

    model = EmotionCNN()
    model.load_state_dict(torch.load("emotion_model_new.pt"))
    model.eval()

    pre_process = transforms.Compose(
        [transforms.Resize(48), transforms.Grayscale(num_output_channels=1), transforms.ToTensor(),
         transforms.Normalize(mean=[0.5], std=[0.5])])

    classes = ["negative", "positive"]
    fig = plt.figure(figsize=(25, 4))
    ax = fig.add_subplot()

    image = np.transpose(faces.numpy(), (1, 2, 0))
    image = Image.fromarray((image * 255).astype(np.uint8))
    image = pre_process(image)

    plt.imshow(np.transpose(faces.numpy(), (1, 2, 0)))
    output = model(image.reshape(1, 1, 48, 48))
    prediction = torch.argmax(output, dim=1).item()

    ax.set_title(f"Predicted:{classes[prediction]}")

    return pic, prediction