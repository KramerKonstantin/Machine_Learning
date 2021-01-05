import torch
import torch.nn as nn
import torchvision
from torch.utils.data.dataloader import DataLoader
from torchvision import transforms
from matplotlib import pyplot as plt


DATA_PATH = '...'
MODEL_PATH = '...'

num_epochs = 5
num_classes = 10
batch_size = 100

transform = transforms.ToTensor()

# MNIST
# train_dataset = torchvision.datasets.MNIST(root=DATA_PATH, train=True, transform=transform, download=True)
# test_dataset = torchvision.datasets.MNIST(root=DATA_PATH, train=False, transform=transform)

# MNIST fashion
train_dataset = torchvision.datasets.FashionMNIST(root=DATA_PATH, train=True, transform=transform, download=True)
test_dataset = torchvision.datasets.FashionMNIST(root=DATA_PATH, train=False, transform=transform)

train_data_loader = DataLoader(dataset=train_dataset, batch_size=batch_size)
test_data_loader = DataLoader(dataset=test_dataset, batch_size=batch_size)


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.dropout = nn.Dropout()
        self.fully_connected_layer1 = nn.Linear(in_features=7 * 7 * 64, out_features=1000)
        self.fully_connected_layer2 = nn.Linear(in_features=1000, out_features=10)

    def forward(self, data):
        out = self.layer1(data)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.dropout(out)
        out = self.fully_connected_layer1(out)
        out = self.fully_connected_layer2(out)
        return out


model = CNN()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

total_step = len(train_data_loader)
loss_list = []
acc_list = []
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_data_loader):
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss_list.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total = labels.size(0)
        _, predicted = torch.max(outputs.data, 1)
        correct = (predicted == labels).sum().item()
        acc_list.append(correct / total)

        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.6f}, Accuracy: {:.2f}%'
                  .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(), (correct / total) * 100))


softmax = nn.Softmax(dim=0)

labels = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
best_prob = [(0, None) for i in range(len(labels))]

model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, targets in test_data_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

        for output, target, prediction, image in zip(outputs, targets, predicted, images):
            probs = softmax(output)
            for i, prob in enumerate(probs):
                if prob > best_prob[i][0]:
                    best_prob[i] = (prob.item(), image)

    print('Test Accuracy: {} %'.format(correct / total * 100))

torch.save(model.state_dict(), MODEL_PATH + 'fashion.ckpt')

plt.figure(figsize=(10, 4))
for i in range(len(best_prob)):
    plt.subplot(2, 5, 1 + i)
    plt.title("{} : {:.6f}".format(labels[i], best_prob[i][0]))
    plt.imshow((best_prob[i][1]).permute(1, 2, 0))
plt.tight_layout()
plt.show()
