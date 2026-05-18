import requests

# BASE_URL = "https://pncp.gov.br/api/consulta/v1"
BASE_URL = "https://pncp.gov.br/api/pncp/v1"
BASE_URL_2 = "https://pncp.gov.br/api/consulta/v1"
SEARCH_URL = "https://pncp.gov.br/api/search"


class PNCPClient:
    """
    Class to get data from PNCP API
    """

    def __init__(self, timeout: int = 120):
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )
        self.session.timeout = timeout

    def _get(self, url: str, params=None):
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def get_contract(self, cnpj, year, sequencial):
        url = f"{BASE_URL_2}/orgaos/{cnpj}/compras/{year}/{sequencial}"
        return self._get(url)

    def list_actas(self, initial_data: str, final_date: str, page: int = 1):
        url = f"{BASE_URL_2}/atas"
        params = {"dataInicial": initial_data, "dataFinal": final_date, "pagina": page}
        return self._get(url, params=params)

    def search(
        self,
        query: str = "",
        page: int = 1,
        page_size: int = 100,
        status: str = "recebendo_proposta",
        **kwargs,
    ):

        params = {
            "q": query,
            "tipos_documento": "edital",
            "pagina": page,
            "ordenacao": "-data",
            "tam_pagina": page_size,
            "status": status,
        }
        params.update(kwargs)
        try:
            return self._get(SEARCH_URL + "/", params=params)
        except Exception as e:
            print(f"Error searching: {e}")
            return None

    def get_contract_itens(
        self, cnpj: str, year: int, sequencial: int, page: int = 1, page_size: int = 100
    ):
        url = f"{BASE_URL}/orgaos/{cnpj}/compras/{year}/{sequencial}/itens"
        params = {"pagina": page, "tam_pagina": page_size}
        return self._get(url, params=params)

    def close(self):
        self.session.close()


if __name__ == "__main__":
    item_buscado = "papel"
    estados = ["CE", "SP", "RJ"]
    modalidade = 8

    client = PNCPClient()
    result = client.search(
        query=item_buscado, ufs="|".join(estados), modalidades=modalidade
    )

    if result:
        print(f"Encontrados {result.get('total',0)} resultados")
    else:
        print("Nenhum resultado encontrado")

    propostas = result.get("items", [])
    print("Primeira proposta:")
    print(propostas[0].get("description"))
