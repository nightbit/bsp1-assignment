import numpy as np
from numpy import sin, cos, pi, linspace
import matplotlib.pyplot as plt

## Visualization
# Create a sine wave and plot it
t = linspace(0, 2*pi, 200)
print(t)
x = sin(t)
plt.plot(t, x)

# Add title and axis labels to the figure
plt.xlabel('t = 0...2*pi')
plt.ylabel('Sine of t')
plt.title('Basic Sine Plot')
plt.show()

# Create another figure, plot two functions
plt.plot(t, sin(t), 'b')
plt.plot(t, sin(t+0.5), 'r--')
plt.show()

# Create figure with subplots and save it
plt.subplot(2, 1, 1)
plt.plot(t, sin(t))
plt.subplot(2, 1, 2)
plt.plot(t, cos(t))
plt.savefig('../testPlot.png')
plt.show()
