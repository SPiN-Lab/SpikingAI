from torch import nn
from SpykeTorch import snn
from spykeTorch import functional as sf

class neural_layer(nn.Module):
  """
  This class implements a simple model consisting on a pooling layer,
  a trainable convolution layer, sf.fire that gives the spiking neurons vector
  and sf.get_k_winners to determine the winner neurons. Finally, the weights
  of the convolutional are update using the stdp algorithm.
  """

  def __init__(self, in_dim=4, out_channels=20,kernel_1=3, kernel_2=30, LR = (0.05, -0.015)):
    """
    Initialize the layers of the network and the stdp class

    Args:
      in_dim: Integer
        dimensionality of input data (4)
      out_channels: Integer
        number of output features (20)
      kernel_1: List
        Kernel for the first pooling layer (3)
      kernel_2: List
        Kernel for the second convolutional layer (20)
      LR: tuple
        Learning rate for the STDP (0.05, -0.015)

    Returns:
      Nothing
    """

    super(neural_layer, self).__init__()

    self.in_dim = in_dim
    self.out_channels = out_channels
    self.pool = snn.Pooling(kernel_size = kernel_1, stride = 2)
    self.conv = snn.Convolution(in_channels=self.in_dim, out_channels=self.out_channels, kernel_size=kernel_2)
    self.stdp = snn.STDP(conv_layer=self.conv,learning_rate = LR)
  def forward(self, x):
    """
    Defines the network structure and flow from input to output

    Args:
      x: Tensor
        Image to be processed by the network

    Returns:
      output: List
        List containing the potencials and the spikes tensors and the winners list

    """
    # Flatten each images into a 'vector'
    x=self.pool(x)
    potencials=self.conv(x)
    spikes, potencials = sf.fire(potencials, 20, return_thresholded_potentials=True)
    winners = sf.get_k_winners(potencials, kwta=1, inhibition_radius=0, spikes=spikes)
    output = [potencials,spikes,winners]
    self.stdp(x, potencials, spikes, winners)
    return output