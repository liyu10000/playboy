import torch
import torch.nn as nn
# import torch.nn.functional as F
from torch.autograd import Variable
from torchvision import models


def conv7x7(in_channels, out_channels):
    return nn.Conv2d(in_channels, out_channels, kernel_size=7, stride=2, padding=3, bias=False)

def conv3x3(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)

def conv1x1(in_channels, out_channels):
    return nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=2, bias=False)


class Downsample(nn.Module):
    def __init__(self, C):
        super(Downsample, self).__init__()
        self.conv = conv1x1(C, 2*C)
        self.bn = nn.BatchNorm2d(2*C)
        
    def forward(self, x):
        out = self.conv(x)
        out = self.bn(out)
        return out

    
class BasicBlock(nn.Module):
    ''' two layer residue block '''
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(BasicBlock, self).__init__()
        self.downsample = downsample
        
        self.conv1 = conv3x3(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu2 = nn.ReLU(inplace=True)
        
    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu1(out)
        
        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)
        else:
            identity = x
        
        out = out + identity
        out = self.relu2(out)
        
        return out


class ResNet18(nn.Module):
    ''' input shape: N x 3 x 224 x 224 '''
    def __init__(self, out_classes=1000):
        super(ResNet18, self).__init__()
        
        self.conv1 = conv7x7(3, 64)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU(inplace=True)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = nn.Sequential(BasicBlock(64, 64), 
                                    BasicBlock(64, 64))
        self.layer2 = nn.Sequential(BasicBlock(64, 128, 2, Downsample(64)), 
                                    BasicBlock(128, 128))
        self.layer3 = nn.Sequential(BasicBlock(128, 256, 2, Downsample(128)), 
                                    BasicBlock(256, 256))
        self.layer4 = nn.Sequential(BasicBlock(256, 512, 2, Downsample(256)), 
                                    BasicBlock(512, 512))
        self.avgpool1 = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, out_classes, bias=True)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        x = self.avgpool1(x) # global average pooling
        x = x.reshape(x.size(0), -1)
        x = self.fc(x)
        
        return x
    

class ResNet18Tiny(nn.Module):
    ''' input shape: N x 3 x 32 x 32 '''
    def __init__(self, out_classes=10):
        super(ResNet18Tiny, self).__init__()
        
        self.conv1 = conv3x3(3, 16)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu1 = nn.ReLU(inplace=True)
        self.layer1 = nn.Sequential(BasicBlock(16, 16), 
                                    BasicBlock(16, 16))
        self.layer2 = nn.Sequential(BasicBlock(16, 32, 2, Downsample(16)), 
                                    BasicBlock(32, 32))
        self.layer3 = nn.Sequential(BasicBlock(32, 64, 2, Downsample(32)), 
                                    BasicBlock(64, 64))
        self.avgpool1 = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(64, out_classes, bias=True)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        
        x = self.avgpool1(x) # global average pooling
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        
        return x



if __name__ == '__main__':
    # compare custom resnet18 with builtin resnet18
    x = torch.randn(64, 3, 224, 224)

    model1 = models.resnet18()
    out1 = model1(x)
    print(out1.shape)

    model2 = ResNet18()
    out2 = model2(x)
    print(out2.shape)

    diff = (out1 - out2).pow(2).sum()
    print(diff)
    
    # compare custom tiny resnet18
    x = torch.randn(64, 3, 32, 32)
    model = ResNet18Tiny()
    out = model(x)
    print(out.shape)