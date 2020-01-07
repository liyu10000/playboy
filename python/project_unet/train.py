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
from eval import bce_dice_loss, evaluate


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
        # scale down
        img = img / 255
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
        img = cv2.imread(img_file, 0)  # input image is in grayscale
        mask = cv2.imread(mask_file, 0)

        img = self.transform(img, True, 128, 128)
        mask = self.transform(mask, True, 128, 128)

        sample = {'image':img, 'mask':mask}
        return sample


def train(model, dir_img, dir_mask, dir_checkpoint, 
          device, epochs=5, batch_size=4, lr=0.1, val_percent=0.1, save_cp=False, resume_from=0):
    dataset = BasicDataset(dir_img, dir_mask)

    n_val = int(len(dataset) * val_percent)
    n_train = len(dataset) - n_val
    train, val = random_split(dataset, [n_train, n_val])
    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True, num_workers=8, pin_memory=True)
    val_loader = DataLoader(val, batch_size=batch_size, shuffle=False, num_workers=8, pin_memory=True)

    optimizer = optim.RMSprop(model.parameters(), lr=lr, weight_decay=1e-8)
#     if model.n_classes > 1:
#         ce_loss = nn.CrossEntropyLoss()
#     else:
#         ce_loss = nn.BCEWithLogitsLoss()

    # resume from a checkpoint
    epoch = 0
    if resume_from > 0:
        model_path = os.path.join(dir_checkpoint, f'epoch{resume_from}.pth')
        if os.path.isfile(model_path):
            model.load_state_dict(torch.load(model_path))
            epoch = resume_from

    model.to(device=device)

    while epoch < epochs:
        model.train()

        epoch_loss = 0
        with tqdm(total=n_train, desc=f'Epoch {epoch + 1}/{epochs}', unit='img') as pbar:
            for i,batch in enumerate(train_loader):
                imgs = batch['image']
                masks_true = batch['mask']

                imgs = imgs.to(device=device, dtype=torch.float32)
                mask_type = torch.float32 if model.n_classes == 1 else torch.long
                masks_true = masks_true.to(device=device, dtype=mask_type)

                masks_pred = model(imgs)
                loss = bce_dice_loss(masks_pred, masks_true)
                epoch_loss += loss.item()
                pbar.set_postfix(**{'loss': '{:.3f}'.format(epoch_loss/(i+1))})

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                pbar.update(imgs.shape[0])

        val_score = evaluate(model, val_loader, device, n_val)
        print('Epoch {} val score: {:.3f}'.format(epoch+1, val_score))

        if save_cp:
            os.makedirs(dir_checkpoint, exist_ok=True)
            model_path = os.path.join(dir_checkpoint, f'epoch{epoch+1}.pth')
            torch.save(model.state_dict(), model_path)

        epoch += 1



if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = UNet(n_filters=32, n_channels=1, n_classes=1)
    # faster convolutions, but more memory
    torch.backends.cudnn.benchmark = True

    train(model=model,
          dir_img='./tgs_salt_identification_challenge/train/images',
          dir_mask='./tgs_salt_identification_challenge/train/masks',
          dir_checkpoint='./tgs_salt_identification_challenge/checkpoints',
          device=device,
          epochs=50,
          batch_size=128,
          lr=0.05,
          val_percent=0.05,
          save_cp=False,
          resume_from=0
          )

