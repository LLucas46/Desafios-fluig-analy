#!/usr/bin/env python3
"""Build the local dashboard demo and short Word hand-in from supplied CSVs."""
import csv
import json
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "model" / "Financeiro"
DATA = ROOT / "data" / "source" / "Financeiro"
OUT = HERE
REFERENCE = "20261002"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def make_dashboard():
    titles = read_csv("ContasAReceber.csv")
    dims = {"Filial": read_csv("Filial.csv"), "Coligada": read_csv("Coligada.csv"),
            "Especie": read_csv("Especie_Documento.csv"), "Cliente": read_csv("Cliente.csv")}
    for r in titles:
        r["VALOR_VENCIMENTO"] = float(r["VALOR_VENCIMENTO"] or 0)
        r["VALOR_RECEBIDO"] = float(r["VALOR_RECEBIDO"] or 0)
        r["SALDO_A_RECEBER"] = float(r["SALDO_A_RECEBER"] or 0)
    data = {"titles": titles, "dims": dims}
    tpl = (HERE / "dashboard.template.html").read_text(encoding="utf-8")
    html = tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    (OUT / "dashboard.html").write_text(html, encoding="utf-8")


def make_report():
    titles = read_csv("ContasAReceber.csv")
    paid_due = [r for r in titles if r["SITUACAO_DO_TITULO"] == "BAIXADO" and r["DATA_VENCIMENTO"].startswith("202609")]
    paid_clear = [r for r in titles if r["SITUACAO_DO_TITULO"] == "BAIXADO" and r["DATA_BAIXA"].startswith("202609")]
    opened = [r for r in titles if r["SITUACAO_DO_TITULO"] == "EM ABERTO"]
    late = [r for r in opened if r["DATA_VENCIMENTO"] < REFERENCE]
    current = [r for r in opened if r["DATA_VENCIMENTO"] >= REFERENCE]
    counts = [("ContasAReceber", len(titles))] + [(p[:-4], len(read_csv(p))) for p in
             ["Cliente.csv", "Filial.csv", "Coligada.csv", "Especie_Documento.csv", "Centro_Custo.csv"]]
    sumv = lambda rs, k: sum((Decimal(x[k] or "0") for x in rs), Decimal(0))
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Entrega — Painel de Recebimentos</title>
<style>@page{{size:A4;margin:16mm}}body{{font:10pt Arial;color:#26343b;line-height:1.4}}h1,h2{{color:#086f68}}h1{{font-size:22pt}}h2{{font-size:14pt;margin:22px 0 6px}}table{{border-collapse:collapse;width:100%;margin:8px 0 16px}}th,td{{border:1px solid #ccd6da;padding:6px;text-align:left}}th{{background:#eaf3f2}}.note{{background:#fff4d6;padding:10px;border-left:4px solid #d49a16}}.diagram{{border:1px solid #cbd6db;border-radius:8px;padding:10px;text-align:center;margin:12px 0}}.box{{display:inline-block;background:#eaf3f2;border:1px solid #0b8279;border-radius:6px;padding:10px;margin:5px}}code{{font-size:8pt}}.small{{font-size:9pt;color:#5c6d75}}.page{{page-break-before:always}}li{{margin:3px 0}}</style></head><body>
<h1>02. Financeiro — Painel de Recebimentos</h1><p>Resumo local de modelagem, métricas, validação e dashboard demonstrativo.</p>
<div class="note"><b>Limite das evidências:</b> este workspace não tem conexão com a instância TOTVS/GoodData. O dashboard e os diagramas deste pacote são artefatos locais preparatórios. Não representam deploy, carga executada, prints do ambiente ou validação remota.</div>
<h2>Modelo lógico local</h2><p>O modelo nativo CloudConnect está em model/model.ldm. Ele usa ContasAReceber como fato e Cliente, Filial, Coligada, Espécie do documento e Centro de custo como dimensões. Grão do fato: um título por linha. Unidade de negócio é atributo de Filial. O modelo inclui os papéis de data de emissão, vencimento e baixa, além da data auxiliar de extração.</p>
<div class="diagram"><span class="box">Cliente<br>PK_CLIENTE</span><span class="box">Filial<br>PK_FILIAL · Unidade de negócio</span><span class="box">Coligada<br>PK_COLIGADA</span><br><span class="box">Espécie do documento<br>PK_ESPECIE_DOCUMENTO</span><span class="box">Centro de custo<br>PK_CENTRO_CUSTO</span><br><b class="box">ContasAReceber (fato)<br>PK_TITULO · valores · situação · datas</b></div>
<h2>Carga CloudConnect — desenho preparatório</h2><p>Reader CSV (vírgula, aspas duplas, pular cabeçalho; chaves como texto; datas yyyyMMdd; decimal(15,2), locale en.US) → writer do dataset GoodData. Cada dimensão tem um graph; o graph principal executa dimensões antes do fato.</p><div class="diagram"><span class="box">Cliente</span><span class="box">Filial</span><span class="box">Coligada</span><span class="box">Espécie</span><span class="box">Centro de custo</span><br>↓ execução sequencial no _Main ↓<br><b class="box">ContasAReceber</b></div>
<p class="small">Este desenho não é export de projeto CloudConnect. O deploy, logs e contagens carregadas precisam ser obtidos no ambiente.</p>
<h2>Contagem de linhas nos arquivos de origem</h2><table><tr><th>CSV / dataset</th><th>Linhas</th></tr>{''.join(f'<tr><td>{n}</td><td>{c:,}</td></tr>' for n,c in counts)}</table>
<h2>Situações distintas</h2><p>BAIXADO, EM ABERTO e CANCELADO. Títulos CANCELADO são excluídos dos indicadores.</p>
<div class="page"></div><h2>Métricas MAQL — fórmulas conceituais</h2><p>Substitua os identificadores entre colchetes pelos elementos gerados no workspace e valide a sintaxe no editor MAQL.</p><table><tr><th>Métrica</th><th>Definição</th></tr>
<tr><td>$ Recebimento total</td><td><code>SELECT SUM([VALOR_VENCIMENTO]) WHERE [SITUACAO_DO_TITULO] &lt;&gt; "CANCELADO"</code></td></tr>
<tr><td>$ Recebido</td><td><code>SELECT SUM([VALOR_RECEBIDO]) WHERE [SITUACAO_DO_TITULO] = "BAIXADO"</code></td></tr>
<tr><td>$ A receber (s/ atraso)</td><td><code>SELECT SUM([SALDO_A_RECEBER]) WHERE [SITUACAO_DO_TITULO] = "EM ABERTO" AND [DATA_VENCIMENTO] &gt;= 2026-10-02</code></td></tr>
<tr><td>$ A receber (c/ atraso)</td><td><code>SELECT SUM([SALDO_A_RECEBER]) WHERE [SITUACAO_DO_TITULO] = "EM ABERTO" AND [DATA_VENCIMENTO] &lt; 2026-10-02</code></td></tr></table>
<p>Comparativos: mês anterior e ano anterior por Data de vencimento; variação = (atual − anterior) ÷ anterior. Aplicar o formato condicional indicado no enunciado às seis variações. O cartão sem atraso mostra “--” nos comparativos.</p>
<h2>Validação de referência — setembro/2026</h2><p>Os dois recortes possíveis de recebimento diferem porque a data de baixa não é igual à data de vencimento. Para conferir o gráfico por vencimento, use a primeira linha.</p>
<table><tr><th>Conferência CSV</th><th>Quantidade</th><th>Valor</th></tr><tr><td>Baixados com vencimento em setembro/2026</td><td>{len(paid_due)}</td><td>{brl(sumv(paid_due,'VALOR_RECEBIDO'))}</td></tr><tr><td>Baixados com baixa em setembro/2026</td><td>{len(paid_clear)}</td><td>{brl(sumv(paid_clear,'VALOR_RECEBIDO'))}</td></tr><tr><td>Em aberto vencidos em 02/10/2026</td><td>{len(late)}</td><td>{brl(sumv(late,'SALDO_A_RECEBER'))}</td></tr><tr><td>Em aberto vencendo em/ após 02/10/2026</td><td>{len(current)}</td><td>{brl(sumv(current,'SALDO_A_RECEBER'))}</td></tr></table>
<h2>Dashboard demonstrativo</h2><p>O arquivo model/Financeiro/dashboard.html mostra cartões e gráfico com interação local. Filtros e cálculos usam os CSVs fornecidos. A seleção “Todos” é inicial; setembro/2026 pode ser escolhido para conferência. A página não se conecta ao GoodData.</p>
<h2>Pendências para concluir na instância</h2><ul><li>Abrir e conferir model/model.ldm no Designer, publicar o LDM e confirmar os IDs de dataset usados pelos writers.</li><li>Revisar graphs no Designer, fazer deploy do projeto e executar _Main.</li><li>Registrar logs e contagens efetivamente carregadas.</li><li>Validar cada métrica MAQL no workspace, criar relatórios e publicar o dashboard TOTVS.</li><li>Capturar prints reais do LDM, graphs, dashboard/filtros e anexar evidências da execução.</li></ul>
<p class="small">Fonte de dados: RM_Backoffice_ficticio local. Data fixa para atraso: 02/10/2026. As contagens acima são dos CSVs de origem, não do GoodData.</p></body></html>'''
    (OUT / "Documento_de_Entrega.html").write_text(html, encoding="utf-8")
    make_docx(counts, paid_due, paid_clear, late, current, sumv)


def make_docx(counts, paid_due, paid_clear, late, current, sumv):
    """Write a small Word document using only the standard library."""
    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    ET.register_namespace("w", W)
    doc = ET.Element(f"{{{W}}}document")
    body = ET.SubElement(doc, f"{{{W}}}body")

    def para(text, style=None):
        p = ET.SubElement(body, f"{{{W}}}p")
        if style:
            ppr = ET.SubElement(p, f"{{{W}}}pPr")
            ET.SubElement(ppr, f"{{{W}}}pStyle", {f"{{{W}}}val": style})
        run = ET.SubElement(p, f"{{{W}}}r")
        t = ET.SubElement(run, f"{{{W}}}t")
        t.text = text

    def table(rows):
        tbl = ET.SubElement(body, f"{{{W}}}tbl")
        props = ET.SubElement(tbl, f"{{{W}}}tblPr")
        ET.SubElement(props, f"{{{W}}}tblW", {f"{{{W}}}w": "5000", f"{{{W}}}type": "pct"})
        for row in rows:
            tr = ET.SubElement(tbl, f"{{{W}}}tr")
            for value in row:
                tc = ET.SubElement(tr, f"{{{W}}}tc")
                p = ET.SubElement(tc, f"{{{W}}}p")
                r = ET.SubElement(p, f"{{{W}}}r")
                t = ET.SubElement(r, f"{{{W}}}t")
                t.text = str(value)

    para("02. Financeiro — Painel de Recebimentos", "Title")
    para("Resumo local de modelagem, métricas, validação e dashboard demonstrativo.")
    para("Limite das evidências: este workspace não tem conexão com a instância TOTVS/GoodData. O dashboard e os diagramas são artefatos locais preparatórios; não representam deploy, carga executada nem capturas do ambiente.")
    para("Modelo lógico local — model/model.ldm", "Heading1")
    para("O arquivo nativo do CloudConnect foi adaptado da atividade semelhante. Grão: um título por linha em ContasAReceber. Dimensões: Cliente (PK_CLIENTE), Filial (PK_FILIAL), Coligada (PK_COLIGADA), Espécie do documento (PK_ESPECIE_DOCUMENTO) e Centro de custo (PK_CENTRO_CUSTO). Filial também contém Unidade de negócio. Papéis de data: emissão, vencimento, baixa e extração auxiliar. O LDM ainda precisa ser aberto no Designer, conferido e publicado no workspace desta atividade.")
    para("Desenho: Cliente / Filial (+ Unidade de negócio) / Coligada / Espécie / Centro de custo → ContasAReceber (fato).")
    para("Carga CloudConnect — preparação", "Heading1")
    para("Um graph por dataset e um _Main que executa as dimensões antes do fato. Reader: vírgula, aspas duplas, cabeçalho ignorado, chaves string, datas yyyyMMdd e decimais(15,2) locale en.US. O desenho é conceitual, não export de CloudConnect.")
    para("Linhas nos arquivos de origem", "Heading1")
    table([("Dataset", "Linhas")] + [(n, f"{c:,}") for n, c in counts])
    para("Situações distintas: BAIXADO, EM ABERTO e CANCELADO. Cancelados excluídos dos indicadores.")
    para("Métricas MAQL conceituais", "Heading1")
    for name, formula in [
        ("$ Recebimento total", 'SUM(VALOR_VENCIMENTO) WHERE SITUACAO_DO_TITULO <> "CANCELADO"'),
        ("$ Recebido", 'SUM(VALOR_RECEBIDO) WHERE SITUACAO_DO_TITULO = "BAIXADO"'),
        ("$ A receber (s/ atraso)", 'SUM(SALDO_A_RECEBER) WHERE EM ABERTO AND DATA_VENCIMENTO >= 2026-10-02'),
        ("$ A receber (c/ atraso)", 'SUM(SALDO_A_RECEBER) WHERE EM ABERTO AND DATA_VENCIMENTO < 2026-10-02')]:
        para(f"{name}: SELECT {formula}")
    para("Para recebimento total, recebido e saldo em atraso: criar mês anterior, mês anterior [% Var], ano anterior e ano anterior [% Var]. Variação = (atual − anterior) ÷ anterior; anterior zero/vazio resulta em nulo (“--”). Usar Data de vencimento no comparativo. Aplicar o formato condicional do enunciado às seis variações. Substituir os identificadores e validar a sintaxe no editor MAQL.")
    para("Validação CSV — setembro/2026", "Heading1")
    table([("Conferência", "Títulos", "Valor")] + [
        ("Baixados por vencimento em setembro/2026", len(paid_due), brl(sumv(paid_due, "VALOR_RECEBIDO"))),
        ("Baixados por baixa em setembro/2026", len(paid_clear), brl(sumv(paid_clear, "VALOR_RECEBIDO"))),
        ("Em aberto vencidos em 02/10/2026", len(late), brl(sumv(late, "SALDO_A_RECEBER"))),
        ("Em aberto vencendo em/após 02/10/2026", len(current), brl(sumv(current, "SALDO_A_RECEBER")))])
    para("Os recortes de vencimento e baixa diferem. Para o gráfico por mês de vencimento, usar a primeira linha.")
    para("Dashboard e pendências", "Heading1")
    para("model/Financeiro/dashboard.html é um dashboard demonstrativo local com filtros e gráfico calculados dos CSVs. Não se conecta ao GoodData. Para concluir no ambiente: abrir, conferir e publicar model/model.ldm; revisar/deployar e executar os graphs; guardar logs/contagens reais; validar métricas e relatórios; publicar o dashboard e anexar capturas reais do LDM, graphs, filtros e carga.")
    para("Data fixa de referência para atraso: 02/10/2026. As contagens deste documento são dos arquivos de origem, não do GoodData.")
    ET.SubElement(body, f"{{{W}}}sectPr")
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
    with zipfile.ZipFile(OUT / "Documento_de_Entrega.docx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", ET.tostring(doc, encoding="utf-8", xml_declaration=True))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_dashboard()
    make_report()
    print(f"Gerados: {OUT / 'dashboard.html'} e {OUT / 'Documento_de_Entrega.docx'}")


if __name__ == "__main__":
    main()
