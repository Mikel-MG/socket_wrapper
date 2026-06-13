"""
renumber_pdb.py
---------------
Loads a PDB file with BioPython, renames every chain in alphabetical order
(A, B, C, ...) and reindexes every residue from 1..N within each chain.
Writes a clean PDB to the output path.

Usage:
    python renumber_pdb.py input.pdb output.pdb
"""

import string
import sys
from pathlib import Path

from Bio import PDB


def renumber_pdb(input_path: Path, output_path: Path, debug: bool) -> None:
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("structure", input_path)

    available_chain_ids = list(string.ascii_uppercase)  # A-Z (26 chains max)

    model = structure[0]  # Work on the first MODEL
    chains = list(model.get_chains())

    if len(chains) > len(available_chain_ids):
        raise ValueError(
            f"Structure has {len(chains)} chains but only A-Z (26) are available."
        )

    for new_chain_id, chain in zip(available_chain_ids, chains):
        old_chain_id = chain.id

        if debug:
            print(f"  Chain {old_chain_id!r} → {new_chain_id!r}")

        # Rename chain
        chain.id = new_chain_id

        # Reindex residues: keep only ATOM/HETATM residues, skip waters optionally
        residues = [r for r in chain.get_residues() if r.id[0] in (" ", "H_")]
        for new_res_seq, residue in enumerate(residues, start=1):
            old_id = residue.id
            # id tuple: (hetfield, seq, icode)
            residue.id = (old_id[0], new_res_seq, " ")

        if debug:
            print(f"    {len(residues)} residues reindexed 1–{len(residues)}")

    # Write the modified structure
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(str(output_path))

    if debug:
        print(f"\nSaved renumbered PDB → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python renumber_pdb.py <input.pdb> <output.pdb>")
        sys.exit(1)

    in_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    print(f"Loading {in_path} ...")
    renumber_pdb(in_path, out_path, debug=True)
