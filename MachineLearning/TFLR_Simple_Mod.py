import tensorflow as tf
import csv

# 단순 선형 회귀를 응용한 다항식 회귀
# 실패 : cost 값이 무한으로 가는 것 같음. 문제 해결이 필요

sess = tf.Session()

raw = open('Data/RealEstateData/Raw.csv', 'r')
data = csv.reader(raw)

x_train = []
x2_train = []
x3_train = []
y_train = []

for line in data:
    x_train.append(float(line[1]))
    x2_train.append(pow(float(line[1]), 2))
    x3_train.append(pow(float(line[1]), 3))
    y_train.append(float(line[3]))

print(x_train)
print(x2_train)
print(x3_train)
print(y_train)

# tf.random_normal은 랜덤 값, [1]은 Shape
weight1 = tf.Variable(tf.random_normal([1],mean=2000000), name='weight1')
weight2 = tf.Variable(tf.random_normal([1],mean=155.28), name='weight2')
weight3 = tf.Variable(tf.random_normal([1],mean=0.0038), name='weight3')
bias = tf.Variable(tf.random_normal([1],mean=0.00000008), name='bias')

hypo = x3_train * weight3 + x2_train * weight2 + x_train * weight1 + bias

# cost = 1/m ∑(W(x^i) - y^i)^2
cost = tf.reduce_mean(tf.square(hypo - y_train))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)

sess.run(tf.global_variables_initializer())

for step in range(2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(cost), sess.run(weight3), sess.run(weight2), sess.run(weight1), sess.run(bias))

