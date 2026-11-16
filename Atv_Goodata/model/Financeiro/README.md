# Modelo e entregáveis locais — Financeiro

- `../model.ldm`: modelo lógico nativo do CloudConnect, adaptado da atividade semelhante para o fato ContasAReceber. Os datasets e campos foram verificados contra os mapeamentos dos writers locais.
- `ldm.json`: contrato JSON auxiliar com colunas, relacionamentos, chaves e metadados de origem; não substitui o arquivo nativo.
- `dashboard.html`: demonstração local interativa, calculada com os CSVs; não publicada nem conectada ao GoodData.
- `Documento_de_Entrega.docx` e `.html`: documento local preparatório com contagens de origem e validação calculada nos CSVs. Não contém capturas/logs reais do CloudConnect.
- `dashboard.template.html`: fonte HTML da demonstração.

Abrir `model/model.ldm` no Designer e conferir os datasets, chaves, relacionamentos e papéis de data. Publicar o LDM no GoodData antes de executar os writers; confirmar que os IDs do modelo coincidem com os mapeamentos nos `.grf`. Depois validar MAQL, criar relatórios e dashboard com os filtros do enunciado. Substituir as evidências preparatórias pelas capturas reais do ambiente.
