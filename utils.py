import csv
import numpy as np

def read_elisa_csv(filename):
    raw_data=[]
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            raw_data.append(row)

    name = raw_data[0][2]
    date = raw_data[2][2]
    experiment = [name, date]

    labels = []
    for i in range(4, 12):
        labels.append(raw_data[i][1:])

    data = []
    for i in range(15, 23):
        raw_line = raw_data[i][1:]
        numbers_line = []
        for num in raw_line:
            numbers_line.append(float(num.replace(",", ".")))
        data.append(numbers_line)

    std_concentrations = []
    for i in range(24, 29):
        raw_concentration = raw_data[i][1].split(' ')[2]
        concentration = float(raw_concentration.replace(",", "."))
        std_concentrations.append(concentration)

    return data, labels, std_concentrations, experiment

def get_average_by_label(label, data, labels):
    ocurrences = []
    for i in range(len(labels)):
        for j in range(len(labels[i])):
            if labels[i][j] == label:
                ocurrences.append(data[i][j])
    return np.mean(ocurrences)

def four_parameter(x, a, b, c, d):
    return d + (a - d) / (1 + (x/c)**b)

def get_concentration(y, a, b, c, d):
    return c*((a-d)/(y-d)-1)**(1/b)
