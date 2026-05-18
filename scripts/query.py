from pncpapi.client import PNCPClient

if __name__ == "__main__":
    # Exemplo de uso da API
    # Consultar a primeira página de uma pesquisa e procurar pelos itens correspondentes

    item_buscado = "papel"
    estados = ["CE", "SP", "RJ"]
    modalidade = 8

    cliente = PNCPClient()
    resultado = cliente.search(
        query=item_buscado, ufs="|".join(estados), modalidades=modalidade
    )

    if resultado:
        print(f"Encontrados {resultado.get('total',0)} resultados")
    else:
        print("Nenhum resultado encontrado")

    propostas = resultado.get("items", [])
    proposta = propostas[0]
    print("Primeira proposta:")
    print(proposta.get("description"))

    cnpj = proposta.get("orgao_cnpj")
    sequencial = proposta.get("numero_sequencial")
    ano = proposta.get("ano")
    itens_da_proposta = cliente.get_contract_itens(
        cnpj=cnpj, sequencial=sequencial, year=ano
    )
    print(f"Proposta com {len(itens_da_proposta)} itens")

    print(f"Busca finalizada")
