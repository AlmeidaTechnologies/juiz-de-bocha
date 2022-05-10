from datetime import datetime

start = datetime.now()

from recognizer import Recognizer
rec = Recognizer(
    # config_file='models/mask_rcnn_X_101_32x8d_FPN_3x/mask_rcnn_X_101_32x8d_FPN_3x.yaml',
    # weights_file='models/mask_rcnn_X_101_32x8d_FPN_3x/model_final_2d9806.pkl',
    config_file='models/mask_rcnn_R_50_FPN_3x/mask_rcnn_R_50_FPN_3x.yaml',
    weights_file='models/mask_rcnn_R_50_FPN_3x/model_final_f10217.pkl',
    confidence_threshold=0.1,
    # gpu_id=0,
)
# img = rec.read_file("datasets/Jogos de bocha/IMG-20220108-WA0016.jpg")
img = rec.read_file("datasets/Jogos de bocha/IMG-20220108-WA0037.jpg")
# img = rec.read_file("datasets/Jogos de bocha/1651761545.226486.7169.jpg")
# img = rec.read_file("datasets/Jogos de bocha/1650716891.458838.5922.jpg")

elapsed = datetime.now() - start
print("Startup:", int(elapsed.total_seconds()*1000), "ms")

######

start = datetime.now()

data = rec.predict_data(img)

elapsed = datetime.now() - start
print("Prediction:", int(elapsed.total_seconds()*1000), "ms")

# print(data)

rec.test(img)

# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4)

# Mandar foto identificada com 3 bolas e sem pessoas identificadas.
# Marcar número de cada

# Marcar qual é a bola
#
