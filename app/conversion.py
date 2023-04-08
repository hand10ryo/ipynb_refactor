import nbconvert
import nbformat

def convert_ipynb_to_py(ipynb_file_path, py_file_path):
    exporter = nbconvert.PythonExporter()
    source, _ = exporter.from_filename(ipynb_file_path)
    with open(py_file_path, 'w') as f:
        f.write(source)

def convert_py_to_ipynb(py_file_path, ipynb_file_path):
    with open(py_file_path, 'r') as f:
        code = f.read()

    nb = nbformat.v4.new_notebook()
    code_cells = [
        nbformat.v4.new_code_cell(source=c)
        for c in code.split("\n[newline]\n")
    ]
    nb['cells'] = code_cells

    with open(ipynb_file_path, 'w') as f:
        nbformat.write(nb, f)
