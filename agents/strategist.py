import json
import os
import datetime
from openai import OpenAI

class StrategistAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, city):
        print("Strategist Agent initiated...")
        
        # 0. Load Knowledge Base (Advanced Frameworks)
        try:
            with open("knowledge_base/framework_vendas_alto_padrao.txt", "r", encoding="utf-8") as f:
                fw_sales = f.read()
            with open("knowledge_base/framework_marketing_luxo.txt", "r", encoding="utf-8") as f:
                fw_marketing = f.read()
            with open("knowledge_base/tecnica_imobiliaria.txt", "r", encoding="utf-8") as f:
                fw_tech = f.read()
            with open("knowledge_base/framework_benchmarking.txt", "r", encoding="utf-8") as f:
                fw_bench = f.read()
        except FileNotFoundError:
            print("Warning: Framework files not found. Using default logic.")
            fw_sales = "Use gatilhos mentais de vendas."
            fw_marketing = "Foque no luxo."
            fw_tech = "Use dados técnicos."
            fw_bench = "Analise concorrentes."

        try:
            # 1. Read intel
            with open(".tmp/market_intel.json", "r", encoding="utf-8") as f:
                market_intel = f.read()
                
            with open(".tmp/financial_context.json", "r", encoding="utf-8") as f:
                financial_context = f.read()
            
            # 2. Synthesize with LLM (Strategic Advisor Mode)
            print("Synthesizing Strategic Dossier with LLM...")
            prompt = f"""
            ATENÇÃO: Você é um ESTRATEGISTA SÊNIOR DE MERCADO IMOBILIÁRIO (Consultoria 'Big 4' - McKinsey/BCG).
            
            Sua mente é moldada por estas 4 Bíblias do Mercado:
            1. VENDAS (Psicologia): {fw_sales}
            2. MARKETING (Posicionamento): {fw_marketing}
            3. TÉCNICA (Fundamentos): {fw_tech}
            4. BENCHMARKING (Service Excellence): {fw_bench}
            
            DADOS DE ENTRADA (ETL PROCESSADO):
            >>> INTELIGÊNCIA DE MERCADO (Players & Produtos):
            {market_intel}
            
            >>> CONTEXTO MACRO-FINANCEIRO (Economia Real):
            {financial_context}
            
            TAREFA FINAL: Escreva um RELATÓRIO DE INTELIGÊNCIA DE MERCADO (Dossiê Completo) para {city}.
            O objetivo NÃO é vender um lote agora. O objetivo é dar CLAREZA ABSOLUTA para a tomada de decisão da diretoria.
            A venda será uma consequência natural dessa análise bem feita.

            Estrutura Obrigatória do Relatório (Markdown Profissional):
            
            # Dossiê Estratégico: Análise de Mercado de Alto Padrão em {city}
            
            ## 1. Executive Summary (O Veredito do Consultor)
            *   Resumo em 3 parágrafos: Oportunidade, Risco e Recomendação Final (Go/No-Go).
            
            ## 2. Análise Profunda da Concorrência (Benchmarking)
            *   Mapeamento dos Players: Quem domina? Quem é irrelevante?
            *   Análise de Produto: Preço/m², Ticket Médio, Diferenciais Técnicos (use o framework técnico).
            *   **Best Practices (Visto em Players de Outros Setores):** O que podemos aprender com a Hotelaria/Automotivo de Luxo (citado no Framework de Benchmarking) para aplicar aqui?
            
            ## 3. Análise Econômica Aplicada
            *   Correlação Selic x Cap Rate na região.
            *   Custo de Oportunidade para o cliente: Por que comprar terra agora e não deixar no CDI? (Use argumentos matemáticos).
            *   Cenário de Inflação de Construção (CUB).
            
            ## 4. O Plano Mestre (Estratégia Baseada em Dados)
            *   **Produto Ideal:** Defina o produto perfeito para este mercado (Metragem, Lazer, Faixa de Preço) baseado nas lacunas dos concorrentes.
            *   **Posicionamento (Quiet Luxury):** Como nos diferenciar do "ruído" do marketing popular?
            *   **Estratégia Comercial:** Sugira 3 ações táticas para atingir o público UHNWI (Ex: Eventos fechados, Parcerias com Private Bank).
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um Consultor Estratégico Sênior. Frieza, Dados e Visão de Longo Prazo."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # 3. Save Report
            # Sanitize city name for filename
            safe_city = city.replace("/", "-").replace("\\", "-").strip()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"reports/Dossier_{safe_city}_{timestamp}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                
            return filename
            
        except Exception as e:
            print(f"Error in Strategist Agent: {e}")
            return None
