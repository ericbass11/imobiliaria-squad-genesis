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

def choose_persona():
    print(f"\n{Fore.MAGENTA}🎭 SELECIONE O CLONE ESTRATEGISTA:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} David Ogilvy (Advertising Master - Foco em Luxo & Copy)")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Alex Hormozi (Grand Slam Offer - Foco em ROI & Valor)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Chris Voss (The Negotiator - Foco em Empatia & Objeções)")
    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Consultor Padrão (Análise Sóbria)")
    
    choice = input("\nEscolha sua estratégia (1-4): ").strip()
    
    if choice == "1":
        return "david_ogilvy"
    elif choice == "2":
        return "alex_hormozi"
    elif choice == "3":
        return "chris_voss"
    else:
        return None  # Default Standard

def main():
    print(f"{Fore.GREEN}🚀 REAL ESTATE SQUAD V2 STARTED (AIOS with Clones){Style.RESET_ALL}")
    
    # Simple check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}❌ Error: OPENAI_API_KEY not found in .env file.{Style.RESET_ALL}")
        return

    # User Input - City
    if len(sys.argv) > 1:
        city = sys.argv[1]
    else:
        city = input("Digite a cidade alvo para análise: ")
    
    if not city:
        print(f"{Fore.RED}❌ Cidade não informada. Abortando.{Style.RESET_ALL}")
        return

    # User Input - Persona
    chosen_persona = choose_persona()

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
    print_step(3, f"Acionando Agente 'Strategist' (Clone: {chosen_persona if chosen_persona else 'Standard'})...")
    strategist = StrategistAgent()
    report_path = strategist.run(city, persona_name=chosen_persona)
    
    if report_path:
        print(f"\n{Fore.GREEN}✅ MISSÃO CUMPRIDA!{Style.RESET_ALL}")
        print(f"📄 Relatório disponível em: {Fore.YELLOW}{report_path}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ Falha ao gerar relatório final.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()