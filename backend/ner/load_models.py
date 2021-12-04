

import tensorflow as tf



procedimiento = tf.keras.models.load_model('procedimiento/model-complete')
enfermedad = tf.keras.models.load_model('enfermedad/model-complete')
farmaco = tf.keras.models.load_model('farmaco/model-complete')
sintoma = tf.keras.models.load_model('sintoma/model-complete')

def get_predict(modelname, x ):
    if modelname == "procedimiento":
        return procedimiento.predict(x)
    if modelname == "enfermedad":
        return enfermedad.predict(x)
    if modelname == "farmaco":
        return farmaco.predict(x)
    if modelname == "sintoma":
        return sintoma.predict(x)
    