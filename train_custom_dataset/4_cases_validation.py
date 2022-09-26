from recognizer import Recognizer
import os
import importlib
from tqdm import tqdm

function = importlib.import_module('cloud-run-function.main')
function._rec = Recognizer(
    config_file='../models/mask_rcnn_juiz_de_bocha_custom/mask_rcnn_juiz_de_bocha.yaml',
    weights_file='../train_custom_dataset/training/model_final.pth',
    confidence_threshold=0.9,
    gpu_id=0,
)


error_cases = {
    "strange balim": [
        '1663869724.345396.5542.jpg',
        '1663700877.340262.7389.jpg',
        '1663869495.713955.5540.jpg',
        '1653334418.803285.6726.jpg',
        '1653334432.121146.6727.jpg',
        '1654888507.255648.4815.jpg',
        '1655659635.85541.4882.jpg',
        '1655659557.171255.4881.jpg',
        '1655732394.541147.8157.jpg',
        '1655732446.783515.8320.jpg',
        '1655734887.477421.8376.jpg',
        '1655735015.830903.8379.jpg',
        '1655734955.103472.8378.jpg',
        '1655734935.598222.8377.jpg',
        '1655843589.142564.5194.jpg',
        '1656516663.022229.4892.jpg',
        '1656959989.414534.9422.jpg',
        '1656960145.767386.9425.jpg',
        '1657139008.338589.2250.jpg',
        '1657136093.914774.9490.jpg',
        '1657655660.04412.2848.jpg',
        '1657905506.530785.6643.jpg',
        '1658257544.458747.3460.jpg',
        '1658258222.471058.3462.jpg',
        '1658431598.084598.1935.jpg',
        '1658601045.127676.6222.jpg',
        '1660243597.872832.785.jpg',
        '1662402730.00121.1368.jpg',
        '1662402444.418346.1367.jpg',
        '1663269964.875002.2060.jpg',
    ],
    "balim in dirt": [
        '1658921757.591203.4547.jpg',
        '1658921736.74386.4546.jpg',
        '1658921720.465124.4545.jpg',
        '1658921702.765388.4544.jpg',
        '1658921684.859911.4543.jpg',
        '1658921665.89887.4542.jpg',
        '1658921640.855864.4541.jpg',
        '1658921497.49266.4540.jpg',
        '1658921444.341192.4539.jpg',
        '1663270593.932687.2072.jpg',
        '1663353911.24066.930.jpg',
        '1663355392.043358.7998.jpg',
        '1663354029.739854.932.jpg',
        '1663353941.359942.931.jpg',
        '1663357215.946784.8006.jpg',
        '1663357007.527574.8005.jpg',
        '1663356954.729912.8004.jpg',
        '1663355864.921186.8002.jpg',
        '1663603897.379339.883.jpg',
        '1663617239.681089.482.jpg',
        '1663616573.410785.479.jpg',
        '1663869724.345396.5542.jpg',
        '1663869495.713955.5540.jpg',
        '1663783226.755644.6090.jpg',
        '1663783138.146048.6089.jpg',
        '1663782377.503888.6086.jpg',
    ],
    "strange ball": [
        '1654976228.170048.4509.jpg',
        '1654976590.778779.4511.jpg',
        '1654976628.831632.9415.jpg',
        '1654976628.831632.9415.jpg',
        '1655058276.033827.8085.jpg',
        '1655058258.854729.8084.jpg',
        '1655732394.541147.8157.jpg',
        '1655732406.218069.8158.jpg',
        '1655732446.783515.8320.jpg',
        '1655732662.419898.8161.jpg',
        '1655732945.349575.8332.jpg',
        '1655733001.764488.8333.jpg',
        '1655733373.521001.8343.jpg',
        '1655733271.60124.8340.jpg',
        '1655733161.659915.8338.jpg',
        '1655733111.471325.8336.jpg',
        '1655733463.875036.8345.jpg',
        '1655734147.854369.8031.jpg',
        '1655733837.651941.8354.jpg',
        '1657905506.530785.6643.jpg',
    ],
    "strange ball/blurred": [
        '1658598943.612881.5521.jpg',
    ],
    "strange ball/sand": [
        '1655734467.57142.8367.jpg',
        '1655734360.611805.8364.jpg',
        '1655734206.282715.8361.jpg',
        '1655734764.054396.8373.jpg',
        '1655734646.867809.8371.jpg',
        '1655734529.076342.8369.jpg',
        '1656960041.893141.9423.jpg',
        '1656962787.496812.1594.jpg',
    ],
    "strange ball/sand and shadow": [
        '1655735071.324975.8381.jpg',
        '1655735168.783775.8382.jpg',
        '1655735194.67074.8383.jpg',
        '1655735265.773664.8384.jpg',
        '1655735168.835196.8034.jpg',
        '1658922702.52447.4548.jpg',
    ],
    "strange ball/leaves": [
        '1655818800.628161.8975.jpg',
        '1655819086.265331.8979.jpg',
    ],
    "strange ball/tenis": [
        '1655819044.343191.8978.jpg',
        '1655818882.341532.8977.jpg',
        '1658490081.283097.9868.jpg',
        '1663269696.883801.2057.jpg',
        '1663603425.554494.874.jpg',
        '1663700658.537285.7385.jpg',
        '1663700983.251971.7390.jpg',
    ],
    "strange ball/fruits": [
        '1655819115.584588.8980.jpg',
        '1655819143.365243.8981.jpg',
        '1655819296.290269.8984.jpg',
        '1655819227.169209.8983.jpg',
        '1655819191.226152.8982.jpg',
        '1655819416.566877.8986.jpg',
    ],
    "strange ball/pants": [
        '1656962293.992941.1584.jpg',
    ],
    "strange ball/cutted ball": [
        '1659377850.48616.2952.jpg',
        '1659641353.705282.9057.jpg',
    ],
    "balim not identified": [
        '1656094585.410888.8802.jpg',
    ],
    "balim not identified/silver": [
        '1654974849.204714.1254.jpg',
        '1655062946.269487.2895.jpg',
        '1655146249.677424.3921.jpg',
        '1655842950.212702.5188.jpg',
        '1655843359.704781.5193.jpg',
        '1655843216.113019.5191.jpg',
        '1656089714.10168.7355.jpg',
        '1656700146.395792.5396.jpg',
        '1656961193.218083.1560.jpg',
        '1656961098.110656.1558.jpg',
        '1656961309.163019.1562.jpg',
        '1656961434.742014.1565.jpg',
        '1656961474.299468.1566.jpg',
        '1656963065.080966.1601.jpg',
        '1657043244.108397.7781.jpg',
        '1658230711.253908.1155.jpg',
        '1658230664.734316.1154.jpg',
        '1658230631.473948.1153.jpg',
        '1658324760.131843.9734.jpg',
        '1658324721.227617.9733.jpg',
        '1658323125.950116.6001.jpg',
        '1658403900.219694.2886.jpg',
        '1658403800.210326.2882.jpg',
        '1658343771.804792.6362.jpg',
        '1658407008.515636.904.jpg',
        '1658406662.302061.902.jpg',
        '1658404788.819804.2898.jpg',
        '1658490125.065168.9869.jpg',
        '1658407830.265207.919.jpg',
        '1659121799.090621.4164.jpg',
        '1659642061.887854.9058.jpg',
        '1663270392.449397.2067.jpg',
    ],
    "balim not identified/home floor": [
        '1662984516.940194.5325.jpg',
        '1662966500.723599.5962.jpg',
        '1662966441.425613.5961.jpg',
        '1662992968.661219.2536.jpg',
    ],
    "leaves": [
        '1654093409.927885.746.jpg',
        '1654093461.940733.747.jpg',
    ],
    "ball not identified": [
        '1654976228.170048.4509.jpg',
        '1654976274.97021.4510.jpg',
        '1656009360.150329.9649.jpg',
        '1656186626.371955.821.jpg',
        '1657219215.691542.1268.jpg',
        '1658322939.591847.6000.jpg',
        '1658404526.496078.2896.jpg',
    ],
    "ball not identified/dog": [
        '1657533873.985111.6603.jpg',
    ],
}


base_dir = '../datasets/juizdebocha-raw'
raw_dir = f'{base_dir}/raw'
output_dir = f'{base_dir}/output_cases'

for case, samples in error_cases.items():
    for sample in tqdm(samples, desc=f"Testing case {case}"):
        output_folder = output_dir + '/' + case
        os.makedirs(output_folder, exist_ok=True)

        raw = os.path.join(raw_dir, sample)
        output = os.path.join(output_folder, sample + '.gif')
        with open(raw, 'rb') as raw_file:
            # process
            result = function._process_image(raw_file.read())
        # write to output folder
        with open(output, 'wb') as output_file:
            output_file.write(function._to_gif_bytes(result))
