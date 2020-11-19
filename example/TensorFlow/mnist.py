import math
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import os
import shutil
import sys
from tensorflow_on_slurm import tf_config_from_slurm

# Flags for defining the tf.train.ClusterSpec
tf.app.flags.DEFINE_string("ps_hosts", "",
                           "Comma-separated list of hostname:port pairs")
tf.app.flags.DEFINE_string("worker_hosts", "",
                           "Comma-separated list of hostname:port pairs")

# Flags for defining the tf.train.Server
tf.app.flags.DEFINE_string("job_name", "", "One of 'ps', 'worker'")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task within the job")
tf.app.flags.DEFINE_integer("hidden_units", 100,
                            "Number of units in the hidden layer of the NN")
tf.app.flags.DEFINE_string("data_dir", "/tmp/mnist-data",
                           "Directory for storing mnist data")
tf.app.flags.DEFINE_integer("batch_size", 100, "Training batch size")

FLAGS = tf.app.flags.FLAGS

IMAGE_PIXELS = 28

def main(_):
  # # Create a cluster from the parameter server and worker hosts.
  if os.path.exists("/tmp/train_logs"):
    shutil.rmtree("/tmp/train_logs")
  cluster, my_job_name, my_task_index = tf_config_from_slurm(ps_number=1)
  cluster_spec = tf.train.ClusterSpec(cluster)

  # Create and start a server for the local task.
  server = tf.train.Server(cluster_spec,
                           job_name=my_job_name,
                           task_index=my_task_index)

  if my_job_name == "ps":
    server.join()
  elif my_job_name == "worker":

    # Assigns ops to the local worker by default.
    with tf.device(tf.train.replica_device_setter(
        worker_device="/job:worker/task:%d" % my_task_index,
        cluster=cluster_spec)):

      # Variables of the hidden layer
      hid_w = tf.Variable(
          tf.truncated_normal([IMAGE_PIXELS * IMAGE_PIXELS, FLAGS.hidden_units],
                              stddev=1.0 / IMAGE_PIXELS), name="hid_w")
      hid_b = tf.Variable(tf.zeros([FLAGS.hidden_units]), name="hid_b")

      # Variables of the softmax layer
      sm_w = tf.Variable(
          tf.truncated_normal([FLAGS.hidden_units, 10],
                              stddev=1.0 / math.sqrt(FLAGS.hidden_units)),
          name="sm_w")
      sm_b = tf.Variable(tf.zeros([10]), name="sm_b")

      x = tf.placeholder(tf.float32, [None, IMAGE_PIXELS * IMAGE_PIXELS])
      y_ = tf.placeholder(tf.float32, [None, 10])

      hid_lin = tf.nn.xw_plus_b(x, hid_w, hid_b)
      hid = tf.nn.relu(hid_lin)

      y = tf.nn.softmax(tf.nn.xw_plus_b(hid, sm_w, sm_b))
      loss = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))

      global_step = tf.Variable(0)

      train_op = tf.train.AdagradOptimizer(0.01).minimize(
          loss, global_step=global_step)
      correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
      accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
      saver = tf.train.Saver()
      summary_op = tf.summary.merge_all()
      init_op = tf.initialize_all_variables()

    # Create a "supervisor", which oversees the training process.
    sv = tf.train.Supervisor(is_chief=(my_task_index == 0),
                             logdir="/tmp/train_logs",
                             init_op=init_op,
                             saver=saver,
                             summary_op=summary_op,
                             global_step=global_step,
                             save_model_secs=600)

    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    # The supervisor takes care of session initialization, restoring from
    # a checkpoint, and closing when done or an error occurs.
    with sv.managed_session(server.target) as sess:
      # Loop until the supervisor shuts down or 1000000 steps have completed.
      step = 0
      while not sv.should_stop() and step < 10000:
        # Run a training step asynchronously.
        # See `tf.train.SyncReplicasOptimizer` for additional details on how to
        # perform *synchronous* training.

        batch_xs, batch_ys = mnist.train.next_batch(FLAGS.batch_size)
        train_feed = {x: batch_xs, y_: batch_ys}

        _, step = sess.run([train_op, global_step], feed_dict=train_feed)
        if step % 1000 == 0:
            acc = sess.run([accuracy], feed_dict={x: mnist.test.images, y_: mnist.test.labels})
            # Compute the accuracy of the model on test data set.
            print("step:" , step,  "accuracy: ",  acc)


    # Ask for all the services to stop.
    tf.logging.info("Training process finished")
    sv.stop()

if __name__ == "__main__":
  tf.app.run()
