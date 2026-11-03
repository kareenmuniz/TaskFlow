# Auditoria de qualidade e segurança — TaskFlow

> Auditoria estática inicial do código entregue. Não representa certificação de segurança nem substitui execução no ambiente final. Itens dependentes de deploy/infraestrutura estão marcados como não verificados.

## 5 achados prioritários
1. **Alto — ausência de autenticação/autorização:** qualquer visitante pode visualizar, alterar e excluir tarefas. Adequado apenas a demonstração local individual; inadequado para dados compartilhados.
2. **Alto — ausência de proteção CSRF:** formulários POST não possuem token CSRF.
3. **Médio — SECRET_KEY de desenvolvimento:** existe fallback conhecido em `config.py`; deve ser substituído por variável de ambiente forte em produção.
4. **Médio — configuração de debug:** execução direta está com `debug=False`, mas a configuração de servidor deve ser validada no deploy.
5. **Baixo — cobertura de concorrência limitada:** CRUD básico é testado, mas não há teste concorrente específico; o sistema não possui estoque/saldo/cupom ou outro recurso limitado.

## Etapa 1 — Testes de integração
| Achado | Risco | Arquivo/linha | Correção sugerida |
|---|---|---|---|
| Pytest configurado | Baixo | `requirements.txt`, `tests/` | Manter comando `pytest -q` |
| Banco de teste temporário por fixture | Baixo | `tests/conftest.py` | Preservar isolamento; nunca apontar para produção |
| Cobertura de CRUD, validações, filtro e 404 | Médio | `tests/test_tasks_integration.py` | Expandir com limites de comprimento e concorrência |
| Execução dos testes neste relatório | Médio | Não verificado | Executar `pytest -q` no ambiente local e anexar saída real |

## Etapa 2 — Confiança no cliente
| Achado | Risco | Arquivo/linha | Correção sugerida |
|---|---|---|---|
| Validação de título, descrição, prioridade e data no servidor | Baixo | `services/task_service.py` | Manter validação no serviço; constraints no SQLite |
| SQL parametrizado | Baixo | `repository.py` | Manter parâmetros em todas as consultas |
| Nenhuma chave de API de terceiros no front | Baixo | `static/`, `templates/` | Reavaliar caso integrações sejam adicionadas |
| SECRET_KEY com fallback de desenvolvimento | Médio | `config.py` | Falhar em produção se variável não estiver configurada |
| Sem Supabase ou banco exposto por API | Baixo | Projeto | RLS/policies não se aplicam ao SQLite local |
| Sem autenticação/autorização | Alto | `app.py` | Adicionar login, sessão segura e autorização por proprietário antes de uso multiusuário |
| Sem CSRF | Alto | `templates/`, `app.py` | Adicionar proteção CSRF nos formulários POST |
| Segredos publicados no front | Não identificado | `static/`, `templates/` | Não foram encontrados tokens de serviços externos no código fornecido |

## Etapa 3 — Race condition
| Achado | Risco | Arquivo/linha | Correção sugerida |
|---|---|---|---|
| Não há estoque, cupom, saldo, crédito ou vaga | Baixo | Escopo funcional | Não aplicável ao domínio atual |
| Escritas de tarefas usam SQLite e commits por conexão | Baixo | `repository.py` | Para futuras regras de limite, usar transação e constraint no banco |
| Lock em memória/Redis | Não identificado | Projeto | Não utilizado |
| Concorrência de múltiplas instâncias em deploy | Médio | `render.yaml` | Validar armazenamento persistente e estratégia de banco antes de escalar |

## Etapa 4 — Idempotência
| Achado | Risco | Arquivo/linha | Correção sugerida |
|---|---|---|---|
| Não existem webhooks | Baixo | Projeto | Não aplicável |
| Não há gateway de pagamento | Baixo | Projeto | Não aplicável |
| POST de criação não é idempotente | Baixo | `app.py`, `repository.py` | Se houver criação por integração, adicionar chave idempotente única |

## Etapa 5 — Separação de responsabilidades
| Achado | Risco | Arquivo/linha | Correção sugerida |
|---|---|---|---|
| Rotas e composição HTTP | Baixo | `app.py` | Manter apenas camada de apresentação |
| Regras de validação e status | Baixo | `services/task_service.py` | Manter no serviço |
| Persistência SQL | Baixo | `repository.py` | Manter no repositório |
| Estrutura modular já separa responsabilidades | Baixo | Raiz, `services/`, `templates/`, `static/` | Evoluir sem adicionar dependências desnecessárias |

## Limitações e itens não verificados
- Não foi fornecido ambiente de produção, credencial ou URL de deploy; infraestrutura, HTTPS, headers e variáveis reais não foram verificados.
- A execução real dos testes deve ser registrada pelo aluno com a saída do terminal.
- Não há autenticação, multiusuário, API externa, pagamentos, webhooks ou banco Supabase neste escopo.
- O relatório é referente ao código deste pacote, não a um repositório externo que não foi fornecido.

## Ordem recomendada dos prompts
1. **Prompt 1 — Auditoria de segurança:** tratar primeiro CSRF, autenticação/autorização e configuração de segredo antes de exposição pública.
2. Prompt 3 — Testes de integração: ampliar a cobertura após aprovar cenários.
3. Prompt 2 — Refatoração segura: a estrutura já está separada; refatorar apenas se a evolução justificar.
4. Prompt 4 — Auditoria completa: repetir após correções para comparar o estado final.

A auditoria inicial foi realizada sem alterar o código durante a análise. As correções de segurança indicadas são pendências explícitas, não devem ser consideradas implementadas.
