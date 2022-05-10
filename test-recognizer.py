from recognizer import Recognizer
# import json

rec = Recognizer(
    config_file='models/mask_rcnn_X_101_32x8d_FPN_3x/mask_rcnn_X_101_32x8d_FPN_3x.yaml',
    weights_file='models/mask_rcnn_X_101_32x8d_FPN_3x/model_final_2d9806.pkl',
)

img = rec.read_file("datasets/Jogos de bocha/IMG-20220108-WA0016.jpg")

data = rec.predict_data(img)
print(data)
rec.test(img)

# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4)

# Mandar foto identificada com 3 bolas e sem pessoas identificadas.
# Marcar número de cada

# Marcar qual é a bola
#
