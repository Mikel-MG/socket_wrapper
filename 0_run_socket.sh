#!/usr/bin/env bash

source ./setup.sh

PDB="./data/sample_PDBs/2ZTA.pdb"

mkdssp $PDB --output-format dssp > temp.dssp
# cat temp.dssp | cut -c1-136 > temp.dssp

./data/SOCKET/socket2_linux -f $PDB -s ./temp.dssp -c 7.0 > socket.output
