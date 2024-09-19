## VEXLaunch

**VEXLaunch** es una herramienta diseñada para probar vulnerabilidades SQLi en URLs usando payloads personalizados. Utiliza un enfoque basado en la búsqueda de errores SQL y retrasos en las respuestas para identificar posibles vulnerabilidades.

## Descripción
Esta herramienta permite:

- Probar URLs para vulnerabilidades SQLi usando un conjunto de payloads.
- Configurar el uso de un proxy para las solicitudes HTTP. (se recomienda el uso de la extension de burpsuite IP ROTATE)
- Cargar agentes de usuario desde un archivo para evitar bloqueos de WAF.

## Requisitos

- Python 3
- Bibliotecas Python: requests, argparse
- Archivo de agentes de usuario (User-Agents.txt)
- Archivos de URLs y payloads

## Uso:

**1. Usar paramspider con el fin de generar el archivo ya con el parametro FUZZ**

```bash
paramspider -d spacex.com
```

El nos genera una carpeta llamada results debemos de ingresar y encontraremos el archivo que contiene las URL ya con el parametro FUZZ incrustado.

**2. Preparación de URLs con el marcador FUZZ.** 

Para generar un archivo de URLs con el marcador FUZZ, puedes utilizar los siguientes comandos:

```bash
subfinder -d spacex.com -silent > subdomains
batcat subdomains | waybackurls | tee waybackURL.txt
batcat waybackURL.txt | gf sqli | tee waybackSQL.txt
```

Luego, realiza las modificaciones necesarias para reemplazar parámetros con FUZZ:

```bash
python3 parametros_FUZZ.py --file waybackSQL.txt --out SQLFUZZ.txt
```

Esto procesará las URLs y reemplazará los parámetros con FUZZ.

**Ejecutar la herramienta**

Una vez que tengas el archivo SQLFUZZ.txt con el marcador FUZZ, puedes lanzar la herramienta con el siguiente comando:

```bash
python3 VEXLaunch.py --url SQLFUZZ.txt --payloads list.txt
```

## Ejemplo de Ejecución

```bash
python3 VEXLaunch.py --url SQLFUZZ.txt --payloads payloads.txt --proxy http://proxy.example.com
```

## Notas

- Asegúrate de que el archivo de URLs contenga el marcador FUZZ en los parámetros que deseas probar.
- La herramienta imprimirá alertas en rojo si detecta errores SQL y mensajes en verde fosforescente si está realizando la prueba.

## Licencia

Derechos reservados a Agrawain. Blog: hacksyndicate.tech











