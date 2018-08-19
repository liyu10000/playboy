import tensorflow as tf

# # constant
# helloworld = tf.constant("Hello world!")

# with tf.Session() as sess:
# 	output = sess.run(helloworld)
# 	print(output)


# placeholder and feed_dict
x = tf.placeholder(tf.string)
y = tf.placeholder(tf.int32)
z = tf.placeholder(tf.float32)

with tf.Session() as sess:
	output = sess.run((x,y,z), feed_dict={x:"test string", y:123, z:34.53})
	print(output)