# Plano de testes de integração

Os testes chamam as rotas reais da aplicação Flask e usam SQLite temporário real. Não há mock do banco nem da regra de negócio. Serviços externos não são utilizados neste projeto.

## Cenários (formato describe / it)
- Cadastro: quando os dados obrigatórios são válidos, então a tarefa é persistida e aparece na listagem.
- Cadastro inválido: quando o título está vazio ou excede 120 caracteres, então o servidor rejeita a requisição.
- Prioridade inválida: quando é enviada uma prioridade fora da lista permitida, então o servidor rejeita a requisição.
- Edição: quando uma tarefa existente é alterada, então os novos dados aparecem na listagem.
- Exclusão: quando uma tarefa existente é excluída, então ela deixa de aparecer.
- Conclusão: quando o usuário aciona concluir, então o status passa para Concluída; ao reabrir, volta para Pendente.
- Recurso inexistente: quando se consulta/edita/exclui um ID inexistente, então a aplicação responde 404.
- Filtro: quando se seleciona um status, então apenas tarefas daquele status são exibidas.

## Repetição, concorrência e limites
- Repetição de exclusão: a segunda exclusão deve resultar em 404.
- Duplo clique em concluir: duas requisições sequenciais alternam o status; a interface deve evitar disparos acidentais. Não existe operação financeira ou recurso limitado.
- Concorrência de criação: IDs são gerados pelo SQLite; não há identificador de negócio único exigido.
- Limites: título vazio, título acima de 120 caracteres, descrição acima de 1.000, prioridade inválida e data inválida.
- Acesso indevido: não aplicável a usuários distintos porque a versão não implementa contas. Isso é uma limitação de escopo, não uma garantia de isolamento.

## Ambiente
`pytest -q`. O fixture cria banco separado em diretório temporário para cada teste. Nunca configure o teste para apontar ao banco de produção.

## Resultado
Execute localmente e registre a saída verdadeira. O pacote contém testes automatizados, mas a execução final deve ser feita no ambiente de entrega.
