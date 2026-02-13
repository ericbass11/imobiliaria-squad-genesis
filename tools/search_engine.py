from duckduckgo_search import DDGS

def search_market(query, max_results=5):
    """
    Realiza uma busca no DuckDuckGo e retorna os resultados.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        print(f"Erro na busca: {e}")
        return []
