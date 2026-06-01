#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR="${HOME}/.cache/libcifpp"
COMPONENTS_FILE="${CACHE_DIR}/components.cif"

mkdir -p "${CACHE_DIR}"

if [[ ! -f "${COMPONENTS_FILE}" ]]; then
    echo "Downloading components.cif..."
    curl -L \
        "https://files.wwpdb.org/pub/pdb/data/monomers/components.cif" \
        -o "${COMPONENTS_FILE}"
fi

export LIBCIFPP_DATA_DIR="${CACHE_DIR}"
