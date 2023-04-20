import tensorflow as tf


class JustDanceModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

    def run_inference(self, input_image):
        input_image = tf.cast(input_image, dtype=tf.float32)
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.interpreter.set_tensor(input_details[0]["index"], input_image.numpy())
        self.interpreter.invoke()
        key_points_with_scores = self.interpreter.get_tensor(output_details[0]["index"])
        return key_points_with_scores
