# Fluxos CloudConnect — Financeiro

Os graphs foram adaptados da atividade semelhante em `/home/llucas/Downloads/Financeiro — Painel de Indicadores/graph/`. Foram reaproveitados os fluxos de dimensão para Filial, Coligada, Centro de custo e Espécie do documento; o graph de Fornecedor virou modelo para Cliente, e Contas a Pagar virou modelo para Contas a Receber. O `_Main.grf` foi ajustado para chamar os seis datasets desta atividade.

## Arquivos e carga

Cada graph unitário lê seu CSV em `data/source/Financeiro/`, ignora o cabeçalho e envia os registros ao writer GoodData correspondente:

- `Cliente.grf` → dataset Cliente.
- `Filial.grf` → dataset Filial, que também contém Unidade de negócio.
- `Coligada.grf` → dataset Coligada.
- `Especie_Documento.grf` → dataset Especie_Documento.
- `Centro_Custo.grf` → dataset Centro_Custo.
- `ContasAReceber.grf` → fato ContasAReceber.
- `_Main.grf` executa Cliente, Filial, Coligada, Especie_Documento, Centro_Custo e ContasAReceber, nessa ordem.

Os metadados de cada reader seguem a ordem das colunas dos CSVs, usam texto para chaves/códigos, datas `yyyyMMdd`, decimais com comprimento 15 e escala 2, locale `en.US`, e deixam a data de baixa vazia como nula. As definições detalhadas estão em `meta/Financeiro/csv_reader_metadata.json`.

## Ajustes feitos ao material de referência

- Os caminhos de entrada usam `${DATA_SOURCE_DIR}/Financeiro/` e apontam para os CSVs desta atividade.
- Os campos e mapeamentos GoodData foram ajustados para Cliente e ContasAReceber.
- Não foram copiados o `workspace.prm` nem o `model/model.ldm` da atividade de referência, pois pertencem a outro projeto GoodData e a outro modelo.

## Verificação no Designer

Os arquivos passaram por checagem XML, ordem/tipo dos campos, caminhos de CSV, correspondência de campos do writer e sequência do `_Main`. Ainda é necessário abrir os graphs no CloudConnect Designer, confirmar os IDs de dataset após publicar o LDM desta atividade, executar e comparar as contagens do log com os valores em `meta/Financeiro/csv_reader_metadata.json`.
