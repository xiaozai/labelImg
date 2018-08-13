import matplotlib.pyplot as plt
import numpy as np

x= np.loadtxt('x.out')
meanNew = np.loadtxt('meanNew.out')
varNew = np.loadtxt('varNew.out')
meanOld = np.loadtxt('meanOld.out')
varOld = np.loadtxt('varOld.out')

ms=1000
plt.title("Comparison execution time: selection best-fit (new) or first found")
ax = plt.subplot(2,1,1)
plt.errorbar(x, meanNew/ms, np.sqrt(varNew)/ms, linestyle='None', marker='^', label="New")
plt.errorbar(x, meanOld/ms, np.sqrt(varOld)/ms, linestyle='None', marker='^', label="Old")
ax.set_xlabel("amount of shapes added (randomly) to the image")
ax.set_ylabel("Time [ns] / hover event")

ax = plt.subplot(2,1,2)
ax.set_xlabel("amount of shapes added (randomly) to the image")
ax.set_ylabel("Factor by which the new impl is slower")
plt.errorbar(x, meanNew/meanOld, np.sqrt(varNew)/ms, linestyle='None', marker='^', label="New")

plt.legend()
plt.show()
plt.savefig("results.png")
