import requests
import json
from typing import Dict, Any

class OllamaSwarmAgent:
    def __init__(self, model_name: str = "llama3.1", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def generate_analysis(self, system_prompt: str, code_snippet: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": f"Analise o seguinte código-fonte:\n\n```python\n{code_snippet}\n```",
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Erro na comunicação com o Ollama: {str(e)}"

class AetherSwarmOrchestrator:
    def __init__(self):
        self.architect_agent = OllamaSwarmAgent(model_name="llama3.1")
        self.code_destructor = OllamaSwarmAgent(model_name="llama3.1")

    def run_security_scan(self, code: str) -> Dict[str, Any]:
        architect_prompt = (
            "Você é o AETHER-ARCHITECT, um arquiteto de software sênior especialista em "
            "análise AST, contratos de código e concorrência."
        )
        destructor_prompt = (
            "Você é o AETHER-DESTRUCTOR, um agente de QA focado em encontrar edge cases, "
            "race conditions, exceções não tratadas e falhas de segurança."
        )

        architecture_review = self.architect_agent.generate_analysis(architect_prompt, code)
        mutation_vectors = self.code_destructor.generate_analysis(destructor_prompt, code)

        return {
            "architecture_review": architecture_review,
            "mutation_vectors": mutation_vectors
        }

if __name__ == "__main__":
    sample_code = """
def process_transaction(account_id, amount, balance):
    if balance >= amount:
        balance -= amount
        return {"status": "success", "new_balance": balance}
    return {"status": "error", "message": "Insufficient funds"}
"""
    orchestrator = AetherSwarmOrchestrator()
    print("🚀 [AETHER-OMNI] A iniciar análise do Swarm...")
    result = orchestrator.run_security_scan(sample_code)
    print("\n--- ANÁLISE DE ARQUITETURA ---")
    print(result["architecture_review"])
    print("\n--- VETORES DE MUTAÇÃO / QA ---")
    print(result["mutation_vectors"])