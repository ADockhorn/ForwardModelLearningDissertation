import numpy as np
import os


game_names = ["Pong", "Qbert", "MontezumaRevenge", "MsPacman", "Phoenix", "SpaceInvaders", "Assault", "Boxing", "Breakout", "Freeway"]
outputs = ["v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0"]
train_files = 50
NUM_EPOCH = 200
NUM_THREADS = 32

for game_name, output in zip(game_names, outputs):
    downsampled = []
    actions = []
    rewards = []

    record_files = [filename for filename in os.listdir(f'./record/{game_name}')
                    if os.path.isfile(f"./record/{game_name}/{filename}") and filename.startswith(f"record_{game_name}")]
    record_files = sorted(record_files, key=lambda x: int(x.split(".")[0].split("_")[-1]))
    for file in record_files[0:train_files]:
        print("load file: ", file)
        data = np.load(f"./record/{game_name}/{file}", allow_pickle=True)
        if len(downsampled) == 0:
            downsampled = data["obs_downsampled"]
            actions = data["actions"]
            rewards = data["rewards"]
        else:
            downsampled = np.concatenate((downsampled, data["obs_downsampled"]))
            actions = np.concatenate((actions, data["actions"]))
            rewards = np.concatenate((rewards, data["rewards"]))

    obs_train_downsampled = downsampled / 255.
    actions_train = actions
    rewards_train = rewards

    print("loaded obs_train_downsampled: ", downsampled.shape)
    print("loaded actions_train: ", actions.shape)
    print("loaded rewards_train: ", rewards.shape)

    downsampled = []
    actions = []
    rewards = []

    for file in record_files[train_files:(train_files*2)]:
        print("load file: ", file)
        data = np.load(f"./record/{game_name}/{file}", allow_pickle=True)
        if len(downsampled) == 0:
            downsampled = data["obs_downsampled"]
            # original = data["obs_original"]
            actions = data["actions"]
            rewards = data["rewards"]
        else:
            downsampled = np.concatenate((downsampled, data["obs_downsampled"]))
            # original = np.concatenate((original, data["obs_original"]))
            actions = np.concatenate((actions, data["actions"]))
            rewards = np.concatenate((rewards, data["rewards"]))

    obs_test_downsampled = downsampled / 255.
    # obs_test = original / 255.
    actions_test = actions
    rewards_test = rewards

    print("loaded obs_test_downsampled: ", downsampled.shape)
    # print("loaded obs_test: ", original.shape)
    print("loaded actions_test: ", actions.shape)
    print("loaded rewards_test: ", rewards.shape)

    ## Simple Auto-Encoder
    def pad_along_axis(array: np.ndarray, target_length, axis=0):
        npad = [(0, 0) for _ in range(len(array.shape))]

        for axes in axis:

            pad_size = (target_length - array.shape[axes])
            if pad_size % 2 == 0:
                npad[axes] = (pad_size // 2, pad_size // 2)
            else:
                npad[axes] = (pad_size // 2, pad_size // 2 + 1)

        b = np.pad(array, pad_width=npad, mode='constant', constant_values=0)

        return b


    ## Simple Convolutional Variational Auto-Encoder
    import numpy as np
    import json
    import tensorflow as tf

    def reset_graph():
        if 'sess' in globals() and sess:
            sess.close()
        tf.reset_default_graph()


    class ConvVAE(object):
        def __init__(self, z_size=32, batch_size=1, learning_rate=0.0001, kl_tolerance=0.5, is_training=False,
                     reuse=False, gpu_mode=False):
            self.z_size = z_size
            self.batch_size = batch_size
            self.learning_rate = learning_rate
            self.is_training = is_training
            self.kl_tolerance = kl_tolerance
            self.reuse = reuse

            with tf.variable_scope('conv_vae', reuse=self.reuse):
                if not gpu_mode:
                    with tf.device('/cpu:0'):
                        tf.logging.info('Model using cpu.')
                        self._build_graph()
                else:
                    tf.logging.info('Model using gpu.')
                    self._build_graph()
            self._init_session()

        def _build_graph(self):
            self.g = tf.Graph()
            with self.g.as_default():

                self.x = tf.placeholder(tf.float32, shape=[None, 64, 64, 3])

                # Encoder
                h = tf.layers.conv2d(self.x, 32, 4, strides=2, activation=tf.nn.relu, name="enc_conv1")
                h = tf.layers.conv2d(h, 64, 4, strides=2, activation=tf.nn.relu, name="enc_conv2")
                h = tf.layers.conv2d(h, 128, 4, strides=2, activation=tf.nn.relu, name="enc_conv3")
                h = tf.layers.conv2d(h, 256, 4, strides=2, activation=tf.nn.relu, name="enc_conv4")
                h = tf.reshape(h, [-1, 2 * 2 * 256])

                # VAE
                self.mu = tf.layers.dense(h, self.z_size, name="enc_fc_mu")
                self.logvar = tf.layers.dense(h, self.z_size, name="enc_fc_log_var")
                self.sigma = tf.exp(self.logvar / 2.0)
                self.epsilon = tf.random_normal([self.batch_size, self.z_size])
                self.z = self.mu + self.sigma * self.epsilon

                # Decoder
                h = tf.layers.dense(self.z, 4 * 256, name="dec_fc")
                h = tf.reshape(h, [-1, 1, 1, 4 * 256])
                h = tf.layers.conv2d_transpose(h, 128, 5, strides=2, activation=tf.nn.relu, name="dec_deconv1")
                h = tf.layers.conv2d_transpose(h, 64, 5, strides=2, activation=tf.nn.relu, name="dec_deconv2")
                h = tf.layers.conv2d_transpose(h, 32, 6, strides=2, activation=tf.nn.relu, name="dec_deconv3")
                self.y = tf.layers.conv2d_transpose(h, 3, 6, strides=2, activation=tf.nn.sigmoid, name="dec_deconv4")

                # train ops
                if self.is_training:
                    self.global_step = tf.Variable(0, name='global_step', trainable=False)

                    eps = 1e-6  # avoid taking log of zero

                    # reconstruction loss
                    self.r_loss = tf.reduce_sum(
                        tf.square(self.x - self.y),
                        reduction_indices=[1, 2, 3]
                    )
                    self.r_loss = tf.reduce_mean(self.r_loss)

                    # augmented kl loss per dim
                    self.kl_loss = - 0.5 * tf.reduce_sum(
                        (1 + self.logvar - tf.square(self.mu) - tf.exp(self.logvar)),
                        reduction_indices=1
                    )
                    self.kl_loss = tf.maximum(self.kl_loss, self.kl_tolerance * self.z_size)
                    self.kl_loss = tf.reduce_mean(self.kl_loss)

                    self.loss = self.r_loss + self.kl_loss

                    # training
                    self.lr = tf.Variable(self.learning_rate, trainable=False)
                    self.optimizer = tf.train.AdamOptimizer(self.lr)
                    grads = self.optimizer.compute_gradients(self.loss)  # can potentially clip gradients here.

                    self.train_op = self.optimizer.apply_gradients(
                        grads, global_step=self.global_step, name='train_step')

                # initialize vars
                self.init = tf.global_variables_initializer()

                t_vars = tf.trainable_variables()
                self.assign_ops = {}
                for var in t_vars:
                    # if var.name.startswith('conv_vae'):
                    pshape = var.get_shape()
                    pl = tf.placeholder(tf.float32, pshape, var.name[:-2] + '_placeholder')
                    assign_op = var.assign(pl)
                    self.assign_ops[var] = (assign_op, pl)

        def _init_session(self):
            """Launch TensorFlow session and initialize variables"""
            self.sess = tf.Session(graph=self.g, config=tf.ConfigProto(intra_op_parallelism_threads=NUM_THREADS))
            self.sess.run(self.init)

        def close_sess(self):
            """ Close TensorFlow session """
            self.sess.close()

        def encode(self, x):
            return self.sess.run(self.z, feed_dict={self.x: x})

        def encode_mu_logvar(self, x):
            (mu, logvar) = self.sess.run([self.mu, self.logvar], feed_dict={self.x: x})
            return mu, logvar

        def decode(self, z):
            return self.sess.run(self.y, feed_dict={self.z: z})

        def decode_mu_logvar(self, mu, logvar):
            return self.sess.run(self.y, feed_dict={self.mu: mu, self.logvar: logvar})

        def get_model_params(self):
            # get trainable params.
            model_names = []
            model_params = []
            model_shapes = []
            with self.g.as_default():
                t_vars = tf.trainable_variables()
                for var in t_vars:
                    # if var.name.startswith('conv_vae'):
                    param_name = var.name
                    p = self.sess.run(var)
                    model_names.append(param_name)
                    params = np.round(p * 10000).astype(np.int).tolist()
                    model_params.append(params)
                    model_shapes.append(p.shape)
            return model_params, model_shapes, model_names

        def get_random_model_params(self, stdev=0.5):
            # get random params.
            _, mshape, _ = self.get_model_params()
            rparam = []
            for s in mshape:
                # rparam.append(np.random.randn(*s)*stdev)
                rparam.append(np.random.standard_cauchy(s) * stdev)  # spice things up
            return rparam

        def set_model_params(self, params):
            with self.g.as_default():
                t_vars = tf.trainable_variables()
                idx = 0
                for var in t_vars:
                    # if var.name.startswith('conv_vae'):
                    pshape = tuple(var.get_shape().as_list())
                    p = np.array(params[idx])
                    assert pshape == p.shape, "inconsistent shape"
                    assign_op, pl = self.assign_ops[var]
                    self.sess.run(assign_op, feed_dict={pl.name: p / 10000.})
                    idx += 1

        def load_json(self, jsonfile='vae.json'):
            with open(jsonfile, 'r') as f:
                params = json.load(f)
            self.set_model_params(params)

        def save_json(self, jsonfile='vae.json'):
            model_params, model_shapes, model_names = self.get_model_params()
            qparams = []
            for p in model_params:
                qparams.append(p)
            with open(jsonfile, 'wt') as outfile:
                json.dump(qparams, outfile, sort_keys=True, indent=0, separators=(',', ': '))

        def set_random_params(self, stdev=0.5):
            rparam = self.get_random_model_params(stdev)
            self.set_model_params(rparam)

        def save_model(self, model_save_path):
            sess = self.sess
            with self.g.as_default():
                saver = tf.train.Saver(tf.global_variables())
            checkpoint_path = os.path.join(model_save_path, 'vae')
            tf.logging.info('saving model %s.', checkpoint_path)
            saver.save(sess, checkpoint_path, 0)  # just keep one

        def load_checkpoint(self, checkpoint_path):
            sess = self.sess
            with self.g.as_default():
                saver = tf.train.Saver(tf.global_variables())
            ckpt = tf.train.get_checkpoint_state(checkpoint_path)
            print('loading model', ckpt.model_checkpoint_path)
            tf.logging.info('Loading model %s.', ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)


    # %%
    # Hyperparameters for ConvVAE
    z_size = 32
    batch_size = 64
    learning_rate = 0.0001
    kl_tolerance = 0.5

    vae = ConvVAE(z_size=z_size,
                  batch_size=batch_size,
                  learning_rate=learning_rate,
                  kl_tolerance=kl_tolerance,
                  is_training=True,
                  reuse=False,
                  gpu_mode=False)

    reset_graph()
    total_epochs = 0

    # %%
    dataset = obs_train_downsampled

    total_length = len(dataset)
    num_batches = int(np.floor(total_length / batch_size))
    print(f"num_batches per epoch = {num_batches}")

    # train loop:

    print("train", "step", "loss", "recon_loss", "kl_loss")
    for epoch in range(NUM_EPOCH):
        print(f"epoch: {epoch}")
        np.random.shuffle(dataset)
        for idx in range(num_batches):
            batch = dataset[idx * batch_size:(idx + 1) * batch_size]

            obs = batch.astype(np.float)
            # obs = pad_along_axis(obs, 256, axis=[1,2])

            feed = {vae.x: obs, }
            (train_loss, r_loss, kl_loss, train_step, _) = vae.sess.run([
                vae.loss, vae.r_loss, vae.kl_loss, vae.global_step, vae.train_op
            ], feed)

            if (train_step + 1) % 10 == 0:
                print("step", (train_step + 1), train_loss, r_loss, kl_loss)

        total_epochs += 1

        if total_epochs in {1, 2, 5, 10} or total_epochs % 10 == 0:
            vae.save_json(f"tf_vae/vae_epochs_{game_name}_{total_epochs}.json")

    # %%
    print(total_epochs)
    print(f"finished learning vae for {game_name}")
