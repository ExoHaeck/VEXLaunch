import re
import argparse

def replace_params_with_fuzz(url):
    # Usamos una expresión regular para encontrar los valores después del signo '='
    return re.sub(r'=(.*?)(&|$)', '=FUZZ\\2', url)

def process_urls(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.readlines()

    fuzzed_urls = [replace_params_with_fuzz(url.strip()) for url in urls]

    # Guardar los resultados en el archivo de salida
    with open(output_file, 'w') as f:
        for url in fuzzed_urls:
            f.write(url + '\n')

    print(f"Se han procesado {len(fuzzed_urls)} URLs y reemplazado los parámetros con FUZZ.")

if __name__ == '__main__':
    # Definir los argumentos
    parser = argparse.ArgumentParser(description="Reemplaza los valores de los parámetros en URLs con FUZZ.")
    parser.add_argument('--file', type=str, required=True, help='Archivo de entrada con las URLs.')
    parser.add_argument('--out', type=str, required=True, help='Archivo de salida para las URLs con FUZZ.')
    
    # Parsear los argumentos
    args = parser.parse_args()

    # Procesar las URLs
    process_urls(args.file, args.out)
