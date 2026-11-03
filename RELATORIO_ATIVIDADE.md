# Atividade prática — Desenvolvimento de software com IA

## Identificação
Disciplina: ____________________________________
Aluno(a): ______________________________________
Turma: _________________________________________
Data: ____/____/________

## 1. Tema e problema
O TaskFlow é um gerenciador de tarefas desenvolvido para apoiar a organização de atividades pessoais. O problema abordado é a dificuldade de registrar tarefas, acompanhar prazos e identificar atividades pendentes ou concluídas em um único ambiente.

## 2. Objetivo
Construir uma aplicação web simples com operações CRUD, validação de dados, persistência, interface responsiva e documentação, utilizando IA como apoio ao desenvolvimento.

## 3. Requisitos implementados
- Interface web navegável e responsiva.
- Cadastro, listagem, consulta, edição e exclusão de tarefas.
- Prioridade, prazo e status.
- Validação no servidor e constraints no banco.
- Persistência SQLite.
- Mensagens de sucesso e erro.
- README com instalação, execução e testes.

## 4. Tecnologias
Python, Flask, SQLite, HTML, CSS, Jinja2 e Pytest.

## 5. Aplicação dos quatro prompts
### Prompt 4 — Auditoria completa
Foi elaborado `AUDITORIA.md` com achados por etapa, classificação de risco, arquivo e recomendação. A análise identificou como principais pendências a ausência de autenticação/autorização e de proteção CSRF.

### Prompt 1 — Auditoria de segurança
A revisão identificou validação no servidor, SQL parametrizado e ausência de segredos de terceiros no front. Também registrou as pendências de CSRF, autenticação e segredo de produção. Correções de segurança devem ser aprovadas e aplicadas antes de uso público.

### Prompt 3 — Testes de integração
Foram preparados testes que chamam rotas reais e utilizam SQLite temporário real. Os cenários cobrem cadastro, edição, exclusão, conclusão, filtros, entradas inválidas e IDs inexistentes. Registrar abaixo o resultado obtido ao executar `pytest -q`:
**Resultado real:** ______________________________________________

### Prompt 2 — Refatoração segura
A estrutura separa rotas (`app.py`), regras (`services/task_service.py`), persistência (`repository.py`), interface (`templates/` e `static/`). Essa separação foi adotada desde o início para reduzir dependências cruzadas. Não foi feita refatoração posterior que alterasse comportamento.

## 6. Validação manual
Preencher após executar:
- Cadastro: ____________________________________
- Listagem/consulta: ____________________________
- Edição: ______________________________________
- Exclusão: ____________________________________
- Entrada inválida: _____________________________
- Responsividade: ______________________________

## 7. Publicação
Repositório GitHub: [PREENCHER]
URL do sistema publicado: [PREENCHER]
As URLs só devem ser informadas após publicação real.

## 8. Evidências
Anexar:
1. Captura da tela inicial.
2. Captura do formulário de cadastro.
3. Captura de tarefa cadastrada.
4. Captura de validação de entrada inválida.
5. Saída do terminal com `pytest -q`.
6. Página do repositório GitHub.
7. Sistema acessível pela URL do deploy.

## 9. Reflexão
A IA pode acelerar a criação da estrutura e sugerir código, mas o resultado precisa ser revisado, executado e testado. A análise também mostrou que uma aplicação funcional não é necessariamente segura para publicação: autenticação, autorização, CSRF e configuração de produção precisam ser avaliadas conforme o contexto.
