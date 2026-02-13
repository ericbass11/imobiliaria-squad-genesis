import json
import os
import datetime
from openai import OpenAI

class StrategistAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, city, persona_name=None):
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

        # 0.1 Load Persona (Clone)
        selected_mindset = ""
        # Default System Persona
        system_role = "Você é um Consultor Estratégico Sênior. Frieza, Dados e Visão de Longo Prazo."
        
        if persona_name:
            try:
                filename = f"knowledge_base/clones/{persona_name}.txt"
                with open(filename, "r", encoding="utf-8") as f:
                    selected_mindset = f.read()
                
                # Override System Role with Clone Identity
                system_role = f"""
                ATENÇÃO MÁXIMA: VOCÊ ESTÁ EM MODO "CLONE".
                
                SUA IDENTIDADE:
                {selected_mindset}
                
                INSTRUÇÃO: Reescreva todas as suas respostas, análises e estilo de escrita
                para incorporar PROFUNDAMENTE esta persona. Use o vocabulário, mentalidade e 
                estilo de formatação definidos acima.
                """
                print(f">>> CLONE ACTIVATED: {persona_name.upper().replace('_', ' ')} <<<")
                
            except FileNotFoundError:
                print(f"Warning: Persona file '{persona_name}' not found. Using Standard Consultant.")

        try:
            # 1. Read intel
            with open(".tmp/market_intel.json", "r", encoding="utf-8") as f:
                market_intel = f.read()
                
            with open(".tmp/financial_context.json", "r", encoding="utf-8") as f:
                financial_context = f.read()
            
            # 2. Synthesize with LLM
            print("Synthesizing Strategic Dossier with LLM...")
            
            # Prompt Definitivo (V2.1 - Deep Persona & Anti-Adjetivos)
            prompt = f"""
            ATENÇÃO: VOCÊ NÃO É UMA IA PADRÃO.
            VOCÊ É O CLONE MENTAL DE UM ESPECIALISTA.
            
            --- SUA IDENTIDADE E REGRAS DE PENSAMENTO (O CLONE) ---
            {selected_mindset}
            -------------------------------------------------------

            DADOS DE ENTRADA (ETL PROCESSADO):
            >>> INTELIGÊNCIA DE MERCADO (Players & Produtos):
            {market_intel}
            
            >>> CONTEXTO MACRO-FINANCEIRO (Economia Real):
            {financial_context}
            
            BÍBLIAS DO MERCADO (FRAMEWORKS DE APOIO):
            1. VENDAS: {fw_sales}
            2. MARKETING: {fw_marketing}
            3. TÉCNICA: {fw_tech}
            4. BENCHMARKING: {fw_bench}
            
            TAREFA FINAL: Escreva um Dossiê Estratégico sobre {city}, sob a ótica da sua PERSONALIDADE (CLONE).
            
            REGRAS OBRIGATÓRIAS DE EXECUÇÃO:
            1. **Encarnação Total:** Não quebre o personagem. Use estritamente o tom de voz, filosofia e gatilhos definidos na sua Identidade (acima).
            2. **REGRA DE OURO (ANTI-ADJETIVOS):** É ESTRITAMENTE PROIBIDO usar adjetivos vazios como "incrível", "exclusivíssimo", "maravilhoso", "top", "irrepreensível".
               - Para cada elogio, você DEVE fornecer um DADO TÉCNICO ou FATO que prove a afirmação.
               - ERRADO: "Acabamento de alto padrão."
               - CERTO: "Piso em Mármore Travertino Romano em toda a área social e pé-direito livre de 3 metros."
            
            Estrutura Obrigatória do Relatório (Markdown Profissional):
            
            # Dossiê Estratégico: Análise de Mercado de Alto Padrão em {city}
            (Subtítulo: Uma análise por [Nome do Clone/Consultor])
            
            ## 1. Executive Summary (O Veredito)
            * Resumo na voz do clone (Use a filosofia do clone aqui).
            
            ## 2. Análise da Concorrência (Benchmarking)
            * Quem são os players?
            * Análise de Produto e Preço (Use números, não adjetivos).
            * **Best Practices:** (Aplique os frameworks de apoio aqui).
            
            ## 3. Análise Econômica (A Lógica do Dinheiro)
            * Custo de Oportunidade e Cap Rate.
            * Inflação de Construção vs Valorização do Lote.
            
            ## 4. O Plano Mestre (A Estratégia do Clone)
            * **Produto Ideal:** Defina o produto perfeito (Metragem, Lazer, Diferenciais).
            * **Posicionamento:** Como vender isso? (Use os gatilhos mentais do clone).
            * **Ações Táticas:** 3 ações concretas e imediatas.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # 3. Save Report
            # Sanitize city name for filename
            safe_city = city.replace("/", "-").replace("\\", "-").strip()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Include persona in filename
            suffix = f"_{persona_name}" if persona_name else "_Standard"
            filename = f"reports/Dossier_{safe_city}{suffix}_{timestamp}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                
            return filename
            
        except Exception as e:
            print(f"Error in Strategist Agent: {e}")
            return None
