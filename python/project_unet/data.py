import os
import cv2
import numpy as np
import logging
from torch.utils.data import Dataset



class BasicDataset(Dataset):
    def __init__(self, dir_img, dir_mask):
        self.dir_img = dir_img
        self.dir_mask = dir_mask
        self.ids = [os.path.splitext(f)[0] for f in os.listdir(dir_img)]
        logging.info(f'Creating dataset with {len(self.ids)} images')

    def __len__(self):
        return len(self.ids)

    @classmethod
    def transform(cls, img, resize=True, W=None, H=None):
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