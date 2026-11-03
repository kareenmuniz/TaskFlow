# TaskFlow — Gerenciador de Tarefas

Aplicação web acadêmica para organizar atividades pessoais. Permite cadastrar, consultar, editar, excluir, filtrar e concluir tarefas.

## Tecnologias
- Python 3.11+
- Flask
- SQLite
- HTML5, CSS3 e Jinja2
- Pytest

## Funcionalidades
- CRUD completo de tarefas.
- Campos: título, descrição, prioridade, prazo e status.
- Validação de título, limites de caracteres, prioridade e data.
- Filtro por status e resumo de tarefas pendentes/concluídas.
- Interface responsiva.

## Executar localmente
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
# opcional: copie .env.example para .env e configure as variáveis
python app.py
```
Acesse http://127.0.0.1:5000.

## Testes
```bash
pytest -q
```
Os testes usam um arquivo SQLite temporário criado pelo pytest. Não apontam para o banco de produção.

## Estrutura
```text
TaskFlow/
├── app.py
├── config.py
├── repository.py
├── services/task_service.py
├── templates/
├── static/style.css
├── tests/
├── AUDITORIA.md
├── PLANO_TESTES.md
└── README.md
```

## Segurança e limitações
- Validações são repetidas no serviço do servidor e reforçadas por constraints SQLite.
- Consultas SQL usam parâmetros.
- O banco é local/SQLite; não há autenticação multiusuário. Não use para armazenar dados sensíveis ou expor instâncias compartilhadas sem adicionar autenticação e autorização.
- O SECRET_KEY padrão serve apenas para desenvolvimento. Em produção, configure variável de ambiente forte.
- A proteção CSRF não está habilitada nesta versão didática; antes de uso público, adicionar Flask-WTF/CSRF ou mecanismo equivalente e revisar cookies/HTTPS.
- Para hospedagem no Render, o disco persistente está configurado no render.yaml. Verifique as condições atuais do plano gratuito antes de publicar.

## Publicação no GitHub
1. Crie um repositório chamado `taskflow-gerenciador-tarefas`.
2. No terminal, na pasta do projeto:
```bash
git init
git add .
git commit -m "Entrega inicial do TaskFlow"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/taskflow-gerenciador-tarefas.git
git push -u origin main
```
3. Substitua `SEU-USUARIO` pelo seu usuário. Não publique `.env`, senhas ou tokens.

## Deploy
1. Crie uma conta no Render e conecte o repositório GitHub.
2. Selecione o arquivo `render.yaml` (Blueprint) ou configure serviço Web Python.
3. Confirme `pip install -r requirements.txt` e `gunicorn app:create_app()`.
4. Configure `SECRET_KEY` como segredo forte e habilite disco persistente em `/var/data`.
5. Após deploy, teste cadastro, edição, conclusão e exclusão no endereço gerado.
6. Cole a URL real do deploy aqui: **[PREENCHER APÓS PUBLICAÇÃO]**.

## Evidências para a atividade
Inclua capturas reais da aplicação, saída real de `pytest -q`, URL do GitHub e URL do deploy. Não declare publicação ou testes executados sem realizar essas ações.
