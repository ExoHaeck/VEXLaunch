import argparse
import requests
import time
import re
import random

# Colores
INTENSE_GREEN = '\033[38;5;10m'  # Verde fosforescente intenso
CYAN = '\033[96m'                # Azul cian
RED = '\033[91m'                 # Rojo
YELLOW = '\033[93m'              # Amarillo
RESET = '\033[0m'                # Reseteo de color
LIGHT_PURPLE = '\033[38;5;135m'  # Morado claro
MEDIUM_PURPLE = '\033[38;5;129m' # Morado medio
DARK_PURPLE = '\033[38;5;56m'    # Morado oscuro

def print_intro():
    """Print the ASCII art and introductory information."""
    ascii_art = """
\033[38;5;129m
___    ______________  _______                            ______  
__ |  / /__  ____/_  |/ /__  / ______ ____  _________________  /_ 
__ | / /__  __/  __    /__  /  _  __ `/  / / /_  __ \  ___/_  __ \\
__ |/ / _  /___  _    | _  /___/ /_/ // /_/ /_  / / / /__ _  / / /
_____/  /_____/  /_/|_| /_____/\__,_/ \__,_/ /_/ /_/\___/ /_/ /_/ 
                                                             
\033[0m
"""
    description = f"""
{INTENSE_GREEN}Esta herramienta está diseñada para
===================================

> Ser un launcher o lanzador de los payloads de VEX
> No te limites a solo un listado de cargas útiles, puedes probar con más.
> Tener en cuenta que el archivo de URLs tiene que contener la palabra FUZZ (por ejemplo: =FUZZ)
> Realizar búsqueda de vulnerabilidades de tipo time based y/o de error based{RESET}
"""
    rights_and_blog = f"""
{LIGHT_PURPLE}Derechos reservados a Agrawain.{RESET}
{LIGHT_PURPLE}Blog: https://www.hacksyndicate.tech/{RESET}
"""
    print(ascii_art)
    print(description)
    print(rights_and_blog)

def load_user_agents(file_path='User-Agents.txt'):
    """Load user agents from a specified file."""
    with open(file_path, 'r') as file:
        user_agents = [line.strip() for line in file if line.strip()]
    return user_agents

def check_vulnerability(url, payloads, user_agents, proxy=None, timeout=60):
    """Check if the URL is vulnerable using the given payloads and user agents."""
    for payload in payloads:
        test_url = url.replace("FUZZ", payload)
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        
        try:
            start_time = time.time()
            response = requests.get(test_url, headers=headers, proxies=proxies, timeout=timeout)
            response_time = time.time() - start_time

            # Check for SQL errors
            sql_errors = [
                # MySQL errors
                "SQL syntax error", "You have an error in your SQL syntax", "MySQL server version",
                "Unknown column", "Table '.*' doesn't exist", "You have an error in your SQL syntax near",
                "mysql_fetch", "mysql_query", "1064 - You have an error in your SQL syntax",
                "1146 - Table '.*' doesn't exist", "1054 - Unknown column '.*' in 'field list'",
                "1451 - Cannot delete or update a parent row: a foreign key constraint fails",
                # PostgreSQL errors
                "ERROR: syntax error at or near", "ERROR: column '.*' does not exist",
                "ERROR: relation '.*' does not exist", "ERROR: invalid input syntax for integer",
                "ERROR: operator does not exist", "ERROR: missing FROM-clause entry for table",
                "ERROR: could not connect to server", "ERROR: permission denied for table",
                "ERROR: duplicate key value violates unique constraint",
                # Microsoft SQL Server errors
                "Incorrect syntax near", "Unclosed quotation mark after the character string",
                "Msg 102, Level 15, State 1", "Invalid column name", "Invalid object name",
                "Msg 207, Level 16, State 1", "Msg 208, Level 16, State 1",
                "Msg 2627, Level 14, State 1", "Msg 50000, Level 16, State 1",
                # Oracle errors
                "ORA-00936: missing expression", "ORA-00942: table or view does not exist",
                "ORA-01722: invalid number", "ORA-06512", "ORA-00933: SQL command not properly ended",
                "ORA-00001: unique constraint (.*) violated", "ORA-01403: no data found",
                "ORA-04063: view '.*' has errors",
                # SQLite errors
                "SQLite::SQLException", "SQL error or missing database", "no such column:",
                "no such table:", "syntax error near", "duplicate column name:",
                "constraint failed", "unrecognized token:",
                # General SQL Errors
                "SQL Error", "Database Error", "Query failed", "Invalid SQL query",
                "Error in SQL statement", "Database connection error", "Syntax error"
            ]

            if any(re.search(error, response.text, re.IGNORECASE) for error in sql_errors):
                print(f"{RED}[ALERTA SQL ERROR]{RESET} {test_url} ha generado un error SQL con el payload: {payload}")
                print(f"{RED}Response Time: {response_time} seconds{RESET}")
                continue

            # Check for delays indicating possible vulnerability
            if response_time > 2:  # Adjust the threshold as needed
                print(f"{RED}[POTENCIALMENTE VULNERABLE]{RESET} {test_url} puede ser vulnerable con el payload: {payload}")
                print(f"{RED}Response Time: {response_time} seconds{RESET}")
            else:
                print(f"{MEDIUM_PURPLE}Testing URL: {test_url}{RESET}")
                print(f"{CYAN}Response Time: {response_time} seconds{RESET}")

        except requests.RequestException as e:
            print(f"{RED}Error en la solicitud para {test_url}: {e}{RESET}")

if __name__ == "__main__":
    print_intro()

    parser = argparse.ArgumentParser(description='Prueba de vulnerabilidad SQLi en URLs con payloads.')
    parser.add_argument('--url', required=True, help='Archivo de URLs con el marcador FUZZ.')
    parser.add_argument('--payloads', required=True, help='Archivo de payloads para pruebas SQLi.')
    parser.add_argument('--proxy', help='Proxy para las solicitudes HTTP (opcional).')

    args = parser.parse_args()

    with open(args.url, 'r') as url_file:
        urls = [line.strip() for line in url_file]

    with open(args.payloads, 'r') as payload_file:
        payloads = [line.strip() for line in payload_file]

    user_agents = load_user_agents()  # No need to pass the file path now

    for url in urls:
        print(f"{CYAN}Testing URL: {url}{RESET}")
        check_vulnerability(url, payloads, user_agents, proxy=args.proxy)
