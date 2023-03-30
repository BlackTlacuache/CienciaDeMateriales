import nbformat
from nbconvert.exporters import PythonExporter

# Cargar el archivo .ipynb
with open('./cienciaMateriales.ipynb') as f:
    nb_content = f.read()

# Convertir a formato de diccionario
notebook_content = nbformat.reads(nb_content, as_version=nbformat.NO_CONVERT)

# Crear un objeto PythonExporter y convertir el notebook
exporter = PythonExporter()
exporter.exclude_input_prompt = True
exporter.exclude_output_prompt = True

output, _ = exporter.from_notebook_node(notebook_content)
with open('./cienciaMateriales.py','w') as f:
    f.write(output)