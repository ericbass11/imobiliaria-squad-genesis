import json
import os
import datetime
from openai import OpenAI
from tools.central_bank import get_real_time_rates

class AnalystAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self):
        print("Analyst Agent initiated...")
        
        # 0. Load Knowledge Base (Frameworks)
        try:
            with open("knowledge_base/framework_analise.txt", "r", encoding="utf-8") as f:
                framework_finance = f.read()
            with open("knowledge_base/tecnica_imobiliaria.txt", "r", encoding="utf-8") as f:
                framework_tech = f.read()
        except FileNotFoundError:
            print("Warning: Framework file not found. Using default logic.")
            framework_finance = "Analise com prudência financeira."
            framework_tech = ""

        # 1. Get economic rates (Macro Data)
        print("Fetching and Normalizing Macro Economic Data...")
        rates = get_real_time_rates()
        selic = rates.get('selic')
        ipca = rates.get('ipca')
        
        # 2. Analyze with LLM (Data Scientist Mode)
        print("Running Cross-Reference Analysis (Data Scientist Mode)...")
        prompt = f"""
        Execute uma ANÁLISE DE CORRELAÇÃO entre o cenário Macro (Selic/IPCA) e o Produto Imobiliário de Alto Padrão.
        
        INDICADORES MACRO:
        Selic: {selic}%
        IPCA: {ipca}%
        
        FRAMEWORKS DE REFERÊNCIA:
        --- FINANCEIRO ---
        {framework_finance}
        ------------------
        --- TÉCNICO ---
        {framework_tech}
        ---------------
        
        SUA MISSÃO ANALÍTICA:
        1. Calcule o "Custo de Oportunidade Real" (Selic - IPCA) e compare com o Cap Rate estimado do setor (3-5%).
        2. Analise o impacto da inflação ({ipca}%) no CUB (Custo Unitário Básico da Construção).
        3. Defina a "Zona de Compra": O momento atual favorece quem tem liquidez (Cash King) ou quem alavanca (Dívida)?

        Saída APENAS em JSON válido com a seguinte estrutura (em Português do Brasil):
        {{
            "macro_correlation": {{
                "real_interest_rate": "valor calculado",
                "opportunity_cost_analysis": "análise técnica comparativa",
                "construction_inflation_risk": "análise de risco CUB"
            }},
            "investment_thesis": {{
                "buy_hold_sell": "veredito técnico",
                "liquidity_premium": "quanto vale o dinheiro na mão hoje?",
                "leverage_viability": "vale a pena financiar?"
            }},
            "data_confidence": "Nível de confiança na análise baseada nos inputs"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um Cientista de Dados Econômicos. Não dê opiniões, dê análises fundamentadas em números."},
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
                    "agent": "AnalystAgent",
                    "data_source": "Banco Central do Brasil (API)",
                    "status": "success"
                },
                "data": llm_content
            }
            
            # Save to .tmp with indentation
            with open(".tmp/financial_context.json", "w", encoding="utf-8") as f:
                json.dump(final_package, f, ensure_ascii=False, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error in Analyst Agent: {e}")
            return False
