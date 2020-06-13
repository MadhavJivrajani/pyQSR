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
python3 test/tests.py
```  
  
### Example
To creare a quantum shift register with 4 data qubits which is circular in nature:  

```py
from pyQSR.quantum_left_shift import QuantumLeftShift

qsrCirc = QuantumLeftShift(4, "1011", circular=True) #create the shift register.

#perform two circular left shift operations.
qsrCirc.shift()
qsrCirc.shift()  

#get the state of the register
state = qsrCirc.get_register_state()

print(state) # {'1110': 8}

#to print the current circuit of the shift register and get extra info about its state.
print(qsrCirc)
"""
     ┌───┐ ░ ┌──────────────────────┐┌──────────────────────┐ ░ ┌─┐          ░ 
q_0: ┤ X ├─░─┤0                     ├┤0                     ├─░─┤M├──────────░─
     ├───┤ ░ │                      ││                      │ ░ └╥┘┌─┐       ░ 
q_1: ┤ X ├─░─┤1                     ├┤1                     ├─░──╫─┤M├───────░─
     └───┘ ░ │                      ││                      │ ░  ║ └╥┘┌─┐    ░ 
q_2: ──────░─┤2                     ├┤2                     ├─░──╫──╫─┤M├────░─
     ┌───┐ ░ │                      ││                      │ ░  ║  ║ └╥┘┌─┐ ░ 
q_3: ┤ X ├─░─┤3                     ├┤3                     ├─░──╫──╫──╫─┤M├─░─
     └───┘ ░ │                      ││                      │ ░  ║  ║  ║ └╥┘ ░ 
q_4: ──────░─┤4 Circular Left Shift ├┤4 Circular Left Shift ├─░──╫──╫──╫──╫──░─
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ 
q_5: ──────░─┤5                     ├┤5                     ├─░──╫──╫──╫──╫──░─
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ 
q_6: ──────░─┤6                     ├┤6                     ├─░──╫──╫──╫──╫──░─
           ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ 
q_7: ──────░─┤7                     ├┤7                     ├─░──╫──╫──╫──╫──░─
     ┌───┐ ░ │                      ││                      │ ░  ║  ║  ║  ║  ░ 
q_8: ┤ X ├─░─┤8                     ├┤8                     ├─░──╫──╫──╫──╫──░─
     └───┘ ░ └──────────────────────┘└──────────────────────┘ ░  ║  ║  ║  ║  ░ 
c_0: ════════════════════════════════════════════════════════════╩══╬══╬══╬════
                                                                    ║  ║  ║    
c_1: ═══════════════════════════════════════════════════════════════╩══╬══╬════
                                                                       ║  ║    
c_2: ══════════════════════════════════════════════════════════════════╩══╬════
                                                                          ║    
c_3: ═════════════════════════════════════════════════════════════════════╩════
                                                                               
Data qubits: 4
Initial seed: 1011
Shifts performed: 2
Circular: True
"""
```

### References  
[1] Jae-weon Lee and Eok Kyun Lee and Jaewan Kim and Soonchil Lee, Quantum Shift Register, 2001.
    https://arxiv.org/abs/quant-ph/0112107
