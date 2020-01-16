import os
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import logging
from tqdm import tqdm
from torch import optim
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms, utils
from data import BasicDataset
from unet import UNet
from eval import dice_loss, bce_dice_loss, evaluate



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
    if resume_from > 0:
        model_path = os.path.join(dir_checkpoint, f'epoch{resume_from}.pth')
        if os.path.isfile(model_path):
            model.load_state_dict(torch.load(model_path))
        else:
            resume_from = 0

    writer = SummaryWriter(comment=f'_LR_{lr}_BS_{batch_size}')
    logging.info(f'''Starting training:
        Device:          {device.type}
        Epochs:          {epochs}
        Batch size:      {batch_size}
        Learning rate:   {lr}
        Training size:   {n_train}
        Validation size: {n_val}
        Checkpoints:     {save_cp}
        Resume from:     {None if resume_from == 0 else resume_from}
    ''')
            
    global_step = 0

    model.to(device=device)

    for epoch in range(resume_from, epochs):
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
                loss = dice_loss(masks_pred, masks_true)
#                 loss = bce_dice_loss(masks_pred, masks_true)
                epoch_loss += loss.item()

                writer.add_scalar('Loss/train', loss.item(), global_step)
                pbar.set_postfix(**{'loss': '{:.3f}'.format(epoch_loss/(i+1))})

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                pbar.update(imgs.shape[0])
                global_step += 1

        val_score = evaluate(model, val_loader, device, n_val)
        print('Epoch {} val score: {:.3f}'.format(epoch+1, val_score))

        if save_cp:
            os.makedirs(dir_checkpoint, exist_ok=True)
            model_path = os.path.join(dir_checkpoint, f'epoch{epoch+1}.pth')
            torch.save(model.state_dict(), model_path)
        
    writer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    model = UNet(n_filters=32, n_channels=1, n_classes=1)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # faster convolutions, but more memory
    torch.backends.cudnn.benchmark = True

    train(model=model,
          dir_img='./tgs_salt_identification_challenge/train/images',
          dir_mask='./tgs_salt_identification_challenge/train/masks',
          dir_checkpoint='./tgs_salt_identification_challenge/checkpoints',
          device=device,
          epochs=5,
          batch_size=128,
          lr=0.05,
          val_percent=0.05,
          save_cp=False,
          resume_from=0
          )

