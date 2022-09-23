import os
import importlib
from tqdm import tqdm

function = importlib.import_module('cloud-run-function.main')

base_dir = '/media/viniciusas/Elements/Datasets/JuizDeBocha/juizdebocha-raw'

raw_dir = f'{base_dir}/raw'
output_dir = f'{base_dir}/output'

for filename in tqdm(os.listdir(raw_dir)):
    raw = os.path.join(raw_dir, filename)
    output = os.path.join(output_dir, filename + '.gif')
    with open(raw, 'rb') as raw_file:
        result = function._process_image(raw_file.read())
    with open(output, 'wb') as output_file:
        output_file.write(function._to_gif_bytes(result))

# foreach sample

