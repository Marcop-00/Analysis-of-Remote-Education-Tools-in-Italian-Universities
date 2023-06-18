import csv
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Funzione per cercare la presenza di Microsoft Teams o MS Teams nella pagina
def search_page(url):
    try:
        # Effettua una richiesta all'URL specificato
        response = requests.get(url)
        # Crea un oggetto BeautifulSoup a partire dalla risposta della richiesta
        soup = BeautifulSoup(response.content, "html.parser")
    except:
        # In caso di eccezione, restituisce False
        return False
    
    # Cerca la presenza di "Microsoft Teams" o "MS Teams" nella pagina
    if "Microsoft Teams" in str(soup) or "MS Teams" in str(soup):
        print(f"Microsoft Teams trovato in {url}")
        # Restituisce True se trovato
        return True
    else:
        # Restituisce False se non trovato
        return False

# Funzione principale per effettuare la ricerca su ogni singolo dominio
def main_function(domain):
    # Costruisce l'URL completo a partire dal dominio
    url = f"https://www.{domain}/"
    if search_page(url):
        # Se Microsoft Teams viene trovato nella pagina principale, lo segnala e interrompe la funzione
        print(f"Microsoft Teams trovato in {url}")
        return True
    else:
        try:
            # Effettua una richiesta all'URL
            response = requests.get(url)
            # Crea un oggetto BeautifulSoup a partire dalla risposta
            soup = BeautifulSoup(response.content, "html.parser")
            # Cerca tutti i link presenti nella pagina
            links = [link.get("href") for link in soup.find_all("a")]
            for link in links:
                if link.startswith("http") and search_page(link):
                    # Se Microsoft Teams viene trovato in uno dei link, interrompe la funzione
                    break
        except:
            # In caso di eccezione, restituisce False
            return False

# Apre il file CSV che contiene i domini degli atenei
with open("Domini_atenei.csv") as file:
    reader = csv.reader(file)
    # Legge i domini dal file CSV
    domains = [row[0] for row in reader]

# Crea un pool di thread con massimo 5 worker
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Effettua la ricerca su ogni dominio utilizzando la funzione principale
    results = [executor.submit(main_function, domain) for domain in domains]
