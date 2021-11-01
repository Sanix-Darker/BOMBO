import argparse
import util
import classifier_util
import torch
from torch import nn
from torch import optim

""" This Python script is part of the developed command line application. It is
used to train a new convolutional neural network on a specified dataset and save
the model as a checkpoint. The script has the following input arguments:
- data_dir : input data directory (required argument)
- save_dir : directory to save checkpoints
- arch : convolutional neural network architecture
- hidden_units : number of hidden units in each layer of the net's fully
connected classifier
- learning_rate : learning rate used in the Adam optimizer
- epochs : number of training epochs
- gpu : flag to run on GPU
"""

parser = argparse.ArgumentParser()
parser.add_argument('data_dir', action = 'store')
parser.add_argument('--save_dir', action = 'store', dest = 'save_dir', default = 'checkpoint.pth')
parser.add_argument('--arch', action = 'store', dest = 'arch', default = 'vgg11')
parser.add_argument('--hidden_units', action = 'append', dest = 'hidden_units', type = int)
parser.add_argument('--learning_rate', action = 'store', dest = 'learning_rate', default = 0.001, type = float)
parser.add_argument('--epochs', action = 'store', dest='epochs', type = int, default = 7)
parser.add_argument('--gpu', action="store_true", default=True)
args = parser.parse_args()

#Load data
trainloader, validloader, class_to_idx = util.load_dataset(args.data_dir)

#action='append' :  argparse does not override the default list but appends to the default
#Hence no default specified for the hidden_units above -> workaround:
if args.hidden_units == None:
    hidden_units = [2048]
else:
    hidden_units = args.hidden_units

#Define the model
model = classifier_util.construct_model(args.arch, hidden_units)
#Mappings from categories to indices
model.class_to_idx = class_to_idx

#Select the device used for training (either CPU or GPU/cuda)
device = 'cuda' if args.gpu else 'cpu'
model.to(device)

#Define the loss function
criterion = nn.NLLLoss()

#Define the optimizer
optimizer = optim.Adam(model.classifier.parameters(), lr = args.learning_rate)

#Model training
epochs = args.epochs
n_batches = len(trainloader)
for i in range(epochs):
    print(f'Epoch {i+1} training...')
    train_loss = 0
    progress = 0.25
    n = 0
    for images, labels in trainloader:
        #Load the labelled training batch to the respective device
        images, labels = images.to(device), labels.to(device)

        #Set the parameter gradient to zero
        optimizer.zero_grad()

        #Forward & backward pass, update weights
        logprob = model.forward(images)
        train_loss_batch = criterion(logprob, labels)
        train_loss_batch.backward()
        optimizer.step()

        #Add the batch loss to total training loss
        train_loss += train_loss_batch.item()

        n += 1
        if n/n_batches >= progress:
            print(f'Progress: {round(progress*100)}%')
            progress += 0.25

    #Pause the training and evaluate the model after every training epoch
    model.eval()
    valid_loss = 0
    accuracy = 0
    with torch.no_grad():
        for images, labels in validloader:
            #Load the labelled validation batch to the respective device
            images, labels = images.to(device), labels.to(device)

            #Forward pass
            logprob_valid = model.forward(images)
            valid_loss_batch = criterion(logprob_valid, labels)

            #Add batch loss to total validation loss
            valid_loss += valid_loss_batch.item()

            #Keep track of validation accuracy
            prob_valid = torch.exp(logprob_valid)
            top_p, top_class = prob_valid.topk(1, dim=1)
            equals = top_class == labels.view(top_class.shape[0], 1)
            accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

    #After evaluation switch back to training
    model.train()

    #Print out the training loss, validation loss, and validation accuracty
    #after every epoch
    print(f'Training (running) loss: {train_loss / len(trainloader):.4f}')
    print(f'Validation loss: {valid_loss / len(validloader):.4f}')
    print(f'Validation accuracy: {100 * accuracy / len(validloader):.4f}%')
    print('\n')

#Save the trained model as a checkpoint along with associated hyperparameters
#and the class_to_idx dictionary
checkpoint = {'model_state': model.state_dict(),
              'classtoidx': model.class_to_idx,
              'arch': args.arch,
              'hidden_units': hidden_units}
torch.save(checkpoint, args.save_dir)
