import argparse
import util
import classifier_util
import torch
from PIL import Image
import numpy as np
import json

""" This Python script is part of the developed command line application. It
loads a trained neural network and use it to predict the most likely
class for an input image (or top k most probable classes). The script has the
following input arguments:
- input : path to input image to be classified (required argument)
- checkpoint : saved trained neural network (required argument)
- top_k : number of most likely categories displayed
- category_names : mapping of categories to category names
- gpu : flag to run on GPU
"""

parser = argparse.ArgumentParser()
parser.add_argument('input', action = 'store')
parser.add_argument('checkpoint', action = 'store')
parser.add_argument('--top_k', action = 'store', dest = 'top_k', type = int, default = 1)
parser.add_argument('--category_names', action = "store", dest = 'category_names', default = 'cat_to_name.json')
parser.add_argument('--gpu', action = "store_true", default = True)

args = parser.parse_args()


#Load the checkpoint and rebuild the model
checkpoint = torch.load(args.checkpoint)
model = classifier_util.construct_model(checkpoint['arch'], checkpoint['hidden_units'])
#Load the trained weights
model.load_state_dict(checkpoint['model_state'])
model.class_to_idx = checkpoint['classtoidx']

#Select the device used for inference (either CPU or GPU/cuda)
device = 'cuda' if args.gpu else 'cpu'
model.to(device)

#Convert a PIL image into an object that can be used as input to a trained model
image = Image.open(args.input)
image_processed = torch.from_numpy(util.process_image(image)).float().to(device)

#Feed the input image to the model and calculate the output probabilities
model.eval()
logprob = model.forward(image_processed.resize_(1, 3, 224, 224))
prob = torch.exp(logprob)
#Categories with top k probabilities
top_p, top_index = prob.topk(args.top_k)

#Translate indices to categories
mapping = model.class_to_idx
inverse_mapping = {ind: cls for cls, ind in mapping.items()}

top_prob = top_p.detach().cpu().numpy().squeeze()
top_index_list = top_index.cpu().numpy().squeeze().tolist()

with open(args.category_names, 'r') as f:
    cat_to_name = json.load(f)

#Translate categories to category names
if args.top_k==1:
    top_classes = inverse_mapping[top_index_list]
    top_names = cat_to_name[top_classes]
else:
    print("inverse_mapping: ", inverse_mapping)
    print("top_index_list: ", top_index_list)
    top_classes = [inverse_mapping[elt] for elt in top_index_list]
    top_names = [cat_to_name[i] for i in top_classes]

print(top_names)
print(top_prob)
