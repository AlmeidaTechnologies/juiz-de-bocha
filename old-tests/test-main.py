import json
import main
from PIL import Image
import numpy as np

# img = 'datasets/Jogos de bocha/IMG-20220108-WA0016.jpg'
img = 'datasets/Jogos de bocha/IMG-20220108-WA0029.jpg'
img = 'datasets/Jogos de bocha/IMG-20220108-WA0030.jpg'

class Test:
    files = {
        'img': img,
    }


instances = main.process_image(Test())

# print(data)
#
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4)
im = main.rec.read_file(img)

print('n instances:', len(instances))

for i, instance in enumerate(instances):
    # mask_colored = np.zeros(instance['mask'].shape + [3])
    # mask_colored[]
    # print(im.shape)
    # print(instance['box'])
    # print(instance['mask'].shape)
    # print(im[int(instance['box']['y1']):int(instance['box']['y2']), int(instance['box']['x1']):int(instance['box']['x2']), :].shape)
    # im[
    #     int(instance['box']['y1']):int(instance['box']['y2']),
    #     int(instance['box']['x1']):int(instance['box']['x2']),
    # ][instance['mask']] = (255, 255, 255)
    color = [0, 0, 0]
    if i == 0:
        color = [255, 255, 255]
    elif i == 1:
        color = [100, 200, 100]
    else:
        color = [200, 100, 100]
    print(color)
    im[instance['mask']] = np.array(color, dtype=np.uint8)

img = Image.fromarray(im)
img.save('test.png')
