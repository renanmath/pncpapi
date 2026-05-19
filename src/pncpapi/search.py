from pncpapi.client import PNCPClient


class PNCPSearch:
    """
    Classe para realizar buscas e consultas elaboradas no PNCP
    """

    def __init__(self):
        self.client = PNCPClient()

    def get_all_results(
        self,
        method: str = "search",
        query: str = "",
        cnpj: str = None,
        year: int = None,
        sequencial: int = None,
        page_size: int = 100,
        verbose: bool = False,
        **kwargs,
    ):

        all_results = []
        total = float("inf")
        current_page = 1

        while len(all_results) < total:
            if verbose:
                print(f"Fetching page {current_page}")
            if method == "search":
                result = self.client.search(query=query, page=current_page, **kwargs)
                
                if not result:
                    break

                partial_results = result["items"]
                total = result.get("total", 0)
            elif method == "items":
                result = self.client.get_contract_itens(
                    cnpj=cnpj,
                    year=year,
                    sequencial=sequencial,
                    page=current_page,
                    page_size=page_size,
                    **kwargs,
                )
                partial_results = result

            if not partial_results:
                break

            all_results.extend(partial_results)
            current_page += 1

        return all_results

    def search(
        self,
        query: str = "",
        page_size: int = 100,
        status: str = "recebendo_proposta",
        verbose: bool = False,
        **kwargs,
    ) -> list[dict]:
        """
        Realiza uma busca no PNCP
        """

        return self.get_all_results(
            method="search", query=query, page_size=page_size, status=status, **kwargs
        )

    def list_itens(self, cnpj: str, year: int, sequencial: int, page_size: int = 100, verbose: bool = False):
        """
        Lista os itens de um contrato
        """
        return self.get_all_results(
            method="items",
            cnpj=cnpj,
            year=year,
            sequencial=sequencial,
            page_size=page_size,
            verbose=verbose
        )
        


if __name__ == "__main__":

    item_buscado = "informatica"
    estados = ["CE", "SP", "RJ"]
    modalidade = 8

    buscador = PNCPSearch()
    results = buscador.search(
        query=item_buscado, ufs="|".join(estados), modalidades=modalidade,verbose=True
    )
    print(f"Encontradas {len(results)} propostas")
    proposta = results[0]
    cnpj = proposta["orgao_cnpj"]
    ano = proposta["ano"]
    sequencial = proposta["numero_sequencial"]
    itens = buscador.list_itens(
        cnpj=cnpj, year=ano, sequencial=sequencial, page_size=100, verbose=True
    )
    print(f"Encontrados {len(itens)} items na primeira proposta")
