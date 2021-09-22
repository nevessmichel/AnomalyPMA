# AnomalyPMA

Authentication Methods and Network Security school work, Anomaly Detection System

# Install Scapy

There is some problems in the production version, which were corrected in development version, so here are the steps to install it:

- clone git repository: git clone https://github.com/secdev/scapy.git

- enter the folder: cd scapy

- install: python setup.py install

---

# Entries

It's possible to pass two params to pragram, confidance and output file, in this order.

- param 1 - confidence (float), range [0 ; 0.99]

- param 2 - output file (string), don't recommend blank space character

---

# Video Test Case

- confidence: 0.1

- default output file (empty): PMA_result.txt

---

# Dataset

The dataset used is from MIT, 1999: https://archive.ll.mit.edu/ideval/data/1999/training/week4/index.html

The file was saved at path {project_folder}/Data/weak4/monday.tcpdump
