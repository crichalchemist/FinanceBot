import logging

import numpy as np
import tensorflow as tf


class OptimizedModelManager:
    def __init__(self, model_path="models/trading_model.tflite"):
        self.model_path = model_path
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_index = self.interpreter.get_input_details()[0]['index']
        self.output_index = self.interpreter.get_output_details()[0]['index']
        logging.info("OptimizedModelManager initialized.")

    def predict(self, features):
        """
        Run inference using the TensorFlow Lite model.
        :param features: Input features as a 2D array.
        :return: Prediction scores.
        """
        try:
            self.interpreter.set_tensor(self.input_index, np.array(features, dtype=np.float32))
            self.interpreter.invoke()
            return self.interpreter.get_tensor(self.output_index)
        except Exception as e:
            logging.error(f"Error during model prediction: {e}")
            return [0]  # Default to neutral prediction on failure
