# Analytics 2 — especificação de configuração

## Carga

`ldm.json` documenta colunas, chaves, relações, tipos e ordem de carga. Os artefatos da Atividade 2 foram separados nas pastas CloudConnect do projeto: dados em `../../../data/source/Financeiro`, sequência de graphs em `../../../graph/Financeiro`, metadados em `../../../meta/Financeiro`, LDM e dashboard demonstrativo em `../../../model/Financeiro`, métricas e utilitários em `../../../trans/Financeiro`. Crie os graphs nativos no Designer; o roteiro está em `../../../graph/Financeiro/README.md`.

### Contrato de execução no CloudConnect

Para cada dataset, configure o leitor CSV com saída em ordem idêntica à lista de colunas, sem conversão numérica das chaves, e conecte a saída ao writer do dataset publicado no LDM. Em `_Main`, execute as dimensões antes do fato; propague falhas. Faça deploy e execução no CloudConnect e confira contagens e erros. O JSON é um contrato de mapeamento, não um export nativo de graph CloudConnect.

## Regras dos indicadores

- Excluir `CANCELADO` do recebimento total.
- `BAIXADO` identifica recebimentos; somar `VALOR_RECEBIDO`.
- `EM ABERTO` identifica títulos em aberto; somar `SALDO_A_RECEBER`.
- Data de referência fixa: 02/10/2026. Sem atraso: vencimento maior ou igual à referência; com atraso: vencimento anterior.
- Os cartões de recebimento total, recebido e saldo em atraso têm comparativos mensal/anual. O saldo sem atraso é uma fotografia atual e mostra `--` nos comparativos.

## Comparativos

No GoodData Classic, a transformação temporal usa `FOR Previous(time_attribute[, períodos])`: um período anterior para Month/Year e doze períodos anteriores em Month/Year para o mesmo mês do ano anterior. A grafia exata do atributo temporal deve ser selecionada no editor após publicar o LDM. Para fórmula e semântica, consulte a documentação oficial: [FOR Previous](https://help.gooddata.com/classic/en/dashboards-and-insights/maql-analytical-query-language/maql-expression-reference/granularity-keywords/time-transformations/functions-for-referring-to-past-time-periods/for-previous/).

## Dashboard

Dashboard `02. Financeiro`, aba `Painel de Indicadores`. Filtros: Data de vencimento, Filial, Coligada, Unidade de negócio e Espécie do documento. Quatro cartões, cada um com valor atual; comparativos nos três cartões aplicáveis; legenda 1K/1M; abaixo, gráfico de colunas de `$ Recebido` por mês de vencimento. Manter os nomes e formatos definidos no PDF da atividade.

## Valores de controle calculados do CSV

- Linhas por situação: BAIXADO 5.102; EM ABERTO 521; CANCELADO 166.
- Recebido em títulos baixados com vencimento em setembro/2026: 114 títulos, R$ 1.065.128,35.
- Como a data de baixa pode ser diferente da data de vencimento, o recorte pela data de baixa em setembro resulta em 141 títulos e R$ 1.351.255,51. Para validar o gráfico pedido e o filtro de vencimento, usar vencimento como recorte; se validar pela data de baixa, registrar explicitamente esse papel de data.
- Fotografia em 02/10/2026: saldo em aberto vencido R$ 1.659.211,06; saldo com vencimento em 02/10/2026 ou depois R$ 2.720.900,40.

O catálogo conceitual de métricas está em `../../../trans/Financeiro/metricas.maql`: substitua marcadores usando o seletor do editor, configure datas pelo papel `Data de vencimento` e valide cada métrica no workspace. A sintaxe final depende dos identificadores publicados no projeto.

## Estado local e pendências no ambiente

Os CSVs e as regras são conferidos por `../../../trans/Financeiro/validar_csv.py`. Ainda precisam ser criados/publicados na instância: LDM, seis graphs e `_Main`, métricas e pasta, relatórios, filtros, dashboard e capturas reais. Não há integração da instância neste workspace; o pacote não registra execução remota como concluída.
