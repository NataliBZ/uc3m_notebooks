from neuron import h

class PassiveNeuron_1Dend:
    def __init__(self):
        # Define all the sections first: soma, dendrite and axon
        self.soma = h.Section(name="soma")
        self.dend = h.Section(name="dend")
        self.axon = h.Section(name="axon")

        # Passive properties: cell geometry
        # Soma section (black in plot)
        self.soma.L = 20  # length (µm)
        self.soma.diam = 20  # diameter (µm)
        self.soma.Ra = 123.0  # axial resistivity (Ω*cm)
        self.soma.cm = 1  # capacitance (µF/cm^2)

        # Dendrite section (red in plot)
        self.dend.L = 200  # length (µm)
        self.dend.diam = 1  # diameter (µm)
        self.dend.nseg = 5  # number of segments
        self.dend.Ra = 300.0  # axial resistivity (Ω*cm)
        self.dend.cm = 1  # capacitance (µF/cm^2)

        # Axon section (blue in plot)
        self.axon.diam = 3
        self.axon.L = 100  # length (µm)
        self.axon.nseg = 5  # diameter (µm)
        self.axon.Ra = 123.0  # axial resistivity (Ω*cm)
        self.axon.cm = 1  # capacitance (µF/cm^2)

        # Topology or how sections are connected
        self.dend.connect(self.soma(1))
        self.axon.connect(self.soma(0))
        
        # Passive properties: conductance and reversal potential of leak channels
        self.soma.insert("pas")
        for seg in self.soma:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential

        self.dend.insert("pas")
        for seg in self.dend:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential

        self.axon.insert("pas")
        for seg in self.axon:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential