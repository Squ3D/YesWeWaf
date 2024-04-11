# YesWeWaf
YesWeWaf
Description
YesWeWaf is a Web Application Firewall Tester designed to help identify vulnerabilities in web applications.

Installation
Assurez-vous d'avoir Python 3 installé sur votre système. Si ce n'est pas le cas, veuillez le télécharger et l'installer depuis le site officiel de Python.

Clonez ce dépôt Git sur votre machine en utilisant la commande suivante :

bash
https://github.com/Squ3D/YesWeWaf.git

bash
cd YesWeWaf
Installez les dépendances requises en exécutant la commande suivante :

bash
pip3 install -r requirements.txt
Utilisation
Pour utiliser YesWeWaf, exécutez le script YesWeWaf.py en ligne de commande et spécifiez les options nécessaires.

bash
python3 YesWeWaf.py <url> [--test-rce] [--test-sql] [--test-rfi-rce] [--payloads-file <chemin_fichier>] [--export-csv]
Options disponibles :
<url> : URL de l'application web à tester (obligatoire).
--test-rce : Teste les vulnérabilités XSS.
--test-sql : Teste les vulnérabilités d'injection SQL.
--test-rfi-rce : Teste les vulnérabilités d'inclusion de fichier à distance (RFI) et d'exécution de code à distance (RCE).
--payloads-file <chemin_fichier> : Chemin vers le fichier contenant les charges utiles personnalisées.
--export-csv : Exporte les résultats vers un fichier CSV.
Exemple :
bash
Copy code
python3 YesWeWaf.py https://example.com --test-sql --export-csv
if __name__ == "__main__":
Le bloc de code if __name__ == "__main__": permet d'exécuter du code spécifique uniquement lorsque le script est exécuté directement et pas lorsqu'il est importé en tant que module dans un autre script. Dans le cas de YesWeWaf, ce bloc est utilisé pour analyser les arguments de la ligne de commande lorsque le script est exécuté directement.

python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YesWeWaf: Web Application Firewall Tester")
    parser.add_argument("url", help="URL of the web application to test")
    parser.add_argument("--test-rce", action="store_true", help="Test for XSS vulnerabilities")
    parser.add_argument("--test-sql", action="store_true", help="Test for SQL Injection vulnerabilities")
    parser.add_argument("--test-rfi-rce", action="store_true", help="Test for Remote File Inclusion vulnerabilities")
    parser.add_argument("--payloads-file", help="Path to the file containing payloads")
    parser.add_argument("--export-csv", action="store_true", help="Export results to a CSV file")
    args = parser.parse_args()
