import matplotlib.pyplot as plt
import numpy as np

x= np.loadtxt('x.out', results_mean)
meanNew = np.loadtxt('meanNew.out', results_mean)
varNew = np.loadtxt('varNew.out', results_var)
meanOld = np.loadtxt('meanOld.out', results_mean)
varOld = np.loadtxt('varOld.out', results_var)

ms=1000
plt.title("Comparison execution time: selection best-fit (new) or first found")
plt.errorbar(x, meanNew/ms, np.sqrt(varNew)/ms, linestyle='None', marker='^', label="New")
plt.errorbar(x, meanOld/ms, np.sqrt(varOld)/ms, linestyle='None', marker='^', label="Old")
plt.xlabel("amount of shapes added (randomly) to the image")
plt.ylabel("Time [ns] / hover event")

plt.show()
plt.legend()
plt.savefig("results.png")
