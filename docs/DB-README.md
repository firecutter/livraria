# Banco de Dados — Django + SQLite

Este documento explica passo a passo como entender, visualizar e administrar o banco de dados deste projeto (Django + SQLite).

## 1. Onde está o banco

O arquivo do banco local é `db.sqlite3` na raiz do projeto.

## 2. Comandos básicos

Ative seu virtualenv e rode os comandos abaixo no PowerShell:

```powershell
# Ativar virtualenv
.\.venv\Scripts\Activate.ps1

# Instalar dependências úteis
pip install django-extensions pydotplus

# (No Windows) instale Graphviz manualmente e adicione ao PATH: https://graphviz.org/download/

# Mostrar migrações
python manage.py showmigrations

# Gerar migrações (se alterar models)
python manage.py makemigrations
python manage.py migrate

# Acessar shell (ORM)
python manage.py shell
# Exemplo:
# from catalog.models import Book, Loan
# Book.objects.count()
# exit()

# Executar testes
python manage.py test
```

## 3. Gerar diagrama ER (Django Extensions + Graphviz)

1. Instale dependências:
```powershell
pip install django-extensions pydotplus
```

2. Adicione `django_extensions` em `library/settings.py` (já foi adicionado neste repositório).

3. Gere o diagrama:
```powershell
python manage.py graph_models catalog -o docs/diagrama_catalog.png
```

Opções:
- `-a`: todos os apps
- `-g`: agrupar modelos por app
- `-o`: arquivo de saída (png, svg)

## 4. Visualizar e editar dados

Recomendado: DB Browser for SQLite
- Abra `db.sqlite3`
- Consulte tabelas e execute SQL

Alternativa: DBeaver ou extensão SQLite no VS Code.

## 5. Backup e restore

Backup:
```powershell
copy db.sqlite3 db_backup_YYYYMMDD.sqlite3
```
Restore: substituir arquivo `db.sqlite3` e reiniciar o projeto.

## 6. Trocar para PostgreSQL (resumo)

1. Instalar driver:
```powershell
pip install psycopg2-binary
```
2. Atualizar `library/settings.py` com credenciais Postgres.
3. Rodar `python manage.py migrate`.

## 7. Exportar dados (fixture)

```powershell
python manage.py dumpdata catalog > docs/catalog_fixture.json
```

---

Se quiser, eu executo os passos: instalar dependências, gerar diagrama e exportar fixture. Deseja que eu rode tudo agora?
