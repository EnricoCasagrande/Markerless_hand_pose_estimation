from Script.Model.whole_model import whole_model
from Script.Manage_dataset.Data_generator import data_gen
from Script import Predict
from keras.layers import Input
import numpy as np

BATCH_SIZE = 4      # Scelto da me abbastanza random, ragionevole
NO_OF_TESTING_IMAGES = len(os.listdir(test_frame_path))

def test(model, stride):

    test_frame_path = 'https://raw.githubusercontent.com/AlbertoGhiotto/group_project/master/Dataset/test_frames'
    test_gen = data_gen(test_frame_path, batch_size = BATCH_SIZE)

    predictions = model.predict_generator( test_gen, steps=(NO_OF_TESTING_IMAGES//BATCH_SIZE) )

    pose = Predict.argmax_predict(predictions, stride)

##### DA RICONTROLLARE

#DA AGGIUNGERE IL MODO DI VISUALIZZARE IL RISULTATO
