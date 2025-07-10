#!/usr/bin/env bash
#
# fix_dae_encoding.sh
# Strips any UTF-8 BOM and normalizes all COLLADA .dae files to use
#     <?xml version="1.0" encoding="UTF-8"?>
#
# Usage:
#   ./fix_dae_encoding.sh /path/to/ur3e_hande_robot_description/meshes

ROOT_DIR="${1:-.}"

# 1) Remove any UTF-8 BOM from every .dae
find "$ROOT_DIR" -type f -name '*.dae' \
  -exec sed -i '1s/^\xEF\xBB\xBF//' {} \;

# 2) Force the XML declaration to uppercase UTF-8
find "$ROOT_DIR" -type f -name '*.dae' \
  -exec sed -i '1s/encoding=".*"/encoding="UTF-8"/' {} \;

echo "All .dae files under $ROOT_DIR have been cleaned."

