import subprocess
from pathlib import Path

CACHE_DIR = Path("$HOME/.cache/libcifpp")
COMPONENTS_FILE = CACHE_DIR / "components.cif"


def run_dssp(pdb_file: Path, i_worker: int = 0, bin_dssp: str = "mkdssp") -> Path:
    # run DSSP
    path_dssp_output = Path(f"temp_{i_worker}.dssp")
    dssp_setup = f"export LIBCIFPP_DATA_DIR={CACHE_DIR}"
    dssp_command = f"{bin_dssp} {pdb_file} --output-format dssp > {path_dssp_output}"
    subprocess.call(dssp_setup + "&&" + dssp_command, shell=True)
    return path_dssp_output


def run_socket(
    pdb_file: Path,
    i_worker: int = 0,
    bin_socket: str = "./data/SOCKET/socket2_linux",
    threshold: float = 7.0,
):
    # run DSSP
    name_dssp_file = run_dssp(pdb_file, i_worker)

    # run socket
    path_socket_file = Path(f"temp_{i_worker}.socket")
    socket_command = f"{bin_socket} -f {pdb_file} -s {name_dssp_file} -c {threshold} > {path_socket_file}"
    subprocess.call(socket_command, shell=True)

    # parse socket results
    with open(path_socket_file) as inpt:
        list_knobs = [line.strip().split() for line in inpt if line.startswith("knob ")]

    # TODO: Finish parsing!
    list_resi_knobs = [data[6].split(":")[0] for data in list_knobs]
    print(list_resi_knobs)
