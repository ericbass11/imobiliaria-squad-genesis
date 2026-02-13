# 🏙️ Squad de Inteligência Imobiliária (Project Genesis)

> **"Dados antes da Venda."**

Este projeto implementa um **Sistema Multi-Agente** para analisar o mercado imobiliário de Alto Padrão (Ticket > 500k) com profundidade técnica e econômica.

## 🧠 Brain (Inteligência)

O sistema utiliza 4 Frameworks de Elite (`knowledge_base/`) para guiar os agentes:
1.  **Técnico:** Engenharia e Arquitetura (Pé-direito, Acústica, Insolação).
2.  **Financeiro:** ROI, Cap Rate, Custo de Oportunidade (Selic x IPCA).
3.  **Marketing:** Posicionamento "Quiet Luxury".
4.  **Benchmarking:** Excelência em Serviço (Hotelaria/Automotivo).

## 🤖 The Squad (Agentes)

*   **HUNTER (`agents/hunter.py`):** O Engenheiro de Dados. Extrai fichas técnicas, limpa ruído e encontra os verdadeiros players.
*   **ANALYST (`agents/analyst.py`):** O Cientista de Dados. Cruza macroeconomia com microeconomia imobiliária.
*   **STRATEGIST (`agents/strategist.py`):** O Consultor Sênior. Gera o Dossiê Estratégico para tomada de decisão.

## 🚀 Como Rodar

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure a API Key:**
    *   Crie um arquivo `.env` na raiz.
    *   Adicione: `OPENAI_API_KEY=sk-...`
3.  **Execute:**
    ```bash
    python main_squad.py
    ```
4.  **Resultado:**
    *   Verifique a pasta `reports/` para ler o Dossiê gerado.

---
*Desenvolvido com Python, OpenAI GPT-4 e DuckDuckGo.*
