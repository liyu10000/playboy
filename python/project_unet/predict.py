import os
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
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
            device,
            threshold=0.5):
    model.to(device=device)
    model.eval()

    img = torch.from_numpy(BasicDataset.transform(img, True, 128, 128))

    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = model(img)

        if model.n_classes > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze(0)

        tf = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(img.size[1]),
                transforms.ToTensor()
            ]
        )

        probs = tf(probs.cpu())
        full_mask = probs.squeeze().cpu().numpy()

    return full_mask > threshold


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