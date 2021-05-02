from utils import read_elisa_csv, get_average_by_label, four_parameter, get_concentration
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data, labels, std_concentrations, experiment = read_elisa_csv('elisa_gmpc.csv')

nsb_avg = get_average_by_label('NSB', data, labels)
b0_avg = get_average_by_label('Bo', data, labels)
corrected_b0 = b0_avg - nsb_avg

std_sample_labels = ['S1', 'S3', 'S5', 'S7', 'S8']

b_b0 = []
for label in std_sample_labels:
    sample_avg = get_average_by_label(label, data, labels)
    b_b0.append((sample_avg - nsb_avg)/corrected_b0*100)

popt, pcov = curve_fit(four_parameter, std_concentrations, b_b0)
a, b, c, d = popt

sample_labels = []
for i in range(len(labels)):
    for j in range(len(labels[i])):
        label = labels[i][j]
        if label.startswith('Am') and label not in sample_labels:
            sample_labels.append(label)

sample_values = []
concentrations = []
concentration_label = []
for label in sample_labels:
    sample_value = get_average_by_label(label, data, labels)
    sample_value = (sample_value - nsb_avg)/corrected_b0*100
    concentration = get_concentration(sample_value, a, b, c, d)
    sample_values.append(sample_value)
    concentrations.append(concentration)
    concentration_label.append(label)

sample_values = np.array(sample_values)

#concentrations = get_concentration(sample_values, a, b, c, d)

points_x = np.linspace(std_concentrations[0], std_concentrations[-1], 500)
points_y = four_parameter(points_x, a, b, c, d)

ax = plt.subplot()
ax.plot(points_x, points_y, color='black', label="fit")
ax.scatter(std_concentrations, b_b0, label="padrão")
ax.scatter(concentrations, sample_values, label="amostras")
ax.set_yscale('linear')
ax.set_xscale('log')
ax.set_ylabel('%B/B0')
ax.set_xlabel('GMPc (pmol/ml)')
ax.set_title(experiment[0])
ax.grid(True)
ax.legend()
plt.show()
