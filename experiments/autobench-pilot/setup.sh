#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
root="$PWD"
local_dir="$root/.local"
mkdir -p "$local_dir/bin" sources output

packages=()
if ! command -v iverilog >/dev/null || ! command -v vvp >/dev/null; then
    if [[ ! -x "$local_dir/sim/usr/bin/iverilog" || ! -x "$local_dir/sim/usr/bin/vvp" ]]; then
        packages+=(iverilog)
    fi
fi
if [[ "${INSTALL_VERILATOR:-1}" == 1 ]] && ! command -v verilator >/dev/null &&
    [[ ! -x "$local_dir/sim/usr/bin/verilator" ]]; then
    packages+=(verilator)
fi

if (( ${#packages[@]} )); then
    if (( EUID == 0 )); then
        apt-get update
        apt-get install -y --no-install-recommends "${packages[@]}"
    else
        # Use APT's signed indexes and extract the selected Debian packages in the workspace.
        apt_dir="$local_dir/apt"
        mkdir -p "$apt_dir"/{config,lists/partial,archives/partial,packages} "$local_dir/sim"
        cat > "$apt_dir/apt.conf" <<EOF
Dir::Etc::parts "$apt_dir/config";
Dir::Etc::main "/dev/null";
Dir::State::lists "$apt_dir/lists";
Dir::Cache::archives "$apt_dir/archives";
Acquire::Languages "none";
Acquire::Retries "2";
EOF
        (
            export APT_CONFIG="$apt_dir/apt.conf"
            apt-get update
            download_dir="$(mktemp -d "$apt_dir/packages/download.XXXXXX")"
            trap 'rm -rf -- "$download_dir"' EXIT
            cd "$download_dir"
            for package in "${packages[@]}"; do
                apt-get download "$package"
                for deb in "${package}"_*.deb; do
                    dpkg-deb -x "$deb" "$local_dir/sim"
                done
            done
        )
    fi
fi

if [[ -x "$local_dir/sim/usr/bin/iverilog" ]]; then
    cat > "$local_dir/bin/iverilog" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
sim_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../sim" && pwd)"
for ivl_dir in "$sim_dir"/usr/lib/*/ivl "$sim_dir"/usr/lib/ivl; do
    if [[ -x "$ivl_dir/ivl" ]]; then
        exec "$sim_dir/usr/bin/iverilog" -B "$ivl_dir" "$@"
    fi
done
echo 'Icarus Verilog support binaries were not found.' >&2
exit 1
EOF
    chmod +x "$local_dir/bin/iverilog"
    ln -sfn ../sim/usr/bin/vvp "$local_dir/bin/vvp"
fi
if [[ -x "$local_dir/sim/usr/bin/verilator" ]]; then
    ln -sfn ../sim/usr/bin/verilator "$local_dir/bin/verilator"
fi

opencode_version=1.19.6
opencode_cli="$local_dir/npm/node_modules/.bin/opencode"
manifest="$local_dir/npm/node_modules/opencode-ai/package.json"
if [[ ! -x "$opencode_cli" ]] ||
    [[ "$(node -p 'require(process.argv[1]).version' "$manifest")" != "$opencode_version" ]]; then
    npm install --prefix "$local_dir/npm" --no-audit --no-fund "opencode-ai@$opencode_version"
fi
ln -sfn ../npm/node_modules/.bin/opencode "$local_dir/bin/opencode"

checkout() {
    local repo="$1" revision="$2" path="sources/$1"
    if [[ ! -d "$path/.git" ]]; then
        git init -q "$path"
        git -C "$path" remote add origin "https://github.com/AutoBench/$repo.git"
    fi
    if ! git -C "$path" cat-file -e "$revision^{commit}" 2>/dev/null; then
        git -C "$path" fetch --depth 1 origin "$revision"
    fi
    if [[ "$(git -C "$path" rev-parse --verify HEAD 2>/dev/null || true)" != "$revision" ]]; then
        git -C "$path" checkout --detach "$revision"
    fi
}
checkout AutoBench 2c1d73c1188222c2bf0e323b87d64e2385c401fa
checkout CorrectBench a2dcd36097b9416fd48dece8c2801401425dfcd1

export PATH="$local_dir/bin:$PATH"
iverilog -V | sed -n '1p'
vvp -V 2>&1 | sed -n '1p'
if command -v verilator >/dev/null; then
    verilator --version
fi
opencode --version
python3 --version
printf '\nPrepare from pinned sources: python3 %q\n' "$root/prepare.py"
printf 'Run or resume the pilot: python3 %q\n' "$root/run_pilot.py"
