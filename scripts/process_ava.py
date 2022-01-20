import os
import scipy.io as sio
import numpy as np
from PIL import Image
import pickle
import csv
from tqdm import tqdm

def get_meta_info():
    """Generate meta information and train/val/test splits for AVA dataset.

    The split follows: 
        - split index 1: official 
        - split index 2: https://github.com/BestiVictory/ILGnet 
    """
    all_label_file = '../../datasets/AVA_dataset/AVA.txt'
    
    # read ILGnet split
    ILGnet_train_list = [x.strip().split()[0] for x in open('../../datasets/AVA_dataset/ILGnet_train.txt').readlines()]
    ILGnet_test_list = [x.strip().split()[0] for x in open('../../datasets/AVA_dataset/ILGnet_val.txt').readlines()]

    official_test_list = [x.strip().split()[0] + '.jpg' for x in open('../../datasets/AVA_dataset/official_test_challenges.txt')]

    save_meta_path = '../pyiqa/data/meta_info/meta_info_AVADataset.csv'
    split_info = {
        1: {'train': [], 'val': [], 'test': []},
        2: {'train': [], 'val': [], 'test': []},
        }
    
    with open(all_label_file) as f, open(save_meta_path, 'w+') as sf:
        csvwriter = csv.writer(sf)
        header = ['img_name'] + ['MOS'] + [f'c{i}' for i in range(1, 11)] + ['semantic_tag1', 'semantic_tag2'] + ['official split', 'ILGnet split']
        csvwriter.writerow(header)
        count = 0
        for row in tqdm(f.readlines()):
            row = row.strip().split() 
            ratings = np.array([int(x) for x in row[2:12]])
            # calculate mos
            mos = np.sum(np.arange(1, 11) * ratings) / np.sum(ratings)
            new_row = [row[1] + '.jpg', mos] + row[2: 14]
            img_path = os.path.join('../../datasets/AVA_dataset/ava_images/', new_row[0])
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    w, h = img.size
                    if w > 10 and h > 10:
                        if new_row[0] in official_test_list:
                            split_info[1]['test'].append(count)
                            official_split = 2
                        else:
                            split_info[1]['train'].append(count)
                            official_split = 0

                        if new_row[0] in ILGnet_test_list:
                            split_info[2]['test'].append(count)
                            ilgnet_split = 2
                        else:
                            split_info[2]['train'].append(count)
                            ilgnet_split = 0

                        new_row += [official_split, ilgnet_split]
                        csvwriter.writerow(new_row)
                        count += 1
                except:
                    print(f'{img_path} image is broken')
    print(len(split_info[1]['train']), len(split_info[1]['test']))
    print(len(split_info[2]['train']), len(split_info[2]['test']))
    save_split_path = '../pyiqa/data/train_split_info/ava_official_ilgnet.pkl'
    with open(save_split_path, 'wb') as sf:
        pickle.dump(split_info, sf)

if __name__ == '__main__':
    get_meta_info()
    #  get_random_splits()
