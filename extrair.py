"""Extrai o recorte declarado da tabela 11 de Macko et al. (2023)."""
import csv
import hashlib
from pathlib import Path

from pypdf import PdfReader

dados = Path(__file__).resolve().parent / "dados"
pdf = dados / "multitude.pdf"
if hashlib.sha256(pdf.read_bytes()).hexdigest() != "21b718ec7f0f5fcd67fbec6009a27ba2620ef76e527637e14bdd14d8bcd1e691":
    raise ValueError("O PDF difere da edição registrada.")
linhas = PdfReader(pdf).pages[19].extract_text().splitlines()
idiomas = linhas[1].split()[3:]
if idiomas != "ar ca cs de en es nl pt ru uk zh".split():
    raise ValueError("Cabeçalho inesperado.")
geradores = "alpaca-lora-30b gpt-3.5-turbo gpt-4 llama-65b opt-66b opt-iml-max-1.3b text-davinci-003 vicuna-13b".split()
detectores = ("bert-base-multilingual-cased", "xlm-roberta-large")
registros = {}
gerador = None
for linha in linhas[2:]:
    if linha.startswith("All Detectors Mean"):
        break
    if linha.strip() in geradores:
        gerador = linha.strip()
        continue
    campos = linha.split()
    if campos and campos[0] in detectores:
        chave = (gerador, campos[0])
        if chave in registros or len(campos) != 1 + len(idiomas):
            raise ValueError(f"Linha inválida: {linha}")
        valor = campos[1 + idiomas.index("pt")]
        if not 0 <= float(valor) <= 1:
            raise ValueError(f"Macro-F1 inválido: {valor}")
        registros[chave] = valor
if set(registros) != {(g, d) for g in geradores for d in detectores}:
    raise ValueError("Pares incompletos ou gerador inesperado.")
with (dados / "resultados_pt.csv").open("w", encoding="utf-8", newline="") as arquivo:
    saida = csv.writer(arquivo)
    saida.writerow(["gerador", "detector", "idioma_treino", "idioma_teste", "macro_f1"])
    for (g, d), valor in registros.items():
        saida.writerow([g, d, "en", "pt", valor])
print(f"{len(registros)} registros extraídos.")
