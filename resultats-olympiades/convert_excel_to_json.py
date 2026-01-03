# Script de conversion Excel vers JSON pour l'application Olympiades
# Ce script lit le fichier Excel et génère le fichier data.js

import pandas as pd
import json
from datetime import datetime
import re
import secrets
import string

def extract_department_from_rne(rne):
    """Extrait le numéro de département du code RNE"""
    if pd.isna(rne) or not str(rne):
        return ""
    rne_str = str(rne).strip()
    # Les 2 premiers chiffres du RNE correspondent au département
    # Format: 0XXYYYY où XX est le département
    if len(rne_str) >= 4:
        # Extraire les chiffres 2 et 3 (après le 0 initial)
        dept = rne_str[1:3]
        if dept in ['77', '93', '94']:
            return dept
    return ""

def generate_password(length=8):
    """Génère un mot de passe aléatoire sécurisé"""
    # Utiliser uniquement lettres et chiffres pour éviter confusion
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # Exclure les caractères ambigus
    alphabet = alphabet.replace('0', '').replace('O', '').replace('l', '').replace('I', '')
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def extract_uai_from_rne(rne):
    """Extrait le code UAI (même que RNE) et le formate correctement"""
    if pd.isna(rne) or not str(rne):
        return ""
    return str(rne).strip().upper()

def excel_to_json(excel_file='Résultats.xlsx', output_file='data.js'):
    """
    Convertit le fichier Excel des résultats en fichier data.js
    
    Le fichier Excel doit contenir les colonnes suivantes :
    - Département (ou Department)
    - Établissement (ou Establishment)
    - Nom Élève (ou StudentName)
    - Date de naissance (ou BirthDate)
    - Niveau (ou Level)
    - Score Individuel (ou IndividualScore)
    - Classement Individuel (ou IndividualRank)
    - Nom Équipe (ou TeamName)
    - Score Équipe (ou TeamScore)
    - Classement Équipe (ou TeamRank)
    - Membres Équipe (ou TeamMembers) - séparés par des virgules ou points-virgules
    """
    
    try:
        # Lire le fichier Excel
        print("📖 Lecture du fichier Excel...")
        df = pd.read_excel(excel_file)
        
        print(f"✅ {len(df)} lignes trouvées")
        print(f"📋 Colonnes détectées : {list(df.columns)}")
        print("\nAperçu des 3 premières lignes :")
        print(df.head(3))
        print("\n" + "="*60)
        
        # Nettoyer les noms de colonnes (enlever espaces et retours à la ligne)
        df.columns = df.columns.str.strip().str.replace('\n', ' ')
        
        # Mapper les noms de colonnes détectées
        column_mapping = {
            'RNE': 'rne',
            'NOM ETABLISSEMENT': 'establishment',
            'Nom Etablissement': 'establishment',
            'ETABLISSEMENT': 'establishment',
            'NOM': 'lastName',
            'Nom': 'lastName',
            'PRENOM': 'firstName',
            'Prénom': 'firstName',
            'Prenom': 'firstName',
            'DATE NAISSANCE': 'birthDate',
            'Date Naissance': 'birthDate',
            'Date de naissance': 'birthDate',
            "Résultat à l'épreuve individuelle": 'individualResult',
            "Resultat individuel": 'individualResult',
            "Résultat à l'épreuve en équipe": 'teamResult',
            "Resultat equipe": 'teamResult',
            "Résultat équipe": 'teamResult',
            'Niveau': 'level',
            'Classe': 'level',
            # Anciens mappings pour compatibilité
            'Département': 'department',
            'Department': 'department',
            'Etablissement': 'establishment',
            'Établissement': 'establishment',
            'Establishment': 'establishment',
            'Nom Élève': 'studentName',
            'Nom Eleve': 'studentName',
            'StudentName': 'studentName',
            'Nom': 'studentName',
            'Date de naissance': 'birthDate',
            'Date Naissance': 'birthDate',
            'BirthDate': 'birthDate',
            'Niveau': 'level',
            'Level': 'level',
            'Classe': 'level',
            'Score Individuel': 'individualScore',
            'Score': 'individualScore',
            'IndividualScore': 'individualScore',
            'Classement Individuel': 'individualRank',
            'Classement': 'individualRank',
            'IndividualRank': 'individualRank',
            'Rang': 'individualRank',
            'Nom Équipe': 'teamName',
            'Nom Equipe': 'teamName',
            'Équipe': 'teamName',
            'Equipe': 'teamName',
            'TeamName': 'teamName',
            'Score Équipe': 'teamScore',
            'Score Equipe': 'teamScore',
            'TeamScore': 'teamScore',
            'Classement Équipe': 'teamRank',
            'Classement Equipe': 'teamRank',
            'TeamRank': 'teamRank',
            'Membres Équipe': 'teamMembers',
            'Membres Equipe': 'teamMembers',
            'Membres': 'teamMembers',
            'TeamMembers': 'teamMembers'
        }
        
        # Renommer les colonnes
        df = df.rename(columns=column_mapping)
        
        # Convertir les données en liste de dictionnaires
        results = []
        
        for index, row in df.iterrows():
            try:
                # Extraire le département du code RNE
                department = extract_department_from_rne(row.get('rne', ''))
                
                # Extraire le code UAI
                uai = extract_uai_from_rne(row.get('rne', ''))
                
                # Construire le nom complet de l'élève
                first_name = str(row.get('firstName', '')).strip() if pd.notna(row.get('firstName')) else ''
                last_name = str(row.get('lastName', '')).strip() if pd.notna(row.get('lastName')) else ''
                student_name = f"{first_name} {last_name}".strip()
                
                # Convertir la date de naissance
                birth_date = row.get('birthDate', '')
                if pd.notna(birth_date):
                    if isinstance(birth_date, datetime):
                        birth_date = birth_date.strftime('%Y-%m-%d')
                    elif isinstance(birth_date, str):
                        # Essayer de parser différents formats de date
                        try:
                            parsed_date = pd.to_datetime(birth_date, dayfirst=True)
                            birth_date = parsed_date.strftime('%Y-%m-%d')
                        except:
                            pass
                else:
                    birth_date = ''
                
                # Récupérer les résultats
                establishment = str(row.get('establishment', '')).strip() if pd.notna(row.get('establishment')) else ''
                individual_result = str(row.get('individualResult', '')).strip() if pd.notna(row.get('individualResult')) else ''
                team_result = str(row.get('teamResult', '')).strip() if pd.notna(row.get('teamResult')) else ''
                level = str(row.get('level', 'Seconde')).strip() if pd.notna(row.get('level')) else 'Seconde'
                
                # Créer l'objet résultat
                result = {
                    'uai': uai,
                    'department': department,
                    'establishment': establishment,
                    'studentName': student_name,
                    'birthDate': birth_date,
                    'level': level,
                    'individualResult': individual_result,
                    'teamResult': team_result,
                    'individualScore': 0,  # Non disponible dans les données
                    'individualRank': '',  # Non disponible dans les données
                    'teamName': '',        # Non disponible dans les données
                    'teamScore': 0,        # Non disponible dans les données
                    'teamRank': '',        # Non disponible dans les données
                    'teamMembers': []      # Non disponible dans les données
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"⚠️ Erreur ligne {index + 2}: {str(e)}")
                continue
        
        print(f"\n✅ {len(results)} résultats convertis avec succès")
        
        # Générer les identifiants des établissements (UAI + mot de passe)
        print(f"\n🔑 Génération des identifiants établissements...")
        establishments_credentials = {}
        
        for result in results:
            uai = result.get('uai', '')
            establishment_name = result.get('establishment', '')
            
            if uai and establishment_name and uai not in establishments_credentials:
                password = generate_password(8)
                establishments_credentials[uai] = {
                    'uai': uai,
                    'name': establishment_name,
                    'password': password,
                    'department': result.get('department', '')
                }
        
        print(f"✅ {len(establishments_credentials)} établissements trouvés")
        
        # Générer le fichier establishments.js
        establishments_file = 'establishments.js'
        print(f"\n📝 Génération du fichier {establishments_file}...")
        
        with open(establishments_file, 'w', encoding='utf-8') as f:
            f.write("// Identifiants des établissements (UAI + mot de passe)\n")
            f.write("// Fichier généré automatiquement à partir de " + excel_file + "\n")
            f.write(f"// Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("const ESTABLISHMENTS_CREDENTIALS = ")
            
            # Convertir le dictionnaire en liste pour le JSON
            credentials_list = list(establishments_credentials.values())
            json_str = json.dumps(credentials_list, ensure_ascii=False, indent=4)
            f.write(json_str)
            
            f.write(";\n\n")
            f.write("// Exporter les données\n")
            f.write("if (typeof module !== 'undefined' && module.exports) {\n")
            f.write("    module.exports = ESTABLISHMENTS_CREDENTIALS;\n")
            f.write("}\n")
        
        print(f"✅ Fichier {establishments_file} créé avec succès !")
        
        # Créer un fichier CSV pour les chefs d'établissement
        csv_file = 'identifiants_etablissements.csv'
        print(f"\n📝 Génération du fichier {csv_file} pour transmission aux établissements...")
        
        import csv
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['UAI', 'Mot de passe', 'Département', 'Nom Établissement'])
            for cred in sorted(credentials_list, key=lambda x: (x['department'], x['name'])):
                writer.writerow([cred['uai'], cred['password'], cred['department'], cred['name']])
        
        print(f"✅ Fichier {csv_file} créé avec succès !")
        print(f"   Ce fichier contient les identifiants à transmettre aux établissements.")
        
        # Générer le fichier data.js
        print(f"\n📝 Génération du fichier {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("// Base de données des résultats des Olympiades de Mathématiques\n")
            f.write("// Fichier généré automatiquement à partir de " + excel_file + "\n")
            f.write(f"// Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("const RESULTS_DATA = ")
            
            # Écrire le JSON avec indentation
            json_str = json.dumps(results, ensure_ascii=False, indent=4)
            f.write(json_str)
            
            f.write(";\n\n")
            f.write("// Message d'information pour le développement\n")
            f.write(f"console.log(`Base de données chargée : ${{RESULTS_DATA.length}} résultats disponibles`);\n\n")
            f.write("// Exporter les données pour une utilisation dans d'autres fichiers\n")
            f.write("if (typeof module !== 'undefined' && module.exports) {\n")
            f.write("    module.exports = RESULTS_DATA;\n")
            f.write("}\n")
        
        print(f"✅ Fichier {output_file} créé avec succès !")
        print(f"\n🎉 Conversion terminée ! Vous pouvez maintenant utiliser l'application.")
        
        return results
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{excel_file}' n'a pas été trouvé.")
        print("Assurez-vous que le fichier Excel est dans le même dossier que ce script.")
    except Exception as e:
        print(f"❌ Erreur lors de la conversion : {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("="*60)
    print("🔄 Conversion Excel → JSON pour l'Application Olympiades")
    print("="*60 + "\n")
    
    # Lancer la conversion
    excel_to_json('Résultats.xlsx', 'data.js')
    
    print("\n" + "="*60)
    input("\nAppuyez sur Entrée pour fermer...")
