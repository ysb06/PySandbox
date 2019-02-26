import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1.5708, 3.1415, 0.0001)
y = 1 / 2 * np.cos(x / 2)

print("Min(90): " + str(1 / 2 * np.cos(1.5708 / 2)))
print("Max(180): " + str(1 / 2 * np.cos(3.1415 / 2)))

plt.plot(x, y)
plt.show()