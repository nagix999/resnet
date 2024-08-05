from pathlib import Path

from torch.utils.data import Dataset
import torch
import numpy as np


class CifarDataset(Dataset):
    def __init__(self, cifar_path, transform=None, train=True):
        filename = "data_batch_*" if train else "test_batch"
        batch_files = list(Path(cifar_path).glob(filename))

        self.images = []
        self.labels = []
        self.transform = transform

        for file in batch_files:
            batch = self.unpickle(str(file))
            self.labels += batch[b'labels']
            data = batch[b'data']

            for image in data:
                image = [np.split(x, 32) for x in np.split(image, 3)]
                image = np.array(image)
                self.images.append(image)

        self.images = torch.from_numpy(np.array(self.images))

    def unpickle(self, file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]

        if self.transform is not None:
            image = self.transform(image)

        return idx, image, label