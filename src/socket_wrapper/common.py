import subprocess
import tempfile
from pathlib import Path

from .renumber import renumber_pdb

# specify location of library and temporary files
tmp_dir = Path(tempfile.gettempdir())


def fix_pdb(
    pdb_file: Path,
    i_worker: str = "0",
    debug: bool = False,
) -> Path:
    # delete HETATM records
    path_fixed_output = tmp_dir / f"temp_fixed_{i_worker}.pdb"
    subprocess.run(f"grep -v 'HETATM' {pdb_file}> {path_fixed_output}", shell=True)

    # renumber chains and residue indices
    renumber_pdb(
        path_fixed_output,
        path_fixed_output,
        debug=debug,
    )

    return path_fixed_output


def run_dssp(
    pdb_file: Path,
    i_worker: str = "0",
    bin_dssp: str = "mkdssp",
    env: None | dict = None,
) -> Path:
    # run DSSP
    path_dssp_output = tmp_dir / f"temp_{i_worker}.dssp"
    dssp_command = f"{bin_dssp} {pdb_file} --output-format dssp > {path_dssp_output}"
    subprocess.call(dssp_command, shell=True, env=env)
    return path_dssp_output


def run_socket(
    pdb_file: Path,
    path_dssp_output: Path,
    i_worker: str = "0",
    bin_socket: str = "socket2",
    threshold: float = 7.0,
) -> tuple[dict, Path]:

    # run socket
    path_socket_file = tmp_dir / f"temp_{i_worker}.socket"
    socket_command = f"{bin_socket} -f {pdb_file} -s {path_dssp_output} -c {threshold} > {path_socket_file}"
    subprocess.call(socket_command, shell=True)

    # parse socket results
    with open(path_socket_file) as inpt:
        list_knobs = [line.strip().split() for line in inpt if line.startswith("knob ")]

    # (resi, chain) pairs
    list_resi_knobs = [data[6].split(":") for data in list_knobs]
    list_resi_knobs = [(chain, int(resi)) for resi, chain in list_resi_knobs]

    # generate dictionary of results
    dict_socket = {
        "knobs": agg_list_resi(list_resi_knobs),
    }

    return (dict_socket, path_socket_file)


def agg_list_resi(list_resi: list) -> dict:
    """
    Take a list of (chain,resi) elements and aggregate into dict[chain] = [resi_list]
    """
    dict_bychain_resi = {}
    for chain, resi in list_resi:
        if chain not in dict_bychain_resi:
            dict_bychain_resi[chain] = [resi]
        else:
            dict_bychain_resi[chain].append(resi)

    return dict_bychain_resi
