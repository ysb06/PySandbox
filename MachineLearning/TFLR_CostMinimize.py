import tensorflow as tf

X = [1, 2, 3]
Y = [1, 2, 3]

W = tf.placeholder(tf.float32)
hypothesis = X * W

cost = tf.reduce_mean(tf.square(hypothesis - Y))

sess = tf.Session()     # 세션을 열기
sess.run(tf.global_variables_initializer())     # 변수 초기화
