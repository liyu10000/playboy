import torch
from torch.autograd import Function
import torch.nn.functional as F
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

    for i, c in enumerate(zip(input, target)):
        s += DiceCoeff().forward(c[0], c[1])

    return s / (i + 1)



def evaluate(model, loader, device, n_val):
    """Evaluation without the densecrf with the dice coefficient"""
    model.eval()
    tot = 0

    with tqdm(total=n_val, desc='Validation', unit='img', leave=False) as pbar:
        for batch in loader:
            imgs = batch['image']
            masks_true = batch['mask']

            imgs = imgs.to(device=device, dtype=torch.float32)
            mask_type = torch.float32 if model.n_classes == 1 else torch.long
            masks_true = masks_true.to(device=device, dtype=mask_type)

            masks_pred = model(imgs)

            for mask_true, mask_pred in zip(masks_true, masks_pred):
                mask_true = (mask_true > 0.5).float()
                if model.n_classes > 1:
                    tot += F.cross_entropy(mask_pred.unsqueeze(dim=0), mask_true.unsqueeze(dim=0)).item()
                else:
                    tot += dice_coeff(mask_pred, mask_true.squeeze(dim=1)).item()
            pbar.update(imgs.shape[0])

    return tot / n_val