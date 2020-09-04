from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf


AUTOTUNE = tf.data.experimental.AUTOTUNE



#path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)



import pathlib
data_root_orig = tf.keras.utils.get_file(origin='https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',fname='flower_photos', untar=True)
data_root = pathlib.Path(data_root_orig)
print(data_root)

import random
all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)


path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

for img_path in all_image_paths:

    img_raw = tf.io.read_file(img_path)
    img_tensor = tf.image.decode_image(img_raw)
    

    print(img_tensor.shape)
    print(img_tensor.dtype)




print()
