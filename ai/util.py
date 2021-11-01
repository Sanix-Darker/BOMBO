import torch
from torchvision import datasets, transforms
from PIL import Image
import numpy as np
import json

def load_dataset(data_dir):
    """ Loads the training and validation set with images

    Parameters
    ----------
    data_dir : str, input data directory

    Returns
    -------
    trainloader: Torch DataLoader, iterable over the training set
    validloader: Torch DataLoader, iterable over the validation set
    class_to_idx: dict, mappings of categories (key) to indices (value)
    """

    #Input data directories
    train_dir = data_dir + '/train'
    valid_dir = data_dir + '/valid'
    #test_dir = data_dir + '/test'

    #Training data augmentation with rotations, mirroring, random scaling, cropping and normalization
    train_transforms = transforms.Compose([transforms.RandomRotation(30),
                                           transforms.RandomHorizontalFlip(),
                                           transforms.RandomVerticalFlip(),
                                           transforms.RandomResizedCrop(224, scale = (0.3, 1)),
                                           transforms.Resize(256),
                                           transforms.CenterCrop(224),
                                           transforms.ToTensor(),
                                           transforms.Normalize([0.485, 0.456, 0.406],
                                                                [0.229, 0.224, 0.225])])

    #Validation/test data augmentation with cropping and normalization
    validation_test_transforms = transforms.Compose([transforms.Resize(256),
                                                transforms.CenterCrop(224),
                                                transforms.ToTensor(),
                                                transforms.Normalize([0.485, 0.456, 0.406],
                                                                     [0.229, 0.224, 0.225])])

    #Data loading
    train_data = datasets.ImageFolder(train_dir, transform = train_transforms)
    valid_data = datasets.ImageFolder(valid_dir, transform = validation_test_transforms)
    #test_data = datasets.ImageFolder(test_dir, transform=validation_test_transforms)

    #Data batching
    trainloader = torch.utils.data.DataLoader(train_data, batch_size = 64, shuffle = True)
    validloader = torch.utils.data.DataLoader(valid_data, batch_size = 64)
    #testloader = torch.utils.data.DataLoader(test_data, batch_size=64)

    #Extract (from the input dataset) the mapping of classes to indices
    class_to_idx = train_data.class_to_idx

    return trainloader, validloader, class_to_idx


def process_image(image):
    """ Scales, crops, and normalizes an input PIL image and converts it into
    an Numpy array that can be fed into the trained PyTorch model

    Parameters
    ----------
    image : PIL image

    Returns
    -------
    image_np : Numpy array, image in the converted format that can be fed into
    the trained PyTorch model
    """

    # Scaling and cropping to 224x224 - different treatment for portrait/landscape
    if image.width <= image.height:
        # Both sides have to be at least 256 pixles - set width to 256, keep the ratio
        image_resize = image.resize((256, round(256 * (image.height / image.width))))

        # Extract the center 224x224
        upper = round((image_resize.height - 224) / 2) - 1
        lower = upper + 224

        left = 15
        right = 239

        image_cropped = image_resize.crop((left, upper, right, lower))

    else:
        # Both sides have to be at least 256 pixles - set height to 256, keep the ratio
        image_resize = image.resize((round(256* (image.width / image.height)), 256))

        # Extract the center 224x224
        lower = 239
        upper = 15
        left = round((image_resize.width - 224) / 2) - 1
        right = left + 224

        image_cropped = image_resize.crop((left, upper, right, lower))

    # Canvert the RGB values from 0-255 into 0-1
    np_image = np.array(image_cropped)/255

    # Normalize the array
    np_image_std = (np_image - np.array([0.485, 0.456, 0.406]).\
    reshape(1, 1, 3)) / np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3)

    # Transpose numpy image height x width x channels to torch image
    # channels x height x width
    image_np = np.transpose(np_image_std, (2, 0, 1))

    return image_np
