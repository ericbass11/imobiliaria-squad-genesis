import os
import sys
from colorama import Fore, Style, init
from dotenv import load_dotenv
from agents.hunter import HunterAgent
from agents.analyst import AnalystAgent
from agents.strategist import StrategistAgent

# Load Environment
load_dotenv()
init(autoreset=True)

def print_step(step, msg):
    print(f"\n{Fore.CYAN}➤ STEP {step}: {Fore.WHITE}{msg}{Style.RESET_ALL}")

def main():
    print(f"{Fore.GREEN}🚀 REAL ESTATE SQUAD STARTED{Style.RESET_ALL}")
    
    # Simple check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}❌ Error: OPENAI_API_KEY not found in .env file.{Style.RESET_ALL}")
        return

    # User Input
    if len(sys.argv) > 1:
        city = sys.argv[1]
    else:
        city = input("Digite a cidade alvo para análise: ")
    
    if not city:
        print(f"{Fore.RED}❌ Cidade não informada. Abortando.{Style.RESET_ALL}")
        return

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
    
    if report_path:
        print(f"\n{Fore.GREEN}✅ MISSÃO CUMPRIDA!{Style.RESET_ALL}")
        print(f"📄 Relatório disponível em: {Fore.YELLOW}{report_path}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ Falha ao gerar relatório final.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()