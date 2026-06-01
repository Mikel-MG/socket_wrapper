#!/usr/bin/env bash

source ./setup.sh
mkdssp ./data/sample_PDBs/2ZTA.pdb --output-format dssp > temp.dssp
./data/SOCKET/socket2_linux -f ./data/sample_PDBs/2ZTA.pdb -s ./temp.dssp -c 7.0 > socket.output
