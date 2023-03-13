import csv


def ler_dados_csv(arquivo_csv):
    dados = []
    try:
        with open(arquivo_csv, newline='', encoding='utf-8') as arquivo_massa:
            leitor_csv = csv.DictReader(arquivo_massa, delimiter='-')
            for linha in leitor_csv:
                dados.append(linha)
        return dados
    except FileNotFoundError:
        print(f'Arquivo não encontrado: {arquivo_csv}')
        return None
    except Exception as e:
        print(f'Ocorreu uma falha na leitura do arquivo {arquivo_csv}: {str(e)}')
        return None
    finally:
        if 'arquivo_massa' in locals():
            arquivo_massa.close()
