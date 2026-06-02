import subprocess
import tempfile
from pathlib import Path

CACHE_DIR = Path("$HOME/.cache/libcifpp")
COMPONENTS_FILE = CACHE_DIR / "components.cif"
tmp_dir = Path(tempfile.gettempdir())


def run_dssp(pdb_file: Path, i_worker: int = 0, bin_dssp: str = "mkdssp") -> Path:
    # run DSSP
    path_dssp_output = tmp_dir / f"temp_{i_worker}.dssp"
    dssp_setup = f"export LIBCIFPP_DATA_DIR={CACHE_DIR}"
    dssp_command = f"{bin_dssp} {pdb_file} --output-format dssp > {path_dssp_output}"
    subprocess.call(dssp_setup + "&&" + dssp_command, shell=True)
    return path_dssp_output


def run_socket(
    pdb_file: Path,
    i_worker: int = 0,
    bin_socket: str = "./data/SOCKET/socket2_linux",
    threshold: float = 7.0,
) -> dict:
    dict_socket = {}

    # run DSSP
    name_dssp_file = run_dssp(pdb_file, i_worker)

    # run socket
    path_socket_file = tmp_dir / f"temp_{i_worker}.socket"
    socket_command = f"{bin_socket} -f {pdb_file} -s {name_dssp_file} -c {threshold} > {path_socket_file}"
    subprocess.call(socket_command, shell=True)

    # parse socket results
    with open(path_socket_file) as inpt:
        list_knobs = [line.strip().split() for line in inpt if line.startswith("knob ")]

    # (resi, chain) pairs
    list_resi_knobs = [data[6].split(":") for data in list_knobs]
    list_resi_knobs = [(chain, int(resi)) for resi, chain in list_resi_knobs]

    dict_socket["knobs"] = agg_list_resi(list_resi_knobs)
    print(dict_socket)
    return dict_socket


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
