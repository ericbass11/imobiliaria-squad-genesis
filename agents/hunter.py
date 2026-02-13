import json
import os
import datetime
from openai import OpenAI
from tools.search_engine import search_market

class HunterAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, city):
        print(f"Hunter Agent initiated for High-End Lots in {city}...")
        
        # 0. Load Knowledge Base (Frameworks)
        try:
            with open("knowledge_base/tecnica_imobiliaria.txt", "r", encoding="utf-8") as f:
                framework_tech = f.read()
            with open("knowledge_base/framework_benchmarking.txt", "r", encoding="utf-8") as f:
                framework_bench = f.read()
        except FileNotFoundError:
            print("Warning: Framework files not found. Using default logic.")
            framework_tech = "Critérios técnicos padrão."
            framework_bench = "Benchmark padrão."
        
        # 1. Search for top real estate agencies & Developers
        print("Scouting Developers & Agencies (ETL Source 1)...")
        agencies = search_market(f"Incorporadoras alto padrão {city} histórico obras")
        
        # 2. Search for Technical Specs of Listings
        print("Extracting Technical Data from Listings (ETL Source 2)...")
        # Queries focused on extracting hard data: Price/m2, amenities, infrastructure
        developments = search_market(f"Ficha técnica condomínio fechado {city} lotes m2 valor condomínio")
        
        # 3. Search for Cross-Industry Benchmarks (Experience)
        print("Analyzing Benchmarks (Competitors & Non-Competitors)...")
        benchmarks = search_market(f"Melhores experiências serviço luxo {city} reviews")

        # 4. Analyze with LLM (ETL Processor)
        print("Processing Data with LLM (Data Analyst Mode)...")
        prompt = f"""
        Execute uma análise de ETL (Extração, Transformação e Carga) sobre os dados do mercado de LOTES DE ALTO PADRÃO em {city}.
        
        ATENÇÃO: Você não é um marketeiro. Você é um ANALISTA DE DADOS IMOBILIÁRIOS.
        Sua missão é estruturar os dados desorganizados da web em inteligência pura.
        
        Use os seguintes Frameworks como critério de filtragem e qualidade:
        1. FRAMEWORK TÉCNICO: {framework_tech}
        2. FRAMEWORK BENCHMARKING: {framework_bench}

        DADOS BRUTOS:
        FONTES 1 (Incorp/Imob): {json.dumps(agencies, ensure_ascii=False)}
        FONTES 2 (Lotes/Fichas Téc): {json.dumps(developments, ensure_ascii=False)}
        FONTES 3 (Experiência/Benchmark): {json.dumps(benchmarks, ensure_ascii=False)}
        
        TAREFA DE EXTRAÇÃO:
        1. Identifique Players Reais (filtre ruído).
        2. Extraia Dados Quantitativos: Preço/m² Médio, Tamanho Médio dos Lotes, Valor do Condomínio.
        3. Identifique "Best Practices" (O que eles fazem de excepcional no atendimento/serviço?).

        Saída APENAS em JSON válido com a seguinte estrutura (em Português do Brasil):
        {{
            "market_players": [
                {{"name": "Nome", "type": "Incorporadora/Imobiliária", "strength": "Ponto Forte Técnico"}}
            ],
            "quantitative_data": {{
                "avg_price_m2": "valor estimado",
                "avg_lot_size": "tamanho estimado",
                "monthly_condo_fee": "valor estimado"
            }},
            "benchmarking_insights": [
                "insight de serviço 1",
                "insight de processo 2"
            ],
            "raw_data_quality": "Avaliação da qualidade dos dados encontrados (Alta/Média/Baixa)"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um Engenheiro de Dados Imobiliários. Seja preciso, técnico e frio."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse LLM content
            llm_content = json.loads(response.choices[0].message.content)
            
            # --- CREATE DATA PACKAGE WITH METADATA (AUDIT LOG) ---
            final_package = {
                "metadata": {
                    "captured_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "agent": "HunterAgent",
                    "target_city": city,
                    "data_source": "Web Search (DuckDuckGo) & Internal Frameworks",
                    "status": "success"
                },
                "data": llm_content
            }
            
            # Save to .tmp with indentation
            with open(".tmp/market_intel.json", "w", encoding="utf-8") as f:
                json.dump(final_package, f, ensure_ascii=False, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error in Hunter Agent: {e}")
            return False
