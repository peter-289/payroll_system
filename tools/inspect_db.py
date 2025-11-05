import sqlite3
import json
import os
from urllib.parse import urlparse

try:
    from config import DATABASE_URL
except Exception:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./payroll.db')


def sqlite_path_from_url(url: str) -> str:
    # support sqlite:///./file or sqlite:///C:/path/file
    if url.startswith('sqlite:'):
        # strip sqlite:/// or sqlite:///
        path = url.split('sqlite:///')[-1]
        # if windows drive like C:/... keep as is
        return os.path.abspath(path)
    return url


def inspect(db_path: str):
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return None

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = []
    cur.execute("SELECT name, type, sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name;")
    for row in cur.fetchall():
        tname = row['name']
        ttype = row['type']
        tsql = row['sql']
        # skip sqlite internal tables
        if tname.startswith('sqlite_'):
            continue
        # columns
        cur.execute(f"PRAGMA table_info('{tname}')")
        cols = [dict(r) for r in cur.fetchall()]
        # foreign keys
        cur.execute(f"PRAGMA foreign_key_list('{tname}')")
        fks = [dict(r) for r in cur.fetchall()]
        tables.append({
            'name': tname,
            'type': ttype,
            'create_sql': tsql,
            'columns': cols,
            'foreign_keys': fks,
        })

    result = {'db_path': db_path, 'tables': tables}
    outpath = os.path.join(os.path.dirname(__file__), 'db_schema.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print(f"Wrote schema report to: {outpath}")
    print(json.dumps({k: len(v) if k=='tables' else v for k,v in result.items() if k!='tables'}, indent=2))
    for t in tables:
        print('\nTABLE:', t['name'])
        print('  columns:')
        for c in t['columns']:
            print(f"    - {c['name']} ({c['type']}) notnull={c['notnull']} pk={c['pk']} dflt={c['dflt_value']}")
        if t['foreign_keys']:
            print('  foreign_keys:')
            for fk in t['foreign_keys']:
                print(f"    - from {fk.get('from')} -> {fk.get('table')}.{fk.get('to')} (on_update={fk.get('on_update')} on_delete={fk.get('on_delete')})")

    conn.close()
    return result


if __name__ == '__main__':
    db_path = sqlite_path_from_url(DATABASE_URL)
    print('Using DATABASE_URL =', DATABASE_URL)
    print('Resolved DB path =', db_path)
    inspect(db_path)
