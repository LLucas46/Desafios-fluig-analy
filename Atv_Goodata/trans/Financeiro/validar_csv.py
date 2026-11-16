#!/usr/bin/env python3
"""Gera contagens e valores de referência para ContasAReceber.csv (stdlib only)."""
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_DIR = ROOT / "data" / "source" / "Financeiro"
FACT = CSV_DIR / "ContasAReceber.csv"
DIMENSIONS = ["Cliente.csv", "Filial.csv", "Coligada.csv", "Especie_Documento.csv", "Centro_Custo.csv"]
RELATIONSHIPS = [
    ("Cliente.csv", "PK_CLIENTE"),
    ("Filial.csv", "PK_FILIAL"),
    ("Coligada.csv", "PK_COLIGADA"),
    ("Especie_Documento.csv", "PK_ESPECIE_DOCUMENTO"),
    ("Centro_Custo.csv", "PK_CENTRO_CUSTO"),
]
REFERENCE = "20261002"


def load(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def money(rows, field):
    return sum((Decimal(row[field] or "0") for row in rows), Decimal("0"))


def brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    fact = load(FACT)
    if len(fact) != 5789 or len({row["PK_TITULO"] for row in fact}) != len(fact):
        raise SystemExit("Contagem ou unicidade da chave PK_TITULO não confere com o esperado.")
    print("Contagem esperada de carga:")
    for name in DIMENSIONS:
        print(f"  {name}: {len(load(CSV_DIR / name))}")
    print(f"  ContasAReceber.csv: {len(fact)}")
    for dimension, key in RELATIONSHIPS:
        known = {row[key] for row in load(CSV_DIR / dimension)}
        orphan_count = sum(row[key] not in known for row in fact)
        print(f"  Chave {key}: {orphan_count} fatos sem dimensão correspondente")
        if orphan_count:
            raise SystemExit(f"Há chaves órfãs em {dimension}.")

    from collections import Counter
    print("Situações:", dict(Counter(row["SITUACAO_DO_TITULO"] for row in fact)))

    paid_due_sep = [r for r in fact if r["SITUACAO_DO_TITULO"] == "BAIXADO" and r["DATA_VENCIMENTO"].startswith("202609")]
    paid_clear_sep = [r for r in fact if r["SITUACAO_DO_TITULO"] == "BAIXADO" and r["DATA_BAIXA"].startswith("202609")]
    opened = [r for r in fact if r["SITUACAO_DO_TITULO"] == "EM ABERTO"]
    late = [r for r in opened if r["DATA_VENCIMENTO"] < REFERENCE]
    future = [r for r in opened if r["DATA_VENCIMENTO"] >= REFERENCE]

    print("Referências:")
    print(f"  Recebido por vencimento em 09/2026: {len(paid_due_sep)} títulos, {brl(money(paid_due_sep, 'VALOR_RECEBIDO'))}")
    print(f"  Recebido por baixa em 09/2026: {len(paid_clear_sep)} títulos, {brl(money(paid_clear_sep, 'VALOR_RECEBIDO'))}")
    print(f"  Em aberto vencido em 02/10/2026: {len(late)} títulos, {brl(money(late, 'SALDO_A_RECEBER'))}")
    print(f"  Em aberto não vencido em 02/10/2026: {len(future)} títulos, {brl(money(future, 'SALDO_A_RECEBER'))}")


if __name__ == "__main__":
    main()
