import csv
import subprocess

# Crea una lista vuota per contenere i domini
domini = []
# Crea una lista vuota per contenere sia i domini che le info trovate
domini_lista = []

# Apri il file CSV "Domini_atenei.csv" e legge i domini in esso contenuti
with open("Domini_atenei.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Aggiungi ogni dominio alla lista
        domini.append(row[0])

# Imposta tre contatori per tenere traccia dei domini che utilizzano Google Workspace, Microsoft 365 o entrambi
google_counter = 0
microsoft_counter = 0
both_counter = 0
# Per ogni dominio nella lista
for dominio in domini:
    # Esegue il comando "nslookup" per ottenere informazioni sui record TXT
    process1 = subprocess.run(["nslookup", "-q=txt", dominio], stdout=subprocess.PIPE, universal_newlines=True)
    output = process1.stdout
    print("il dominio: ",dominio)
    print(output)

    # Esegue un altro comando "nslookup" per ottenere informazioni sui record MX
    process2 = subprocess.run(["nslookup", "-q=mx", dominio], stdout=subprocess.PIPE, universal_newlines=True)
    output2 = process2.stdout
    print(output2)
    
        # Verifica se il dominio utilizza Google Workspace
    if "ASPMX.L.GOOGLE.COM" in output2 or "google-site-verification" in output or "spf.google" in output:
        google_counter += 1
        # Verifica se il dominio utilizza Microsoft 365
        if "MS=" in output or "outlook.com" in output2 or "spf.protection.outlook" in output:
            both_counter += 1
            print("Utilizza entrambi")
            # Aggiunge alla lista dei domini il dominio e le info per la lista finale
            domini_lista.append((dominio, "Utilizza Entrambi"))
        else:
            print("Utilizza Google Workspace")
            domini_lista.append((dominio, "Utilizza Google Workspace"))
    else:
        print("Non utilizza Google Workspace")
        # Verifica se il dominio utilizza Microsoft 365
        if "MS=" in output or "outlook.com" in output2 or "spf.protection.outlook" in output:
            microsoft_counter += 1
            print("Utilizza Microsoft 365")
            domini_lista.append((dominio, "Utilizza Microsoft 365"))
        else:
            print("Non utilizza nessuno dei due")
            domini_lista.append((dominio, "Non utilizza nessuno dei due servizi"))

# Calcola e stampa le percentuali dei domini che utilizzano Google Workspace e Microsoft 365
total_domains = len(domini)
google_percentage = (google_counter / total_domains) * 100
microsoft_percentage = (microsoft_counter / total_domains) * 100
both_percentage = ((google_counter + microsoft_counter - both_counter) / total_domains) * 100

# Formatta la percentuale con massimo 2 numeri decimali
google_percentage_formatted = "{:.2f}".format(google_percentage)
microsoft_percentage_formatted = "{:.2f}".format(microsoft_percentage)
both_percentage_formatted = "{:.2f}".format(both_percentage)

# Stampa la lista finale con tutti i domini analizzati precedentemente inseriti
print("Domini e informazioni sul servizio di posta elettronica:")
for dominio, info in domini_lista:
    print(dominio, ":", info)

# Stampa le percentuali
print("Percentuale dei domini che utilizzano solo Google Workspace:", google_percentage_formatted, "%" )
print("Percentuale dei domini che utilizzano solo Microsoft 365:", microsoft_percentage_formatted, "%")
print("Percentuale dei domini che utilizzano sia Google Workspace che Microsoft 365:", both_percentage_formatted, "%")