import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py
import csv
import glob
import ipywidgets as widgets
from IPython.display import display
import efel
from json2html import json2html
import IPython


def get_data(fn):
    """Read  data file and format for plotting"""
    d = np.fromfile(fn)    
    return d[::2], d[1::2]

def extract_PSP_window(trace, time, stimulation_index, time_before=50, time_after=300):
    """Extract a time window with a single EPSP trace"""
    psp_trace = trace[stimulation_index - time_before : stimulation_index + time_after]
    psp_time = time[stimulation_index - time_before : stimulation_index + time_after]

    return psp_trace, psp_time


def extract_EPSP_features(psp_trace, psp_time, stimulation_time):
    """
    Function takes in a EPSP curve and calculates the following features: amplitude;
    5%, 20% and 80% of the amplitude, tau rise and latency. Based on defintions from
    Feldmeyer et al., 1999.

    Parameters
    ----------
    psp_trace : array with voltage trace [mV]
    psp_time : array of psp times [s]
    stimulation_time : time of the stimulation [s]

    Returns
    -------
    psp_percent : dictionary with psp amplitudes at 5%, 20% and 80% of the amplitude
    times : dictionary with psp times at 5%, 20% and 80% of the amplitude
    amplitude : mplitude of the first EPSP computed as the difference between the 20 and the 80 % of rise
    tau_rise : distance between the time of 20% and 80% of the rise of the EPSP [s]
    latency : time between the AP of the presynaptic cell and 5% amplitude rise of the EPSP [s]
    """

    # find absolute values of the psp trace
    max_psp = np.max(psp_trace)
    min_psp = np.min(psp_trace)
    amplitude_psp = np.abs(max_psp - min_psp)

    # compute percentages of amplitudes
    twenty_amplitude = amplitude_psp * 80.0 / 100.0
    eighty_amplitude = amplitude_psp * 20.0 / 100.0
    five_amplitude = amplitude_psp * 95.0 / 100.0
    amplitude = eighty_amplitude - twenty_amplitude

    # compute amplitude percentages on the psp trace
    psp_percent = {
        "five": -(five_amplitude - max_psp),
        "twenty": -(twenty_amplitude - max_psp),
        "eighty": -(eighty_amplitude - max_psp),
    }

    # find corresponding index of an array
    five_index = np.where(psp_trace >= psp_percent["five"])[0][0]
    twenty_index = np.where(psp_trace >= psp_percent["twenty"])[0][0]
    eighty_index = np.where(psp_trace >= psp_percent["eighty"])[0][0]

    # extract time points for percentage points of the trace
    psp_times = {
        "five": psp_time[five_index],
        "twenty": psp_time[twenty_index],
        "eighty": psp_time[eighty_index],
    }
    
    # calculate time features of a PSP
    tau_rise = np.abs((psp_times["twenty"] - psp_times["eighty"]))
    latency = np.abs((psp_times["five"]) - stimulation_time)

    return psp_percent, psp_times, amplitude, tau_rise, latency

def load_traces(filename):
    data = h5py.File(filename, "r")
    data.keys()

    traces = []
    for key in data.keys():
        traces.append(data.get(key))

    return np.array(traces)

def extract_tau_latency(psp_trace, psp_time, stimulation_time):
    """
    Function takes in a EPSP curve and calculates the following features: amplitude;
    5%, 20% and 80% of the amplitude, tau rise and latency. Based on defintions from
    Feldmeyer et al., 1999.

    Parameters
    ----------
    psp_trace : array with voltage trace [mV]
    psp_time : array of psp times [s]
    stimulation_time : time of the stimulation [s]

    Returns
    -------
    tau_rise : distance between the time of 20% and 80% of the rise of the EPSP [s]
    latency : time between the AP of the presynaptic cell and 5% amplitude rise of the EPSP [s]
    """

    # find absolute values of the psp trace
    max_psp = np.max(psp_trace)
    min_psp = np.min(psp_trace)
    amplitude_psp = np.abs(max_psp - min_psp)

    # compute percentages of amplitudes
    twenty_amplitude = amplitude_psp * 80.0 / 100.0
    eighty_amplitude = amplitude_psp * 20.0 / 100.0
    five_amplitude = amplitude_psp * 95.0 / 100.0
    amplitude = eighty_amplitude - twenty_amplitude

    # compute amplitude percentages on the psp trace
    psp_percent = {
        "five": -(five_amplitude - max_psp),
        "twenty": -(twenty_amplitude - max_psp),
        "eighty": -(eighty_amplitude - max_psp),
    }

    # find corresponding index of an array
    five_index = np.where(psp_trace >= psp_percent["five"])[0][0]
    twenty_index = np.where(psp_trace >= psp_percent["twenty"])[0][0]
    eighty_index = np.where(psp_trace >= psp_percent["eighty"])[0][0]

    # extract time points for percentage points of the trace
    psp_times = {
        "five": psp_time[five_index],
        "twenty": psp_time[twenty_index],
        "eighty": psp_time[eighty_index],
    }

    # calculate time features of a PSP
    tau_rise = np.abs((psp_times["twenty"] - psp_times["eighty"]))
    latency = np.abs((psp_times["five"]) - stimulation_time)

    return amplitude_psp*1000, tau_rise, latency

def extract_all_amps_taus_latencies(trace, stimulation_indices, time):
    taus = np.array([])
    latencies = np.array([])
    amplitudes = np.array([])


    for index in stimulation_indices:
        psp_trace, psp_time = extract_PSP_window(trace, time, index)
        amp, tau_rise, latency = extract_tau_latency(psp_trace, psp_time, time[index])

        taus = np.append(taus, tau_rise)
        latencies = np.append(latencies, latency)
        amplitudes = np.append(amplitudes, amp)


    return amplitudes, taus, latencies

def compute_noise(trace, stimulation_index, time_before=50):
    pre_psp_trace = trace[0 : stimulation_index - time_before]
    noise_max = np.max(trace)
    noise_min = np.min(trace)
    noise_amp = np.abs(noise_max - noise_min)
    return noise_amp * 1000

def calculate_failure_rate(amplitudes, latencies, noise_std):
    failure = 0
    total = 0

    latency_average = np.mean(latencies.mean(axis=0))
    failed_amps, correct_amps = [], []
    for amps, lats in zip(amplitudes, latencies):
        for amp, lat in zip(amps, lats):
            if amp < 1.5 * noise_std or lat > 2.5 * np.mean(latency_average):
                failure += 1
                failed_amps.append(amp)
            else:
                correct_amps.append(amp)
            total += 1

    return failure, total, failed_amps, correct_amps


resp_list_global = []
def choose_protocol():
    """
    Shows a dropdown with experiment names and plots the corresponding
    response and stimulation traces once selected.
    Works reliably inside Jupyter / JupyterLab.
    """
    global resp_list_global 
    
    exp_list = ['exp_FirePattern', 'exp_IV']

    dropdown = widgets.Dropdown(
        options=exp_list,
        description='Select:',
        style={'description_width': 'initial'}
    )

    output = widgets.Output()

    def plot_experiment(exp_name):
        global resp_list_global
        output.clear_output(wait=True)
        with output:
            resp_path = f'{exp_name}_ch6_*.dat'
            stim_path = f'{exp_name}_ch7_*.dat'

            resp_list = sorted(glob.glob(resp_path))
            stim_list = sorted(glob.glob(stim_path))

            # store globally so other functions can use it
            resp_list_global = resp_list 

            if not resp_list and not stim_list:
                print(f"No files found for {exp_name}")
                return

            # Response
            fig1, ax1 = plt.subplots(figsize=(15, 3))
            ax1.set_title(f'{exp_name} — Response')
            for fv in resp_list:
                t, v = get_data(fv)
                ax1.plot(t, v)
            plt.show()

            # Stimulation
            fig2, ax2 = plt.subplots(figsize=(15, 3))
            ax2.set_title(f'{exp_name} — Stimulation')
            for fv in stim_list:
                t, v = get_data(fv)
                ax2.plot(t, v)
            plt.show()

    # Create interactive connection
    widgets.interactive_output(plot_experiment, {'exp_name': dropdown})

    # Layout UI
    ui = widgets.VBox([dropdown, output])
    display(ui)

def choose_answer():
    global resp_list_global

    exp_list = ['Sub-threshold', 'Supra-threshold'] 

    dropdown = widgets.Dropdown(
        options=exp_list,  # <- keyword argument!
        description='Select:', # optional, adds a label
        style={'description_width': 'initial'}
    )
    
    output = widgets.Output()

    def run_analysis(answer):
        output.clear_output(wait=True)
        with output:
            if answer == "Supra-threshold":
                for fv in resp_list_global:
                    t, v = get_data(fv)
                    #t, i = get_data(file_c1)

                    stim_start = 378.9 # in ms
                    stim_end = 3681.0
                    trace = {'T': t, 'V': v, 'stim_start': [stim_start], 'stim_end': [stim_end]}
   
                    #Find the mean firing freq., after hyperpol depth and spikecount 
                    feature_values = efel.get_feature_values([trace], ['mean_frequency', 'AHP_depth', 'Spikecount'])[0]
                    print(feature_values)
                    feature_values = {feature_name: list(values) for feature_name, values in feature_values.items()}
                    IPython.display.HTML(json2html.convert(json=feature_values))

            if answer == "Sub-threshold": 
                for fv in resp_list_global:
                    t, v = get_data(fv)

                    stim_start = 378.9 # in ms
                    stim_end = 3681.0
                    trace = {'T': t, 'V': v, 'stim_start': [stim_start], 'stim_end': [stim_end]}

                    feature_values = efel.get_feature_values([trace], ['voltage_base'])[0]
                    print(feature_values)
                    feature_values = {feature_name: list(values) for feature_name, values in feature_values.items()}
                    IPython.display.HTML(json2html.convert(json=feature_values))

        # Create interactive connection
    widgets.interactive_output(run_analysis, {'answer': dropdown})

    # Layout UI
    ui = widgets.VBox([dropdown, output])
    display(ui)


#mean_trace_global = None   # <-- will store the output of the function

def choose_connection():
    """
    Shows a dropdown with connection h5 file names and plots the corresponding
    experimental traces. Returns a dictionary that will hold the mean trace.
    """

    exp_list = ['connection_c1', 'connection_c2', 'connection_c4']

    # A safe container to store the mean trace after selection
    result = {"mean_trace": None}

    dropdown = widgets.Dropdown(
        options=exp_list,
        description='Select:',
        style={'description_width': 'initial'}
    )

    output = widgets.Output()

    def plot_traces(exp_name):
        """Plots all sweeps and stores the mean trace."""
        with output:
            output.clear_output()

            # Read the H5 file
            with h5py.File(f'{exp_name}.h5', "r") as data:
                traces = np.array([data[key][()] for key in data.keys()])

            # Compute mean trace
            mean_trace = np.mean(traces, axis=0)
            result["mean_trace"] = mean_trace  # store it safely

            # Plot sweeps and mean
            plt.figure(figsize=(8, 4))
            for trace in traces:
                plt.plot(trace, "b--", alpha=0.4)

            plt.plot(mean_trace, "r", linewidth=2, label='mean')
            plt.ylabel('V (V)')
            plt.xlabel('time (ms)')
            plt.title(f"{exp_name}")
            plt.legend()
            plt.show()

            print("Mean trace stored in result['mean_trace']")

    # Link dropdown to plot
    widgets.interactive_output(plot_traces, {'exp_name': dropdown})

    display(dropdown, output)

    # Return the dictionary that will hold the mean trace
    return result



def compute_failure_rate(files):
    traces_collection = {}
    for n, file in enumerate(files):
        traces_collection[n] = load_traces(file)

    time = np.arange(0, 1.3, 0.0001)
    stimulation_indices = np.array([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 10000])

    taus_collection = {}
    latencies_collection = {}
    amplitudes_collection = {}

    for key in traces_collection:
        traces = traces_collection[key]
        all_amplitudes, all_taus, all_latencies = extract_all_amps_taus_latencies(
            traces[0], stimulation_indices, time
        )

        for trace in traces[1:]:
            amps, taus, latencies = extract_all_amps_taus_latencies(trace, stimulation_indices, time)
            all_taus = np.vstack([all_taus, taus])
            all_latencies = np.vstack([all_latencies, latencies])
            all_amplitudes = np.vstack([all_amplitudes, amps])

        taus_collection[key] = all_taus
        latencies_collection[key] = all_latencies
        amplitudes_collection[key] = all_amplitudes 

    noise_collection = {}
    for key in traces_collection:
        noise = []
        for psp_trace in traces:
            noise.append(compute_noise(psp_trace, stimulation_indices[0]))

        noise_collection[key] = np.array(noise)

    noise_std = pd.DataFrame(noise_collection).std()

    fails0, total, failed_amps0, correct_amps0 = calculate_failure_rate(
    amplitudes_collection[0], latencies_collection[0], noise_std.iloc[0]
    )

    fails1, _, failed_amps1, correct_amps1 = calculate_failure_rate(
    amplitudes_collection[1], latencies_collection[1], noise_std.iloc[1]
    )

    fails2, _, failed_amps2, correct_amps2 = calculate_failure_rate(
    amplitudes_collection[2], latencies_collection[2], noise_std.iloc[2]
    )
    conn0 = [fails0, total, failed_amps0, correct_amps0]
    conn1 = [fails1, _, failed_amps1, correct_amps1]
    conn2 = [fails2, _, failed_amps2, correct_amps2]
    return conn0, conn1, conn2
