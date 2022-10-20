# 优化器
import torch
import torchvision
from torch import nn
from torch.nn import Sequential, Conv2d, MaxPool2d, Flatten, Linear
from torch.utils.data import DataLoader

dataset = torchvision.datasets.CIFAR10("./set", train=False, transform=torchvision.transforms.ToTensor(),
                                       download=True)
dataloader = DataLoader(dataset, batch_size=1)


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        # 或者用sequential打包
        self.model1 = Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 4, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )

    def forward(self, x):
        x = self.model1(x)
        return x


loss = nn.CrossEntropyLoss()
model = Model()
# 选择随机梯度下降优化器
optim = torch.optim.SGD(model.parameters(), lr=0.01)
for data in dataloader:
    imgs, targets = data
    outputs = model(imgs)
    result_loss = loss(outputs, targets)
    # 通过反向传播，算出grad（小土堆pytorch p23），选择合适的优化器
    # 将之前算出来的梯度清零
    optim.zero_grad()
    result_loss.backward()
    # 优化器优化
    optim.step()
    print(result_loss)

