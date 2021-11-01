import torch
from torch import nn
from torchvision import models

def construct_model(arch, hidden_units):
    """ Builds a convolutional neural network through transfer learning.

    The function first imports one of the already trained torchvision CNNs (vgg11,
    vgg13, vgg16, vgg19, densenet121, densenet169, densenet201, densenet161,
    alexnet). It then fixes all the weights for all of the network except for the final
    fully connected layer, which is replaced with a new one with random weights.
    Only the fully connected layer will be trained to a specific problem (CNN is
    essentially used as a fixed feature extractor).

    Parameters
    ----------
    arch : str, name of the imported torchvision model
    hidden_units : list, number of hidden units in each layer of the new classifier

    Returns
    -------
    model : torchvision model
    """

    # Load a pretrained network
    model = getattr(models, arch)(pretrained = True)

    # Freeze all its parameters so that the gradients are not computed during training
    for params in model.parameters():
        params.requires_grad = False

    # Obtain the size of the layer that represents the input layer of the fully
    # connected classifier
    if arch in ['vgg11', 'vgg13', 'vgg16', 'vgg19']:
        input_size = model.classifier[0].in_features
    elif arch in ['densenet121', 'densenet169', 'densenet201', 'densenet161']:
        input_size = model.classifier.in_features
    elif arch in ['alexnet']:
        input_size = model.classifier[1].in_features
    else:
        print('The selected pre-trained network is not supported')

    # Define a new fully connected feedforward network for use as a classifier
    # Use rectified linear activation functions and dropout
    if len(hidden_units)==1:
        alt_classifier = nn.Sequential(
            nn.Linear(input_size, hidden_units[0]),
            nn.ReLU(),
            nn.Dropout(p = 0.3),
            nn.Linear(hidden_units[0], 102),
            nn.LogSoftmax(dim = 1)
        )
    # Instance with 2 hidden layers
    else:
        alt_classifier = nn.Sequential(
            nn.Linear(input_size, hidden_units[0]),
            nn.ReLU(),
            nn.Dropout(p = 0.3),
            nn.Linear(hidden_units[0],hidden_units[1]),
            nn.Dropout(p = 0.3),
            nn.ReLU(),
            nn.Linear(hidden_units[1], 102),
            nn.LogSoftmax(dim = 1)
        )

    # Overwrite the model's classifier
    # Parameters of the newly constructed module have requires_grad=True by default
    model.classifier = alt_classifier

    return model
