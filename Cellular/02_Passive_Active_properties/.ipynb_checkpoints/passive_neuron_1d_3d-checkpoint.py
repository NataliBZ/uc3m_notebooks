from neuron import h

class PassiveNeuron_1D_3D:
    def __init__(self):
        
        # SOMA
        # Create soma
        self.soma = h.Section(name="soma")
        self.soma.L = 20  # length (µm)
        self.soma.diam = 20  # diameter (µm)
        self.soma.Ra = 123.0  # axial resistivity (Ω*cm)
        self.soma.cm = 1  # capacitance (µF/cm^2)

        # Insert passive properties
        self.soma.insert("pas")
        for seg in self.soma:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential

        # AXON
        self.axon = h.Section(name="axon")

        # Axon section (blue in plot)
        self.axon.diam = 3
        self.axon.L = 100  # length (µm)
        self.axon.nseg = 5  # diameter (µm)
        self.axon.Ra = 123.0  # axial resistivity (Ω*cm)
        self.axon.cm = 1  # capacitance (µF/cm^2)

        # Topology
        self.axon.connect(self.soma(0))

        self.axon.insert("pas")
        for seg in self.axon:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential

        # DENDRITE
        self.dend = h.Section(name="dend")

        # Dendrite section (red in plot)
        self.dend.L = 200  # length (µm)
        self.dend.diam = 1  # diameter (µm)
        self.dend.nseg = 5  # number of segments
        self.dend.Ra = 300.0  # axial resistivity (Ω*cm)
        self.dend.cm = 1  # capacitance (µF/cm^2)

        # Topology
        self.dend.connect(self.soma(1))

        # Passive properties in dendrite and axon
        self.dend.insert("pas")
        for seg in self.dend:
            seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
            seg.pas.e = (
                -70
            )  # Leak reversal potential, it influences the steady state membrane potential


        # DENDRITIC BRANCHES
        self.branch_0 = h.Section(name="branch_0")
        self.branch_1 = h.Section(name="branch_1")
        self.branch_2 = h.Section(name="branch_2")
        self.branch_3 = h.Section(name="branch_3")

        branchlst = [self.branch_0, self.branch_1, self.branch_2, self.branch_3]

        # Branch geometry
        # Long and thick
        self.branch_0.L = 300
        self.branch_0.diam = 10
        # Short and thin
        self.branch_1.L = 100
        self.branch_1.diam = 8
        # Short and thick
        self.branch_2.L = 100
        self.branch_2.diam = 3
        # Long and thin
        self.branch_3.L = 200
        self.branch_3.diam = 1

        # Connect them
        self.branch_0.connect(self.dend(1))
        self.branch_1.connect(self.dend(1))
        self.branch_2.connect(self.dend(1))
        self.branch_3.connect(self.dend(1))

        # Passive properties in dendrite branches
        for branch in branchlst:
            branch.Ra = 130.0  # axial resistivity (Ω*cm)
            branch.cm = 1  # capacitance (µF/cm^2)
            branch.insert("pas")
            for seg in branch:
                seg.pas.g = 0.0003  # Conductance of the leak channels (in S/cm2)
                seg.pas.e = (
                    -70
                )  # Leak reversal potential, it influences the steady state membrane potential











