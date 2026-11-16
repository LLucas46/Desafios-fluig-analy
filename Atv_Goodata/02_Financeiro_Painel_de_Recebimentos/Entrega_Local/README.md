# Entrega local — Fluig 2 e Analytics 2

Este pacote contém os fontes e as evidências que podem ser preparados fora dos ambientes TOTVS. Não é um export nativo de um workspace GoodData nem um pacote publicável de Fluig: a instância de treinamento, os IDs de estado do workflow e as permissões de publicação não estão disponíveis neste workspace.

## Conteúdo

- `fluig/`: formulário responsivo com tabela pai-filho, máscara e ligação de pesquisa configurável; blueprint para montar/publicar o processo no Fluig Studio.
- `analytics/`: mapeamento LDM, rascunho de métricas MAQL, especificação de carga e roteiro do dashboard.
- `validacao/`: validação original da atividade anterior, se aplicável.

Os materiais específicos da Atividade 2 foram organizados no projeto CloudConnect nas pastas de raiz: `data/source/Financeiro`, `graph/Financeiro`, `meta/Financeiro`, `model/Financeiro` e `trans/Financeiro`.

## Próximos passos no ambiente TOTVS

1. Importar/ajustar o formulário na aplicação Fluig e substituir o dataset de laboratório pelo dataset selecionado na Atividade 4.
2. Criar o workflow no Studio usando `fluig/workflow/blueprint.md`, configurar grupos e códigos reais das atividades/estados e publicar.
3. Criar os graphs CloudConnect para os dados em `data/source/Financeiro`, configurar metadados em `meta/Financeiro`, modelar/publicar o LDM e validar métricas usando os materiais em `model/Financeiro` e `trans/Financeiro`.
4. Fazer deploy e execução pelo ambiente TOTVS, registrar logs e capturas reais e testar os filtros.
