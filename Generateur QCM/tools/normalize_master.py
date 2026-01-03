import pandas as pd
import os
import glob
from datetime import datetime

CANONICAL_COLUMNS = [
    'uid','level','topic','subtopic','skill','competence','format','difficulty','time_s',
    'stem_tex','answer_tex','distractors_tex','explanation_tex','tags','status','language',
    'source_path','source_file','author','date_created','date_modified','review_count','success_rate'
]

DEFAULT_VALUES = {
    'competence': '',
    'explanation_tex': '',
    'tags': '',
    'status': 'validé',
    'language': 'fr',
    'author': '',
    'date_created': None,
    'date_modified': None,
    'review_count': 0,
    'success_rate': None,
}

TAG_SEP = ';'
BACKUP_DIR = 'data/backups'
MASTER_PATH = 'data/master_questions.csv'
QUESTION_GLOB = 'data/questions/*/*.csv'


def load_all_question_files(pattern: str):
    files = glob.glob(pattern)
    frames = []
    for path in files:
        try:
            df = pd.read_csv(path, encoding='utf-8')
            df['source_path'] = path.replace('\\', '/')
            df['source_file'] = os.path.basename(path)
            frames.append(df)
        except Exception as e:
            print(f"[WARN] Échec lecture {path}: {e}")
    if not frames:
        raise RuntimeError('Aucun fichier question chargé.')
    return pd.concat(frames, ignore_index=True)


def coerce_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie harmonisée du DataFrame source selon le schéma canonique."""
    work = df.copy()
    for col in CANONICAL_COLUMNS:
        if col not in work.columns:
            work[col] = DEFAULT_VALUES.get(col, '')
    work = work[CANONICAL_COLUMNS].copy()
    work['difficulty'] = pd.to_numeric(work['difficulty'], errors='coerce').fillna(1).astype(int)
    work['time_s'] = pd.to_numeric(work['time_s'], errors='coerce').fillna(30).astype(int)
    work['review_count'] = pd.to_numeric(work['review_count'], errors='coerce').fillna(0).astype(int)

    def norm_tags(x):
        if pd.isna(x) or x == '':
            return ''
        parts = [p.strip().lower() for p in str(x).replace(',', TAG_SEP).split(TAG_SEP) if p.strip()]
        seen = set()
        ordered = []
        for p in parts:
            if p not in seen:
                seen.add(p)
                ordered.append(p)
        return TAG_SEP.join(ordered)
    work['tags'] = work['tags'].apply(norm_tags)

    now = datetime.now().strftime('%Y-%m-%d')
    work['date_created'] = work['date_created'].fillna('').replace({pd.NA: ''})
    empty_created = work['date_created'] == ''
    work.loc[empty_created, 'date_created'] = now
    work['date_modified'] = now
    return work


def validate(df: pd.DataFrame):
    errors = []
    # Unicité uid
    duplicated = df['uid'][df['uid'].duplicated()].unique()
    if len(duplicated):
        errors.append(f"UIDs dupliqués: {', '.join(duplicated)}")
    # Champs obligatoires
    mandatory = ['uid','level','topic','stem_tex','answer_tex','format','difficulty']
    for col in mandatory:
        missing = df[col].isna() | (df[col].astype(str).str.strip() == '')
        if missing.any():
            errors.append(f"Valeurs manquantes dans {col}: {missing.sum()}")
    # Difficulté dans 1..5 (préparation d'un futur niveau 5)
    if not df['difficulty'].between(1,5).all():
        errors.append('Valeurs difficulty hors intervalle 1..5')
    if errors:
        print('[VALIDATION] Problèmes rencontrés:')
        for e in errors:
            print(' -', e)
    else:
        print('[VALIDATION] OK')


def summary(df: pd.DataFrame):
    print('\n=== RÉSUMÉ ===')
    print('Total questions :', len(df))
    print('\nPar niveau :')
    print(df['level'].value_counts())
    print('\nPar thème :')
    print(df['topic'].value_counts())
    print('\nDifficulté :')
    print(df['difficulty'].value_counts().sort_index())
    missing_expl = (df['explanation_tex'].str.strip()=='') | (df['explanation_tex'].isna())
    print(f"\nSans explication détaillée : {missing_expl.sum()} ({missing_expl.sum()/len(df):.1%})")


def backup_master():
    if not os.path.exists(MASTER_PATH):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(BACKUP_DIR, f'master_questions_{ts}.csv')
    try:
        os.replace(MASTER_PATH, dest)
        print(f'[BACKUP] Ancien master déplacé vers {dest}')
    except PermissionError:
        import shutil
        shutil.copy2(MASTER_PATH, dest)
        print(f'[BACKUP] Copie créée (fichier verrouillé) : {dest}')


def main():
    print('--- Normalisation du master ---')
    raw = load_all_question_files(QUESTION_GLOB)
    print(f'Chargé {len(raw)} lignes initiales. Colonnes détectées: {len(raw.columns)}')
    norm = coerce_columns(raw)
    validate(norm)
    summary(norm)
    backup_master()
    norm.to_csv(MASTER_PATH, index=False, encoding='utf-8')
    print(f'✅ Nouveau master écrit : {MASTER_PATH}')

if __name__ == '__main__':
    main()
