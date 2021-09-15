from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Embedding, Bidirectional
from tensorflow.keras.layers import Dense, Dropout, TimeDistributed, Activation,\
 Input, Multiply, Subtract, Add, Lambda, Average, concatenate
from tensorflow.keras.layers import LSTM, GRU, Conv1D
from tensorflow.keras.optimizers import Nadam
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras import regularizers
# from tf2crf import CRF, ModelWithCRFLoss # https://github.com/xuxingya/tf2crf
import os
def create_ner_model(maxSeqLength, maxCharLength, nChars, embeddingDim, vocabSize,
                 bpeDim, hiddenDim, dropout_bilstm, char_embedd_length,
                 char_LSTM_units, tensorboard_path, model_checkpoint_path, weight,
                 target, path, validation_split=0.15, mask=False,
                 use_crf=True, use_bpe=True):
    
    char_input = Input(shape=(maxSeqLength,
                          maxCharLength,), 
                   name='char_input')
    emb_char = Embedding(input_dim=nChars + 2,
                         output_dim=char_embedd_length, # NeuroNER: 25
                         input_length=maxCharLength,
                         mask_zero=True,
                         name='char_emb')(char_input)
    # I believe this TimeDistributed is unnecessary. We already have a 3D 
    # tensor, where the first dimension is the batch size. Keras should
    # already know that it has to pass every sentence at a time.

    char_enc = TimeDistributed(Bidirectional(LSTM(units=char_LSTM_units,  # NeuroNER: 25 (or 25x2??)
                                    return_sequences=False,
                                    recurrent_dropout=0.5), merge_mode='concat'),
                               name='bilstm_char_emb')(emb_char)
    # Since LSTM is TimeDistributed, I apply a LSTM to each word, which is
    # what I want! (see neuroner diagram: http://neuroner.com/)
    # TimeDistributed layer description in Keras:
    # This wrapper allows to apply a layer to every temporal slice of an input.
    # Consider a batch of 32 video samples, where each sample is a 128x128 RGB 
    # image with channels_last data format, across 10 timesteps. 
    # The batch input shape is (32, 10, 128, 128, 3).
    # You can then use TimeDistributed to apply the same Conv2D layer to 
    # each of the 10 timesteps, independently

    ### Word embedding ###
    word_input = Input(shape=(maxSeqLength,), dtype='int32', 
                       name='word_input')
    emb_word = Embedding(output_dim=embeddingDim,
                         input_dim=vocabSize,
                         input_length=maxSeqLength,
                         weights=weight,
                         mask_zero=mask,
                         trainable=False,
                         name='word_emb')(word_input)

    if use_bpe == True:
      ### BPE embedding ###
      bpe_input = Input(shape=(maxSeqLength,bpeDim,), dtype='float32', 
                        name='bpe_input')
      ### Concat embeddings ###
      emb = concatenate([emb_word, char_enc, bpe_input], name="input_concat")
    else:
      emb = concatenate([emb_word, char_enc], name="input_concat")

    ### Define inputs ###
    inputs = [word_input, char_input, bpe_input]
    
    ### Tag prediction ###
    bi_LSTM = Bidirectional(LSTM(hiddenDim, return_sequences=True), 
                            merge_mode='concat',
                            name='biLSTM')(emb)
    bi_RNN = Dropout(dropout_bilstm, name='dropout')(bi_LSTM)



    tag_pred = Dense(target, activation ='softmax',
                     kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),
                     name='classification')(bi_RNN) # Remove if https://github.com/xuxingya/tf2crf
    output = tag_pred

    ### Define model ###
    base_model = Model(inputs=inputs, outputs=output) # https://github.com/xuxingya/tf2crf

    return base_model