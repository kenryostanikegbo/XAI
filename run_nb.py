"""Execute a Jupyter notebook by running each code cell in order.

Usage: python run_nb.py notebooks/01_data_loading_and_integration.ipynb

Reads the .ipynb JSON, extracts the code cells, executes each one in the
current Python process. Markdown cells are printed for orientation but not
executed. Errors stop the run; outputs are printed as they happen.

The script `chdir`s to the notebook's directory before execution so that
relative paths in the cells (e.g. '../data/raw/...') resolve correctly
regardless of where the user invokes the script from.
"""
import json
import os
import sys
import traceback
from pathlib import Path

# Force unbuffered stdout so we can monitor progress live when output is
# redirected to a file.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

def run(path: str) -> int:
    nb_path = Path(path).resolve()
    if not nb_path.exists():
        print(f'Notebook not found: {nb_path}')
        return 2
    nb_dir = nb_path.parent
    # chdir to the notebook's directory so relative paths in cells work.
    os.chdir(nb_dir)

    nb = json.loads(nb_path.read_text(encoding='utf-8'))
    cells = nb.get('cells', [])
    print(f'== Executing {nb_path.name} ({len(cells)} cells) ==')
    print(f'   cwd = {os.getcwd()}\n')

    # Maintain execution state across cells via a namespace built up as we go
    # (so later cells can see earlier cells' variables).
    ns = {'__name__': '__main__'}
    for i, cell in enumerate(cells, 1):
        ctype = cell.get('cell_type', 'code')
        source = cell.get('source', [])
        if isinstance(source, list):
            source = ''.join(source)
        if ctype == 'markdown':
            print(f'\n----- cell {i} (markdown) -----')
            for line in source.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    # Strip non-ASCII characters to avoid console encoding errors on Windows.
                    safe = line.encode('ascii', errors='replace').decode('ascii').replace('?', ' ')
                    print(' ', safe)
                    break
            continue
        print(f'\n----- cell {i} (code) -----', flush=True)
        sys.stdout.flush()
        try:
            exec(source, ns)
        except Exception:
            print('CELL FAILED:', flush=True)
            traceback.print_exc()
            return 1
        sys.stdout.flush()
    print(f'\n== {nb_path.name} finished ==')
    return 0

if __name__ == '__main__':
    sys.exit(run(sys.argv[1]))
