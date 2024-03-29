import tensorflow as tf


def calc_2_moments(tensor):
    """flattens tensor and calculates sample mean and covariance matrix
    along last dim (presumably channels)"""

    shape = tf.shape(tensor, out_type=tf.int32)
    n = tf.reduce_prod(shape[:-1])

    flat_array = tf.reshape(tensor, (n, shape[-1]))
    mu = tf.reduce_mean(flat_array, axis=0, keepdims=True)
    cov = tf.matmul(flat_array - mu, flat_array - mu, transpose_a=True) / tf.cast(
        n, tf.float32
    )

    return mu, cov


def calc_l2wass_dist(layer_style_desc, mean_synth, cov_synth):
    """Calculates (squared) l2-Wasserstein distance between gaussians
    parameterized by first two moments of style and synth activations"""

    mean_stl, tr_cov_stl, root_cov_stl = layer_style_desc

    tr_cov_synth = tf.reduce_sum(tf.maximum(tf.linalg.eigh(cov_synth)[0], 0.0))

    mean_diff_squared = tf.reduce_sum(tf.square(mean_stl - mean_synth))

    cov_prod = tf.matmul(tf.matmul(root_cov_stl, cov_synth), root_cov_stl)

    var_overlap = tf.reduce_sum(tf.sqrt(tf.maximum(tf.linalg.eigh(cov_prod)[0], 0.1)))

    dist = mean_diff_squared + tr_cov_stl + tr_cov_synth - 2 * var_overlap

    return dist
