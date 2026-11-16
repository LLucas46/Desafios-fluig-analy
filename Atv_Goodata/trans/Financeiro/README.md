# Métricas e utilitários — Financeiro

- `metricas.maql`: catálogo conceitual com quatro métricas base e os comparativos requeridos. Substituir elementos pelos identificadores do workspace e validar no editor; não é um script de importação direta.
- `validar_csv.py`: conta linhas, valida integridade de chaves e calcula referências nos arquivos de `data/source/Financeiro`.
- `gerar_entrega.py`: regenera o dashboard local e o documento DOCX a partir dos CSVs e do template em `model/Financeiro`.

Na raiz do projeto, execute os scripts com Python 3. A demonstração não substitui a execução/deploy dos graphs no CloudConnect.
