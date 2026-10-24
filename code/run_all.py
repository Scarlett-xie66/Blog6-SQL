"""Offline rebuild from included original source columns; full extraction is optional."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
for item in manifest['selected_files']:
 p=ROOT/'data'/item['filename']
 with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
 assert actual==item['sha256'],f'Source snapshot changed: {p.name}'
for script in ['02_sql_audit.py','03_validate_estimate.py','05_further_analysis.py','06_make_figures.py','build_article.py','check_article.py','check_quarto_source.py']:
 print('\nRunning',script,flush=True)
 subprocess.run([sys.executable,str(ROOT/'code'/script)],cwd=ROOT,check=True)
print('Rebuild and tutorial checks passed. Run python code/render_preview.py for HTML.')
