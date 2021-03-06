# Quantum Shift Registers  

This is an IBM Qiskit implementation of quantum shift registers. Currently, a left shift register and circular left shift register is implemented.  
  
### Installation and setup  
  
- Clone the repository
```sh
git clone https://github.com/MadhavJivrajani/pyQSR.git
```  

- The following python modules are required:
  - qiskit
  - ddt (for tests)

  Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to install the required dependencies. 
  
### Running tests  
You can run the tests as follows:
```sh
python3 -m unittest discover -s test -p 'tests.py'
```  
### Tutorial
A comprehensive tutorial explaining stuff can be found [here](https://github.com/QForestCommunity/launchpad/tree/master/tutorials) :smile:
### Example
To creare a quantum shift register with 4 data qubits which is circular in nature:  

```py
from pyQSR.quantum_left_shift import *

qsrCirc = QuantumLeftShift(4, "1011", circular=True) #create the shift register.

#perform two circular left shift operations.
qsrCirc.shift()
qsrCirc.shift()  

#get the state of the register
state = qsrCirc.get_register_state()

print(state) # {'1110': 8}

#perform an additional shift.
qsrCirc.shift()

#to print the current circuit of the shift register and get extra info about its state.
print(qsrCirc)
"""
     ┌───┐ ░ ┌──────────────────────┐┌──────────────────────┐ ░ ┌─┐          ░ ┌──────────────────────┐
q_0: ┤ X ├─░─┤0                     ├┤0                     ├─░─┤M├──────────░─┤0                     ├
     ├───┤ ░ │                      ││                      │ ░ └╥┘┌─┐       ░ │                      │
q_1: ┤ X ├─░─┤1                     ├┤1                     ├─░──╫─┤M├───────░─┤1                     ├
     └───┘ ░ │                      ││                      │ ░  ║ └╥┘┌─┐    ░ │                      │
q_2: ──────░─┤2                     ├┤2                     ├─░──╫──╫─┤M├────░─┤2                     ├
     ┌───┐ ░ │                      ││                      │ ░  ║  ║ └╥┘┌─┐ ░ │                      │
q_3: ┤ X ├─░─┤3                     ├┤3                     ├─░──╫──╫──╫─┤M├─░─┤3                     ├
     └───┘ ░ │                      ││                      │ ░  ║  ║  ║ └╥┘ ░ │                      │
q_4: ──────░─┤4 Circular Left Shift ├┤4 Circular Left Shift ├─░──╫──╫──╫──╫──░─┤4 Circular Left Shift ├
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ │                      │
q_5: ──────░─┤5                     ├┤5                     ├─░──╫──╫──╫──╫──░─┤5                     ├
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ │                      │
q_6: ──────░─┤6                     ├┤6                     ├─░──╫──╫──╫──╫──░─┤6                     ├
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ │                      │
q_7: ──────░─┤7                     ├┤7                     ├─░──╫──╫──╫──╫──░─┤7                     ├
     ┌───┐ ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ │                      │
q_8: ┤ X ├─░─┤8                     ├┤8                     ├─░──╫──╫──╫──╫──░─┤8                     ├
     └───┘ ░ └──────────────────────┘└──────────────────────┘ ░  ║  ║  ║  ║  ░ └──────────────────────┘
c_0: ════════════════════════════════════════════════════════════╩══╬══╬══╬════════════════════════════
                                                                    ║  ║  ║                            
c_1: ═══════════════════════════════════════════════════════════════╩══╬══╬════════════════════════════
                                                                       ║  ║                            
c_2: ══════════════════════════════════════════════════════════════════╩══╬════════════════════════════
                                                                          ║                            
c_3: ═════════════════════════════════════════════════════════════════════╩════════════════════════════
                                                                                                       
Data qubits: 4
Initial seed: 1011
Shifts performed: 3
Circular: True
"""

#to see what the 'Circular Left Shift' gate looks like
circLeftShift = qsrCirc.construct_shift_gate()

#4 is the number of data qubits, an additional 4 ancillary ones required and one extra control.
qc = QuantumCircuit(4 + 4 + 1) 
qc.append(circLeftShift, range(4 + 4 + 1))

print(qc.decompose())
"""
                               ┌───┐     
q_0: ───────────────────X───■──┤ X ├──■──
                        │   │  └─┬─┘  │  
q_1: ────────────────X──X───┼────┼────┼──
                     │      │    │    │  
q_2: ─────────────X──X──────┼────┼────┼──
                  │         │    │    │  
q_3: ──────────X──X─────────┼────┼────┼──
               │          ┌─┴─┐  │  ┌─┴─┐
q_4: ───────X──X──────────┤ X ├──■──┤ X ├
            │             └───┘  │  └───┘
q_5: ────X──X────────────────────┼───────
         │                       │       
q_6: ─X──X───────────────────────┼───────
      │                          │       
q_7: ─X──────────────────────────┼───────
                                 │       
q_8: ────────────────────────────■───────

"""
```

### References  
[1] Jae-weon Lee and Eok Kyun Lee and Jaewan Kim and Soonchil Lee, Quantum Shift Register, 2001.
    https://arxiv.org/abs/quant-ph/0112107
