# Étape 1 : Image Python stable
FROM python:3.10-slim

# Étape 2 : Installer LaTeX minimal (pour la compilation PDF)
RUN apt-get update && \
    apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra && \
    apt-get clean

# Étape 3 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 4 : Copier tous les fichiers du projet dans le conteneur
COPY . .

# Étape 5 : Installer les dépendances Python nécessaires
RUN pip install --no-cache-dir pandas jinja2

# Étape 6 : Arguments par défaut (modifiables dans la commande docker run)
ENTRYPOINT ["python", "generate_flash.py"]
CMD ["--level", "3e", "4e", "--topic", "pythagore", "thales", "puissances", "--n", "5", "--compile"]
