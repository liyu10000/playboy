import torch
import torch.nn as nn
import torch.nn.functional as F


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)


class UNet(nn.Module):
    def __init__(self, n_filters=16, n_channels=1, n_classes=1):
        super().__init__()
        self.n_filters = n_filters
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.dc1 = DoubleConv(n_channels, n_filters)
        self.mp1 = nn.MaxPool2d(2, stride=2)
        self.dc2 = DoubleConv(n_filters, n_filters*2)
        self.mp2 = nn.MaxPool2d(2, stride=2)
        self.dc3 = DoubleConv(n_filters*2, n_filters*4)
        self.mp3 = nn.MaxPool2d(2, stride=2)
        self.dc4 = DoubleConv(n_filters*4, n_filters*8)
        self.mp4 = nn.MaxPool2d(2, stride=2)
        self.dc5 = DoubleConv(n_filters*8, n_filters*16)
        self.up1 = nn.ConvTranspose2d(n_filters*16, n_filters*8, kernel_size=2, stride=2)
        self.dc6 = DoubleConv(n_filters*16, n_filters*8)
        self.up2 = nn.ConvTranspose2d(n_filters*8, n_filters*4, kernel_size=2, stride=2)
        self.dc7 = DoubleConv(n_filters*8, n_filters*4)
        self.up3 = nn.ConvTranspose2d(n_filters*4, n_filters*2, kernel_size=2, stride=2)
        self.dc8 = DoubleConv(n_filters*4, n_filters*2)
        self.up4 = nn.ConvTranspose2d(n_filters*2, n_filters, kernel_size=2, stride=2)
        self.dc9 = DoubleConv(n_filters*2, n_filters)
        self.out = nn.Conv2d(n_filters, n_classes, kernel_size=1)

    def forward(self, x):
        # contraction path
        c1 = self.dc1(x)
        p1 = self.mp1(c1)
        c2 = self.dc2(p1)
        p2 = self.mp2(c2)
        c3 = self.dc3(p2)
        p3 = self.mp3(c3)
        c4 = self.dc4(p3)
        p4 = self.mp4(c4)
        c5 = self.dc5(p4)

        # expansion path
        u6 = self.up1(c5)
        u6 = torch.cat([c4, u6], dim=1)
        c6 = self.dc6(u6)
        u7 = self.up2(c6)
        u7 = torch.cat([c3, u7], dim=1)
        c7 = self.dc7(u7)
        u8 = self.up3(c7)
        u8 = torch.cat([c2, u8], dim=1)
        c8 = self.dc8(u8)
        u9 = self.up4(c8)
        u9 = torch.cat([c1, u9], dim=1)
        c9 = self.dc9(u9)
        out = self.out(c9)

        return out


if __name__ == '__main__':
    i = torch.randn(1, 3, 128, 128)
    unet = UNet(n_channels=3, n_classes=1)
    o = unet(i)
    print(o.size())