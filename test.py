import tensorflow as tf


n_hidden_layers = 0
n_hidden_nodes = []
learning_rate = 0.
activation = 'tahn'

x_train, y_train = [], []
x_test, y_test = [], []
with open('dataset2.csv', 'r') as f:
	lines = f.readlines()
	i = 0
	for line in lines:
		if i < 100:
			x_train.append([float(line.replace('\n', '').split(',')[0]), float(line.replace('\n', '').split(',')[1])])
			y_ = [float(line.replace('\n', '').split(',')[2])]
			if y_ == 1.0:
				y_train.append([0, 1])
			else:
				y_train.append([1, 0])
		else:
			x_test.append([float(line.replace('\n', '').split(',')[0]), float(line.replace('\n', '').split(',')[1])])
			y_ = [float(line.replace('\n', '').split(',')[2])]
			if y_ == 1.0:
				y_test.append([0, 1])
			else:
				y_test.append([1, 0])
		i += 1


x = tf.placeholder(tf.float32, [None, 2])
y = tf.placeholder(tf.float32, [None, 2])

'''
w1 = tf.Variable(tf.truncated_normal([2, n_hidden_nodes]))
b1 = tf.Variable(tf.truncated_normal([n_hidden_nodes]))
w2 = tf.Variable(tf.truncated_normal([n_hidden_nodes, 2]))
b2 = tf.Variable(tf.truncated_normal([2]))

hl = tf.nn.relu(tf.matmul(x, w1) + b1)
logits = tf.matmul(hl, w2) + b2
'''
def model():
	layers = []
	activation_funcs = {'relu': tf.nn.relu, 'tanh': tf.nn.tanh, 'sigmoid': tf.nn.sigmoid}
	for layer in range(n_hidden_layers):
		if layer == 0:
			layers.append(tf.layers.dense(
				inputs=x,
				units=n_hidden_nodes[layer],
				activation=activation_funcs[activation]))
		else:
			layers.append(tf.layers.dense(
				inputs=layers[layer-1],
				units=n_hidden_nodes[layer],
				activation=tf.nn.relu))

	logits = tf.layers.dense(
		inputs=x,
		units=2)
	out = tf.nn.softmax(logits)

	loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
	optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

	correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(out, 1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	return accuracy, loss, optimizer

accuracy, loss, optimizer = model()

init = tf.global_variables_initializer()
with tf.Session() as sess:
	sess.run(init)
	for i in range(10):
		sess.run(optimizer, {x: x_train, y: y_train})
		print(sess.run(accuracy, {x: x_test, y: y_test}), sess.run(loss, {x: x_test, y: y_test}))