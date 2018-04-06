from flask import Blueprint, request, jsonify
from cStringIO import StringIO
import tensorflow as tf
import sys
import re

_model = Blueprint('_model', __name__)

# Model parameters
input_layer = 3
hidden_layers = []
output_layer = 2

activation = 'Tanh'
learning_rate = 0.01
problem_type = 'Classification'

data = []

def process_data():
    x_train, y_train = [], []
    x_test, y_test = [], []
    i = 0
    for row in data:
        if i < int(0.8*len(data)):
            x_train.append([float(row.replace('\n', '').split(',')[0]), float(row.replace('\n', '').split(',')[1])])
            y_ = [float(row.replace('\n', '').split(',')[2])]
            if y_ == 1.0:
                y_train.append([0, 1])
            else:
                y_train.append([1, 0])
        else:
            x_test.append([float(row.replace('\n', '').split(',')[0]), float(row.replace('\n', '').split(',')[1])])
            y_ = [float(row.replace('\n', '').split(',')[2])]
            if y_ == 1.0:
                y_test.append([0, 1])
            else:
                y_test.append([1, 0])
        i += 1
    return x_train, y_train, x_test, y_test

def get_data():
    with open('dataset.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.replace('\n', ''))

@_model.route('/generate_model', methods=['GET', 'POST'])
def generateModel():
    global input_layer
    input_layer = int(request.json['input_layer'])
    global hidden_layers
    hidden_layers = list(request.json['hidden_layers'])
    for i in range(len(hidden_layers)):
        hidden_layers[i]  = int(hidden_layers[i])
    global output_layer
    output_layer = int(request.json['output_layer'])
    global activation
    activation = str(request.json['activation']).lower()
    global learning_rate
    learning_rate = float(request.json['learning_rate'])
    global problem_type
    problem_type = str(request.json['problem_type']).lower()
    return jsonify('success')

def model():
    layers = []
    activation_funcs = {'relu': tf.nn.relu, 'tanh': tf.nn.tanh, 'sigmoid': tf.nn.sigmoid}
    for layer in range(len(hidden_layers)):
        if layer == 0:
            layers.append(tf.layers.dense(
                inputs=x,
                units=hidden_layers[layer],
                activation=activation_funcs[activation]))
        else:
            layers.append(tf.layers.dense(
                inputs=layers[layer-1],
                units=hidden_layers[layer],
                activation=activation_funcs[activation]))

    if len(layers) != 0:
        logits = tf.layers.dense(
            inputs=layers[-1],
            units=output_layer)
    else:
        logits = tf.layers.dense(
            inputs=x,
            units=output_layer)
    out = tf.nn.softmax(logits)

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(out, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return accuracy, loss, optimizer

graph1 = tf.Graph()
with graph1.as_default():
    x = tf.placeholder(tf.float32, [None, 2])
    y = tf.placeholder(tf.float32, [None, 2])

@_model.route('/train', methods=['GET', 'POST'])
def train():
    epochs = int(request.json['n_epochs'])
    print(epochs)
    total_loss = []
    acc = None

    with graph1.as_default():
        accuracy, loss, optimizer = model()

    with tf.Session(graph=graph1) as sess:
        sess.run(tf.global_variables_initializer())
        x_train, y_train, x_test, y_test = process_data()
        for epoch in range(epochs):
            sess.run(optimizer, {x: x_train, y: y_train})
            total_loss.append(float(sess.run(loss, {x: x_train, y: y_train})))
            print(sess.run(accuracy, {x: x_test, y: y_test}))
        acc = float(sess.run(accuracy, {x: x_test, y: y_test}))
    
    tf.reset_default_graph()
    print(total_loss[-1])
    return jsonify({'acc': "{0:.2f}".format(acc), 'loss': "{0:.2f}".format(total_loss[-1]), 'total_loss': total_loss})

