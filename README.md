# caged_action
# https://www.gov.br/trabalho-e-previdencia/pt-br/servicos/empregador/caged
"O Cadastro Geral de Empregados e Desempregados (CAGED) foi criado como registro permanente de admissões e dispensa de empregados, sob o regime da Consolidação das Leis do Trabalho (CLT). É utilizado pelo Programa de Seguro-Desemprego, para conferir os dados referentes aos vínculos trabalhistas, além de outros programas sociais.
”

## Este action faz:
- scrap da tabela.xlxs disponibilizada, 
- extrai 5 tabelas e gera um csv para cada uma 
- leva pro bucket criado na AWS para posterior analise.

## Este scrap pode ser executado por demanda ou agendamento.
## As tabelas são extraidas e copiadas individualmente.

Referências:
- https://www.automat-it.com/post/using-github-actions-with-aws-iam-roles
- https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions
