import os
import torch
import argparse
import numpy as np
from PIL import Image

import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

from model import network
from datasets import SCHPDataset, transform_logits

dataset_settings = {
    'lip': {
        'input_size': [473, 473],
        'num_classes': 20,
        'label': ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat',
                  'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm',
                  'Left-leg', 'Right-leg', 'Left-shoe', 'Right-shoe']
    },
    'atr': {
        'input_size': [512, 512],
        'num_classes': 18,
        'label':['Background', 'Hat', 'Hair', 'Sunglasses', 'Upper-clothes', 'Skirt', 'Pants', 'Dress', 'Belt',
                 'Left-shoe', 'Right-shoe', 'Face', 'Left-leg', 'Right-leg', 'Left-arm', 'Right-arm', 'Bag', 'Scarf']
    },
    'pascal': {
        'input_size': [512, 512],
        'num_classes': 7,
        'label': ['Background', 'Head', 'Torso', 'Upper Arms', 'Lower Arms', 'Upper Legs', 'Lower Legs'],
    }
}

def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette


def get():
    # args = get_arguments()

    num_classes = dataset_settings['lip']['num_classes']
    input_size = dataset_settings['lip']['input_size']
    label = dataset_settings['lip']['label']

    model = network(num_classes=num_classes, pretrained=None)
    model = nn.DataParallel(model)
    state_dict = torch.load('./exp-schp-201908261155-lip.pth')
    model.load_state_dict(state_dict)
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.406, 0.456, 0.485], std=[0.225, 0.224, 0.229])
    ])
    dataset = SCHPDataset(root='./static/Database/val/person/', input_size=input_size, transform=transform)
    dataloader = DataLoader(dataset)

    if not os.path.exists('./static/Database/val/person-parse'):
        os.makedirs('./static/Database/val/person-parse')

    palette = get_palette(num_classes)

    with torch.no_grad():
        for idx, batch in enumerate(dataloader):

            image, meta = batch
            img_name = meta['name'][0]
            c = meta['center'].numpy()[0]
            s = meta['scale'].numpy()[0]
            w = meta['width'].numpy()[0]
            h = meta['height'].numpy()[0]

            output = model(image)
            upsample = torch.nn.Upsample(size=input_size, mode='bilinear', align_corners=True)
            upsample_output = upsample(output)
            upsample_output = upsample_output.squeeze()
            upsample_output = upsample_output.permute(1, 2, 0) #CHW -> HWC

            logits_result = transform_logits(upsample_output.data.cpu().numpy(), c, s, w, h, input_size=input_size)
            parsing_result = np.argmax(logits_result, axis=2)

            parsing_result_path = os.path.join('./static/Database/val/person-parse', img_name[:-4]+'.png')
            output_img = Image.fromarray(np.asarray(parsing_result, dtype=np.uint8))
            output_img.putpalette(palette)
            output_img.save(parsing_result_path)
            # if args.logits:
            #     logits_result_path = os.path.join(args.output, img_name[:-4] + '.npy')
            #     np.save(logits_result_path, logits_result)
    return
