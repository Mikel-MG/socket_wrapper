import os
from pathlib import Path

from .common import fix_pdb, run_dssp, run_socket

# infer location of SOCKET binary
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
path_default_socket = ROOT_DIR / "data/SOCKET/socket2_linux"

CACHE_DIR = Path.home() / ".cache" / "libcifpp"
# COMPONENTS_FILE = CACHE_DIR / "components.cif"


class SocketCC:
    def __init__(
        self, bin_dssp: str = "mkdssp", bin_socket: str = str(path_default_socket)
    ):
        # TODO: Add a method to check installation / suggest download of components.cif file
        self.bin_dssp = bin_dssp
        self.bin_socket = bin_socket
        # TODO: Add checks for presence of binaries

        # set environment
        env = os.environ.copy()
        env["LIBCIFPP_DATA_DIR"] = str(CACHE_DIR)
        self.env = env

    def detect_kih(
        self,
        path_pdb: Path,
        i_worker: str = "0",
        auto_fix_pdb: bool = False,
        delete_tempfiles: bool = True,
    ):
        # fix PDB file
        # TODO: Review, inconsistent API
        if auto_fix_pdb is True:
            path_pdb = fix_pdb(path_pdb, i_worker)

        # run DSSP and generate temporary file
        path_dssp_file = run_dssp(
            path_pdb, i_worker, bin_dssp=self.bin_dssp, env=self.env
        )

        # run SOCKET
        dict_socket, path_socket_file = run_socket(
            path_pdb, path_dssp_file, i_worker, bin_socket=self.bin_socket
        )

        # optional: remove temporary files
        if delete_tempfiles is True:
            path_dssp_file.unlink()
            path_socket_file.unlink()

        return dict_socket
