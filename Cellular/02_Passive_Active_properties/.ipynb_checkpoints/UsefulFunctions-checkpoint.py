# Defining some usefull functions.
from neuron import h
import matplotlib.pyplot as plt
import neurom as nm
from neurom import view
from hoc2swc import neuron2swc

import ipywidgets as widgets
from IPython.display import display, clear_output

# Global containers for objects
simulations_records = []  # stimulations
voltage_records = []  # voltage recordings
current_records = []  # current recordings


def reset():
    """Convenience functions for setting up stimulation, recording and simulation"""
    del simulations_records[:]
    del voltage_records[:]
    del current_records[:]


def iclamp(location, delay=100, amplitude=0.1, duration=500):
    """"Inject a current step with parameters at location"""
    stim = h.IClamp(location)  # Place a stimulation electrode at location
    stim.delay = delay  # stim delay (ms)
    stim.amp = amplitude  # stim amplitude (pA)
    stim.dur = duration  # stim duration (ms)
    simulations_records.append({"stim": stim, "loc": str(location)})


def record_voltage(location):
    """Setup recording of voltage at location"""
    vec = h.Vector()
    vec.record(location._ref_v)  # record voltage at location
    voltage_records.append({"vec": vec, "loc": str(location)})


def record_current(stimulation_dict):
    """Setup recording of stimulation current"""
    vec = h.Vector()
    vec.record(stimulation_dict["stim"]._ref_i)  # record stimulation current
    current_records.append({"vec": vec, "loc": stimulation_dict["loc"]})


def init_run(v_i, t_stop):
    """Initialize and run a simulation"""
    # Record time
    rec_t = h.Vector()
    rec_t.record(h._ref_t)
    # Record current for all stimuli
    for stimulation_dict in simulations_records:
        record_current(stimulation_dict)
    # Setup simulation and run
    h.load_file("stdrun.hoc")
    h.finitialize(v_i)  # initial voltage
    h.continuerun(t_stop)  # final time
    return rec_t


def tvi_plots(t, voltage_records=[], current_records=[], vmax=40, imax=0.5):
    """Plot current and voltage for all stims and recordings"""
    plt.figure()
    plt.title("currents")
    plt.ylim((-0.01, imax))
    plt.xlabel("t (ms)")
    plt.ylabel("I (pA)")
    for idict in current_records:
        plt.plot(t, idict["vec"], label=idict["loc"])
    plt.legend(loc=1)

    plt.figure()
    plt.title("voltages")
    plt.ylim((-71, vmax))
    plt.ylabel("V (mV)")
    plt.xlabel("t (ms)")
    for vdict in voltage_records:
        plt.plot(t, vdict["vec"], label=vdict["loc"])
    plt.legend(loc=1)


def plot_morphology(fname="cell_01"):
    fname = "{}.swc".format(fname)
    h.define_shape()
    h.topology()
    neuron2swc(fname, 0) #swap_yz=False)
    neuron1 = nm.load_morphology(fname)
    view.plot_morph(neuron1)

def chage_passive_prop(cell):
    reset()
    # Fix description width using layout
    style = {'description_width': '150px'} # Adjust as needed

    # Create three input boxes
    var1_box = widgets.FloatText(description='Diamater (µm):', value=1.0, style=style)
    var2_box = widgets.FloatText(description='Axial resistivity (Ω*cm):', value=300.0, style=style)
    var3_box = widgets.FloatText(description='Capacitance (µF/cm^2):', value=1.0, style=style)

    # Create a button
    save_button = widgets.Button(description='Change Values')

    # Function to save values when button is clicked
    def click_button(b):
        reset()
        cell.dend.diam = var1_box.value
        cell.dend.Ra = var2_box.value
        cell.dend.cm = var3_box.value
        print("Values changed!")

    save_button.on_click(click_button)

    # Display input boxes and button
    display(var1_box, var2_box, var3_box, save_button)