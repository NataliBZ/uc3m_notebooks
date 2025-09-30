import csv
import matplotlib.pyplot as plt
from neuron import h
import instantiate_neuron as IN

# Defining a function for: cell instantiation and simulation and safe in file
def SquarePulses_stim(stim_ampl, morph_filename, output_filename, axs=None):
    import csv
    from neuron import h
    import instantiate_neuron as IN
    
    data = {}
    cell = IN.NEURON(morph_filename)
    
    # If no axes were passed, create them
    if axs is None:
        fig, axs = plt.subplots(2, 1, figsize=(13, 9))
    else:
        fig = axs[0].figure  # get figure from passed axes
    
    # Top plot: soma voltage
    axs[0].set_title('%s \n Soma voltage' % morph_filename )
    axs[0].set_xlabel('t (ms)')
    axs[0].set_ylabel('V (mV)')

    # Bottom plot: injected current
    axs[1].set_title('Current injection')
    axs[1].set_xlabel('t (ms)')
    axs[1].set_ylabel('I (nA)')

    # Loop over stim amplitudes
    for i, sa in enumerate(stim_ampl):
        stim = h.IClamp(cell.somatic[0](0.5))         
        stim.delay = 100
        stim.dur = 300
        stim.amp = sa    

        rec_t = h.Vector(); rec_t.record(h._ref_t)
        rec_v_soma = h.Vector(); rec_v_soma.record(cell.somatic[0](0.5)._ref_v)
        rec_i = h.Vector(); rec_i.record(stim._ref_i)

        h.load_file('stdrun.hoc')
        h.finitialize(-65)
        h.continuerun(500)
        
        data[f'time_{i}'] = list(rec_t)
        data[f'current_{i}'] = list(rec_i)
        data[f'voltage_{i}'] = list(rec_v_soma)
        
        axs[0].plot(rec_t, rec_v_soma, label=f"I={sa} nA")
        axs[1].plot(rec_t, rec_i, label=f"I={sa} nA")
    
    #axs[0].legend()
    #axs[1].legend()

    # Save to CSV
    with open(output_filename, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))

    return fig, axs