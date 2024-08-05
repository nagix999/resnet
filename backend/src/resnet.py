import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_dim, dim, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(in_dim, dim, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(dim)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(dim, dim, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(dim)
        self.downsample = downsample

    def forward(self, x):
        input = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            input = self.downsample(input)

        out = out + input
        out = self.relu(out)
        return out


class BottleneckBlock(nn.Module):
    expansion = 4

    def __init__(self, in_dim, dim, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(in_dim, dim, kernel_size=1, stride=stride, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(dim)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(dim, dim, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(dim)
        self.conv3 = nn.Conv2d(dim, dim * self.expansion, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = nn.BatchNorm2d(dim * self.expansion)
        self.downsample = downsample

    def forward(self, x):
        input = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            input = self.downsample(input)

        out = out + input
        out = self.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes):
        super().__init__()
        self.in_dim = 64
        self.downsample = None
        self.stem = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64)
        )
        self.max_pool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.stage1 = self._build_stage(block, 64, layers[0], stride=1)
        self.stage2 = self._build_stage(block, 128, layers[1], stride=2)
        self.stage3 = self._build_stage(block, 256, layers[2], stride=2)
        self.stage4 = self._build_stage(block, 512, layers[3], stride=2)

        self.average_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _build_stage(self, block, dim, layers, stride):
        stage = []

        if stride != 1 or self.in_dim != dim * block.expansion:
            self.downsample = nn.Sequential(
                nn.Conv2d(self.in_dim, dim * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(dim * block.expansion)
            )

        stage.append(block(self.in_dim, dim, stride, self.downsample))
        self.in_dim = dim * block.expansion

        for _ in range(layers - 1):
            stage.append(block(self.in_dim, dim, stride=1))

        return nn.Sequential(*stage)

    def forward(self, x):
        out = self.stem(x)
        out = self.max_pool(out)
        out = self.stage1(out)
        out = self.stage2(out)
        out = self.stage3(out)
        out = self.stage4(out)
        out = self.average_pool(out)
        out = torch.flatten(out, 1)
        out = self.fc(out)
        return out


def resnet18(num_classes):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes)

def resnet34(num_classes):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes)

def resnet50(num_classes):
    return ResNet(BottleneckBlock, [3, 4, 6, 3], num_classes)

def resnet101(num_classes):
    return ResNet(BottleneckBlock, [3, 4, 23, 3], num_classes)

def resnet152(num_classes):
    return ResNet(BottleneckBlock, [3, 8, 36, 3], num_classes)