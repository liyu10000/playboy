import os
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
from torch import optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, utils
from unet import UNet


class BasicDataset(Dataset):
    def __init__(self, dir_img, dir_mask):
        self.dir_img = dir_img
        self.dir_mask = dir_mask
        self.ids = [os.path.splitext(f)[0] for f in os.listdir(dir_img)]

    def __len__(self):
        return len(self.ids)

    def transform(self, img, resize=True, W=None, H=None):
        # resize
        if resize:
            img = cv2.resize(img, (W, H))
        # expand dimension
        if len(img.shape) == 2:
            img = np.expand_dims(img, axis=2)
        # HWC to CHW
        img = img.transpose((2, 0, 1))
        return img


    def __getitem__(self, i):
        idx = self.ids[i]
        img_file = os.path.join(self.dir_img, idx+'.png')
        mask_file = os.path.join(self.dir_mask, idx+'.png')
        img = cv2.imread(img_file, 1)
        mask = cv2.imread(mask_file, 0)

        img = self.transform(img, True, 128, 128)
        mask = self.transform(mask, True, 128, 128)

        sample = {'image':img, 'mask':mask}
        return sample


def evaluate(net, loader, device, n_val):
    net.eval()
    if net.n_classes > 1:
        criterion = nn.CrossEntropyLoss()
    else:
        criterion = nn.BCEWithLogitsLoss()

    val_loss = 0
    with tqdm(total=n_val, desc='Validation', unit='img', leave=False) as pbar:
        for batch in loader:
            imgs = batch['image']
            masks = batch['mask']

            imgs = imgs.to(device=device, dtype=torch.float32)
            mask_type = torch.float32 if net.n_classes == 1 else torch.long
            masks = masks.to(device=device, dtype=mask_type)

            masks_pred = net(imgs)
            loss = criterion(masks_pred, masks)
            val_loss += loss.item()
            pbar.set_postfix(**{'loss (batch)': loss.item()})
            pbar.update(imgs.shape[0])

    return val_loss


def train(net, dir_img, dir_mask, dir_checkpoint, 
          device, epochs=5, batch_size=4, lr=0.1, val_percent=0.1, save_cp=False):
    dataset = BasicDataset(dir_img, dir_mask)

    n_val = int(len(dataset) * val_percent)
    n_train = len(dataset) - n_val
    train, val = random_split(dataset, [n_train, n_val])
    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True, num_workers=8, pin_memory=True)
    val_loader = DataLoader(val, batch_size=batch_size, shuffle=False, num_workers=8, pin_memory=True)

    optimizer = optim.RMSprop(net.parameters(), lr=lr, weight_decay=1e-6)
    if net.n_classes > 1:
        criterion = nn.CrossEntropyLoss()
    else:
        criterion = nn.BCEWithLogitsLoss()

    net.to(device=device)

    for epoch in range(epochs):
        net.train()

        epoch_loss = 0
        with tqdm(total=n_train, desc=f'Epoch {epoch + 1}/{epochs}', unit='img') as pbar:
            for batch in train_loader:
                imgs = batch['image']
                masks = batch['mask']

                imgs = imgs.to(device=device, dtype=torch.float32)
                mask_type = torch.float32 if net.n_classes == 1 else torch.long
                masks = masks.to(device=device, dtype=mask_type)

                masks_pred = net(imgs)
                loss = criterion(masks_pred, masks)
                epoch_loss += loss.item()
                pbar.set_postfix(**{'loss (batch)': loss.item()})

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                pbar.update(imgs.shape[0])

        val_loss = evaluate(net, val_loader, device, n_val)
        print(f'val score: {val_loss}')

        if save_cp:
            os.makedirs(dir_checkpoint, exist_ok=True)
            torch.save(net.state_dict(), os.path.join(dir_checkpoint, f'epoch{epoch+1}.pth'))



if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = UNet(n_channels=3, n_classes=1)
    # faster convolutions, but more memory
    # cudnn.benchmark = True

    train(net=net,
          dir_img='./tgs_salt_identification_challenge/train/images',
          dir_mask='./tgs_salt_identification_challenge/train/masks',
          dir_checkpoint='./tgs_salt_identification_challenge/checkpoints',
          device=device,
          epochs=2,
          batch_size=128,
          lr=0.05,
          val_percent=0.05,
          save_cp=True
          )

