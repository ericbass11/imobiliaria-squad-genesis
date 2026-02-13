# Project: Real Estate Autonomous Squad (The "War Room") - HIGH END

## 1. Vision & Architecture
We are building a **Sequential Multi-Agent System** inspired by "Squads".
The goal is to automate the entire intelligence gathering process for a Real Estate Agency focused on **HIGH-END LOTS (Ticket > 500k)**.
**The Flow:**
1.  **Hunter Agent:** Scours the web for luxury competitors and high-end lot listings.
2.  **Analyst Agent:** Cross-references data with economic indicators (Selic/IPCA) focusing on wealth preservation.
3.  **Strategist Agent:** Consumes all data and produces a decision-making Dossier for Luxury Market.

**Key Principle:** "The Shared Brain". Agents do not talk directly; they write to a shared state (`.tmp/` folder). When one finishes, the Orchestrator triggers the next, passing the context.
...
### C. The Agents (Layer 2)

**1. The Hunter (`agents/hunter.py`)**

* **Persona:** "You are a Specialist in Luxury Real Estate & Traffic arbitrage. Your job is to find high-end lots (>500k), competitors, and **Reverse Engineer their Paid Traffic**."
* **Method `run(city: str)`:**
1. Executes `tools.search_engine.search_market(f"Imobiliárias alto padrão {city} lotes condomínio fechado")`.
2. Executes `tools.search_engine.search_market(f"Lotes à venda condomínio fechado {city} preço acima de 500 mil")`.
3. **[NEW] Ads Spy:** Searches for `site:facebook.com/ads/library` and Instagram sponsored posts to gather Ad Intelligence.
4. **LLM Task:** "Analyze benefits of high-end lots. Identify competitors in Class A niche. **Analyze Ad Strategies**. Output valid JSON in Portuguese."
5. **Save:** `.tmp/market_intel.json`.



**2. The Analyst (`agents/analyst.py`)**

* **Persona:** "You are a Family Office Consultant. You care about wealth preservation and investment opportunity."
* **Method `run()`:**
1. Executes `tools.central_bank.get_real_time_rates()`.
2. **LLM Task:** "Given Selic={selic}% and IPCA={ipca}%, create a context for High-End Investors. Cash vs Financing. Land as value reserve. Output valid JSON in Portuguese."
3. **Save:** `.tmp/financial_context.json`.



**3. The Strategist (`agents/strategist.py`)**

* **Persona:** "You are the Senior Luxury Partner. You read reports and make decisions for Class A market."
* **Method `run(city: str)`:**
1. Reads `.tmp/market_intel.json` (from Hunter).
2. Reads `.tmp/financial_context.json` (from Analyst).
3. **LLM Task:** "Synthesize reports. Write a Strategic Plan for High-End Lots Agency in {city}.
* **Section 1:** O Campo de Batalha (Concorrência e **Benchmark de Ads**).
* **Section 2:** O Terreno (Cenário Econômico para Classe A).
* **Section 3:** Plano de Ataque (Estratégias para Vender Lotes > 500k e **Tráfego Pago**).
* **Format:** Professional Markdown in Portuguese."


4. **Save:** `reports/Dossier_{city}_{date}.md`.



---

### D. The Orchestrator (`main_squad.py`)

This is the most important file. It ensures the **Synchrony**.

```python
import os
import time
from colorama import Fore, Style
from dotenv import load_dotenv
from agents.hunter import HunterAgent
from agents.analyst import AnalystAgent
from agents.strategist import StrategistAgent

# Load Environment
load_dotenv()

def print_step(step, msg):
    print(f"\n{Fore.CYAN}➤ STEP {step}: {Fore.WHITE}{msg}{Style.RESET_ALL}")

def main():
    print(f"{Fore.GREEN}🚀 REAL ESTATE SQUAD STARTED{Style.RESET_ALL}")
    city = input("Digite a cidade alvo para análise: ")
    
    # --- STEP 1: HUNTER ---
    print_step(1, "Acionando Agente 'Hunter' (Pesquisa de Mercado)...")
    hunter = HunterAgent()
    hunter_success = hunter.run(city)
    if not hunter_success:
        print(f"{Fore.RED}❌ Falha no Hunter. Abortando.{Style.RESET_ALL}")
        return

    # --- STEP 2: ANALYST ---
    print_step(2, "Acionando Agente 'Analyst' (Dados Econômicos)...")
    analyst = AnalystAgent()
    analyst_success = analyst.run()
    if not analyst_success:
        print(f"{Fore.RED}❌ Falha no Analyst. Abortando.{Style.RESET_ALL}")
        return

    # --- STEP 3: STRATEGIST ---
    print_step(3, "Acionando Agente 'Strategist' (Consolidação Estratégica)...")
    strategist = StrategistAgent()
    report_path = strategist.run(city)
    
    print(f"\n{Fore.GREEN}✅ MISSÃO CUMPRIDA!{Style.RESET_ALL}")
    print(f"📄 Relatório disponível em: {Fore.YELLOW}{report_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

```