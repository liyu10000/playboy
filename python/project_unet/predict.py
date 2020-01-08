import os
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torchvision import transforms
from random import randint
from data import BasicDataset
from unet import UNet


def load_model(dir_checkpoint, checkpoint):
    model = UNet(n_filters=32, n_channels=1, n_classes=1)
    model_path = os.path.join(dir_checkpoint, f'epoch{checkpoint}.pth')
    if os.path.isfile(model_path):
        model.load_state_dict(torch.load(model_path))
    return model


def predict(model,
            img,
            device):
    model.to(device=device)
    model.eval()

    img = torch.from_numpy(np.array([BasicDataset.transform(img, True, 128, 128)]))

    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = model(img)

        if model.n_classes > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze()

        mask_pred = probs.cpu().numpy()
        # mask_pred_b = mask_pred > 0.5  # binary mask

    return mask_pred


if __name__ == '__main__':
    dir_img='./tgs_salt_identification_challenge/train/images'
    dir_mask='./tgs_salt_identification_challenge/train/masks'
    dir_checkpoint='./tgs_salt_identification_challenge/checkpoints'

    checkpoint = 10
    model = load_model(dir_checkpoint, checkpoint)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    ids = [os.path.splitext(f)[0] for f in os.listdir(dir_img)]
    i = randint(0, len(ids))
    idx = ids[i]
    img_file = os.path.join(dir_img, idx+'.png')
    mask_file = os.path.join(dir_mask, idx+'.png')
    img = cv2.imread(img_file, 0)  # input image is in grayscale
    mask = cv2.imread(mask_file, 0)

    predict(model, img, device)