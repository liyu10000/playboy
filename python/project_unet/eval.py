import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Function
from tqdm import tqdm


class DiceCoeff(Function):
    """Dice coeff for individual examples"""

    def forward(self, input, target):
        self.save_for_backward(input, target)
        eps = 0.0001
        self.inter = torch.dot(input.view(-1), target.view(-1))
        self.union = torch.sum(input) + torch.sum(target) + eps

        t = (2 * self.inter.float() + eps) / self.union.float()
        return t

    # This function has only a single output, so it gets only one gradient
    def backward(self, grad_output):

        input, target = self.saved_variables
        grad_input = grad_target = None

        if self.needs_input_grad[0]:
            grad_input = grad_output * 2 * (target * self.union - self.inter) \
                         / (self.union * self.union)
        if self.needs_input_grad[1]:
            grad_target = None

        return grad_input, grad_target


def dice_coeff(input, target):
    """Dice coeff for batches"""
    if input.is_cuda:
        s = torch.FloatTensor(1).cuda().zero_()
    else:
        s = torch.FloatTensor(1).zero_()
        
    for i, (ip, tg) in enumerate(zip(input, target)):
        ip = (ip > 0.5).float()  # this operation will loss grad info
        s += DiceCoeff().forward(ip, tg)
        
    return s / (i + 1)


# def dice_loss(input, target):
#     """Dice coeff for batches"""
#     num = input.size(0)
#     inter = (input.view(num, -1) * target.view(num, -1)).sum()
#     union = input.sum() + target.sum()

#     t = (2 * inter.float() + 1) / (union.float() + 1)
#     return 1 - t / num


def dice_loss(input, target):
    """Dice coeff for batches"""
    if input.is_cuda:
        s = torch.FloatTensor(1).cuda().zero_()
    else:
        s = torch.FloatTensor(1).zero_()

    for i, (ip, tg) in enumerate(zip(input, target)):
        s += DiceCoeff().forward(ip, tg)

    return 1. - s / (i + 1)


def bce_dice_loss(input, target):
    return nn.BCEWithLogitsLoss()(input, target) + dice_loss(input, target)


def evaluate(model, loader, device, n_val):
    """Evaluation without the densecrf with the dice coefficient"""
    model.eval()
    tot = 0

    with tqdm(total=n_val, desc='Validation', unit='img', leave=False) as pbar:
        for i, batch in enumerate(loader):
            imgs = batch['image']
            masks_true = batch['mask']

            imgs = imgs.to(device=device, dtype=torch.float32)
            mask_type = torch.float32 if model.n_classes == 1 else torch.long
            masks_true = masks_true.to(device=device, dtype=mask_type)

            masks_pred = model(imgs)
            
            tot += dice_loss(masks_pred, masks_true).item()
#             tot += bce_dice_loss(masks_pred, masks_true).item()

#             for mask_true, mask_pred in zip(masks_true, masks_pred):
#                 mask_pred = (mask_pred > 0.5).float()
#                 if model.n_classes > 1:
#                     tot += F.cross_entropy(mask_pred.unsqueeze(dim=0), mask_true.unsqueeze(dim=0)).item()
#                 else:
#                     tot += dice_coeff(mask_pred, mask_true).item()
            pbar.update(imgs.shape[0])

    return tot / (i + 1)
