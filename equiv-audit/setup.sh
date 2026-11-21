#!/usr/bin/env bash
# Local amd64 Debian 13 tool installation. No root privileges are needed.
set -euo pipefail
audit_prefix="$(realpath -m "${1:-./.work/tools}")"
mkdir -p "$audit_prefix/downloads" "$audit_prefix/install"
deb_root=https://deb.debian.org/debian/pool/main
packages=(
  y/yosys/yosys_0.52-2_amd64.deb
  z/z3/z3_4.13.3-1.1_amd64.deb
  b/berkeley-abc/berkeley-abc_1.01+20221019git70cb339+dfsg-4_amd64.deb
  b/boolector/boolector_3.2.4-1_amd64.deb
  b/btor2tools/libbtor2parser0_1.0.3-1_amd64.deb
  m/minisat2/minisat_2.2.1-8_amd64.deb
)
for pkg in "${packages[@]}"; do
    file="$audit_prefix/downloads/${pkg##*/}"
    if [[ ! -s "$file" ]]; then
        curl -fsSL "$deb_root/$pkg" -o "$file.tmp"
        mv "$file.tmp" "$file"
    fi
    dpkg-deb -x "$file" "$audit_prefix/install"
done
tool_usr="$audit_prefix/install/usr"
ln -sfn berkeley-abc "$tool_usr/bin/yosys-abc"
if [[ ! -d "$audit_prefix/sby/.git" ]]; then
    git clone -q --depth 1 --branch v0.52 https://github.com/YosysHQ/sby.git "$audit_prefix/sby"
fi
make -s -C "$audit_prefix/sby" install PREFIX="$tool_usr"
python3 -m pip install --quiet --target "$audit_prefix/python" click pyarrow pyslang
{
    printf 'export PATH=%q:"$PATH"\n' "$tool_usr/bin"
    printf 'export PYTHONPATH=%q:"${PYTHONPATH:-}"\n' "$tool_usr/share/yosys:$audit_prefix/python"
    printf 'export LD_LIBRARY_PATH=%q:"${LD_LIBRARY_PATH:-}"\n' "$tool_usr/lib:$tool_usr/lib/x86_64-linux-gnu"
} > "$audit_prefix/env.sh"
source "$audit_prefix/env.sh"
yosys -V
sby --version
yosys-abc -c version
z3 --version
boolector --version
