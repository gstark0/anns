# Awesome Neural Network Simulator v0.01 (ANNS) [Work In Progress]

<h4>Overview</h4>

ANNS is an artificial neural network simulator/generator based on Python-Flask and Google's TensorFlow. You can create deep learning models by adjusting available parameters(number of neurons, hidden layers, activation functions, learning rate etc), train them, and immediately see the accuracy and loss. Currently the model, ran out of the box, can be trained and tested on pregenerated dataset (dataset_generator.py), but in the future, running your own data will be possible. ANNS is made to be easy and user-friendly.

<h4>Getting Started</h4>

In order to run ANNS, you will need the following dependencies:
- Flask==0.12.2
- tensorflow==1.0.1

You can download them by running this command while being in ANNS directory:

    pip install -r requirements.txt

Then, to run the server:

    python server.py

That's it! ANNS should now be running on your machine, just open http://127.0.0.1:5000/ in your browser to start working with it.
