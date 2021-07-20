##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import matplotlib.pyplot as plt

def plot_results(job):
    result = job.result()
    count = int(job._azure_job.details.metadata['qubits'])
    histogram = result.results['histogram']

    data = []
    for i in range(1 << count):
        value = histogram[str(i)] if str(i) in histogram else 0
        data.append(value)

    axes = plt.gca()
    axes.set_ylim([0,1])

    plt.bar(range(1 << count), data)
    plt.show()
