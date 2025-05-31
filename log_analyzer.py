import os
import sys
from collections import defaultdict, Counter


def find_duplicates(directory):
    """Trouve les fichiers en double par taille dans un dossier."""
    size_to_files = defaultdict(list)
    
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            size = os.path.getsize(filepath)
            size_to_files[size].append(filepath)
    
    duplicates = {size: files for size, files in size_to_files.items() if len(files) > 1}
    return duplicates

def analyze_log(log_file):
    """Compte les ERROR, WARNING, INFO dans un fichier log."""
    levels = Counter()
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if 'ERROR' in line:
                    levels['ERROR'] += 1
                elif 'WARNING' in line:
                    levels['WARNING'] += 1
                elif 'INFO' in line:
                    levels['INFO'] += 1
    except FileNotFoundError:
        print(f"Erreur : Fichier {log_file} non trouvé.")
        sys.exit(1)
    return levels

def export_results(duplicates, log_stats, output_file):
    """Exporte les résultats dans un fichier rapport.txt."""
    with open(output_file, 'w') as f:
        # Ajouter dans export_results, après l'ouverture du fichier
        import colorama
        colorama.init()
        f.write(f"{colorama.Fore.GREEN}=== Rapport d'analyse ==={colorama.Style.RESET_ALL}\n")
        f.write("=== Rapport d'analyse ===\n\n")
        
        f.write("Fichiers en double (par taille) :\n")
        if duplicates:
            for size, files in duplicates.items():
                f.write(f"Taille {size} octets :\n")
                for file in files:
                    f.write(f"  - {file}\n")
        else:
            f.write("Aucun fichier en double trouvé.\n")
        
        f.write("\nStatistiques du fichier log :\n")
        for level, count in log_stats.items():
            f.write(f"{level}: {count}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python log_analyzer.py <dossier> <fichier_log>")
        sys.exit(1)
    
    directory = sys.argv[1]
    log_file = sys.argv[2]
    
    # Analyser les doublons et les logs
    duplicates = find_duplicates(directory)
    log_stats = analyze_log(log_file)
    
    # Exporter les résultats
    export_results(duplicates, log_stats, "rapport.txt")
    print("Analyse terminée. Résultats exportés dans rapport.txt")

if __name__ == "__main__":
    main()