import pytest

import SpykeTorch.utils as utils
import SpykeTorch.utils as utils
import SpykeTorch.functional as sf
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torch.utils.data import SubsetRandomSampler
from torch import manual_seed
from SpikingAI import models


def test_neural_layer():
    seed = 123
    manual_seed(seed) 
    def time_dim(input):
        return input.unsqueeze(0)
    
    kernels = [	utils.GaborKernel(window_size = 3, orientation = 45+22.5),
                utils.GaborKernel(3, 90+22.5),
                utils.GaborKernel(3, 135+22.5),
                utils.GaborKernel(3, 180+22.5)]
    filter = utils.Filter(kernels, use_abs = True)

    transform = transforms.Compose(
        [transforms.Grayscale(),
        transforms.ToTensor(),
        time_dim,
        filter,
        sf.pointwise_inhibition,
        utils.Intensity2Latency(number_of_spike_bins = 15, to_spike = True)])
    dataset = ImageFolder("dataset/eth", transform)
    dataset = utils.CacheDataset(dataset)
    train_loader = DataLoader(dataset, sampler=SubsetRandomSampler([0]))
    neu_lat = models.neural_layer(in_dim=4, out_channels=20,kernel_1=3,
                                  kernel_2=30, LR = (0.05, -0.015))
    for data,_ in train_loader:
        for x in data:
            output = neu_lat.forward(x)


    assert len(output) == 3
    assert output[2][0] == (17,0,0)
    assert output[0].shape[0] == 15
    assert output[0].shape[1] == 20
    # assert  output[0].shape == ()