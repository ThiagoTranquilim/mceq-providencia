# Detecção de textos gerados por IA em português

Marco 2 de MCEQ, PUC-Campinas. O protocolo e o dicionário estão no documento Ficha de Proveniência.docx.

## Fonte

Macko et al. (2023). MULTITuDE: Large-Scale Multilingual Machine-Generated Text Detection Benchmark. EMNLP, apêndice E, tabela 11, p. 9979. DOI https://doi.org/10.18653/v1/2023.emnlp-main.616. Acesso em 08/11/2026. PDF original sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). O CSV é uma seleção e reorganização da tabela.

## Reproduzir a extração

Na pasta do repositório, com Python 3, execute:

    python -m pip install pypdf==6.21.4
    python extrair.py

O arquivo dados/multitude.pdf é a entrada original. Para recuperá-lo, baixe https://aclanthology.org/2023.emnlp-main.616.pdf nesse caminho. O script confere o SHA-256 antes de ler a tabela. A saída dados/resultados_pt.csv contém 16 linhas de dados, duas para cada gerador, em UTF-8 e com ponto decimal. Para comparar uma nova execução com a versão registrada, use git diff -- dados/resultados_pt.csv.
