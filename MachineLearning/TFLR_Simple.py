import tensorflow as tf

sess = tf.Session()



x_train = [1, 2, 3]
y_train = [1, 2, 3]

# tf.random_normal은 랜덤 값, [1]은 Shape
weight = tf.Variable(tf.random_normal([1]), name='weight')
bias = tf.Variable(tf.random_normal([1]), name='bias')

hypo = x_train * weight + bias

# cost = 1/m ∑(W(x^i) - y^i)^2
cost = tf.reduce_mean(tf.square(hypo - y_train))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)

sess.run(tf.global_variables_initializer())

for step in range(2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(cost), sess.run(weight), sess.run(bias))