import keras
from keras.layers import Dense, Activation, Conv2DTranspose, Reshape, Input, Add, Conv2D, Cropping2D, UpSampling2D
from keras.regularizers import l2
from keras import backend as K; 
from keras.models import Model
from keras.activations import sigmoid
import numpy as np
from resnet50_model import ResNet50

NUM_JOINTS = 16


def whole_model(input_tensor=None):
    
    #================================== ResNet =======================================
    # Importing the ResNet architecture pretrained on ImageNet
    resnet_model = ResNet50(weights='imagenet', include_top=False, input_tensor=input_tensor)
    
    # Set the resnet layers (except the last ones) to non trainable
    for layer in resnet_model.layers:         
        layer.trainable = False

    resnet_model.get_layer("res5c_branch2a").trainable = True 
    resnet_model.get_layer("res5c_branch2b").trainable = True  
    resnet_model.get_layer("res5c_branch2c").trainable = True
    
    #============================= Part classification ================================
    x = Conv2DTranspose(NUM_JOINTS, (3,3), strides=(2,2), activation = None)(resnet_model.output)  
    y = Conv2D(NUM_JOINTS, (1,1), strides=(1, 1))(resnet_model.get_layer("res4a_branch2a").input)
    #x = UpSampling2D(size=(2, 2))(x)
    x = Cropping2D(cropping=((1, 0), (0, 1)))(x)
    x = Add()([x, y]) 
    scmap = Activation('sigmoid',  name='scmap')(x)
    
    #============================= Location refinement ================================
    #z = Conv2DTranspose(NUM_JOINTS*2, (3,3), strides=(2,2), activation = None)(resnet_model.output)
    #y = Conv2D(NUM_JOINTS*2, (1,1), strides=(1, 1))(resnet_model.get_layer("res4a_branch2a").input)
    #z = UpSampling2D(size=(2, 2))(z)
    #z = Cropping2D(cropping=((1, 0), (0, 1)))(z)
    #locref = Add( name='locref')([z, y]) 
    
    #============================= Regression to other joints ==========================
    #w = Conv2DTranspose(364, (3,3), strides=(2,2), activation = None)(resnet_model.output)        
    #y = Conv2D(364, (1,1), strides=(1, 1))(resnet_model.get_layer("res4a_branch2a").input)
    #w = UpSampling2D(size=(2, 2))(w)
    #w = Cropping2D(cropping=(1, 1))(w)
    #w = Add()([w, y]) 
    
    #============================ Building the model ===================================
    
    #model = Model(inputs=resnet_model.input, outputs= [scmap, locref]) # In case of using also location refinement
    model = Model(inputs=resnet_model.input, outputs=scmap)
    
    model.compile( optimizer=Adam(lr=2E-4), loss=weighted_cross_entropy(0.8), metrics=['accuracy'] )
    
    return model
