import streamlit as st
import sys
import os

# Garantir que o Python encontra a pasta core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.swarm import AetherSwarmOrchestrator
from core.symbolic import AetherSymbolicVerifier
from core.sandbox import AetherSandboxManager

# Configuração da página do Streamlit
st.set_page_config(
    page_title="AETHER-OMNI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AETHER-OMNI: Distributed Neuro-Symbolic Engine")
st.markdown("Plataforma Autónoma de Garantia de Software, Verificação Formal e Swarm Local (Ollama + Z3 + Docker).")

# Criar abas para separar os módulos
tab1, tab2, tab3 = st.tabs(["🤖 Swarm LLM (Ollama)", "🔍 Verificação Simbólica (Z3)", "🐳 Sandbox (Docker)"])

with tab1:
    st.header("Orquestração de Agentes da Colmeia")
    st.markdown("Envie um trecho de código para análise arquitetural e busca de vetores de mutação/falha.")
    
    default_code = """def process_transaction(account_id, amount, balance):
    if balance >= amount:
        balance -= amount
        return {"status": "success", "new_balance": balance}
    return {"status": "error", "message": "Insufficient funds"}"""
    
    code_input = st.text_area("Código-fonte alvo:", default_code, height=150)
    
    if st.button("🚀 Executar Análise do Swarm"):
        with st.spinner("O Ollama está a analisar a arquitetura e a procurar vulnerabilidades..."):
            orchestrator = AetherSwarmOrchestrator()
            result = orchestrator.run_security_scan(code_input)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏛️ Análise de Arquitetura")
                st.write(result["architecture_review"])
            with col2:
                st.subheader("⚡ Vetores de Mutação / QA")
                st.write(result["mutation_vectors"])

with tab2:
    st.header("Verificação Formal de Invariantes")
    st.markdown("Utiliza o Z3 Solver para provar matematicamente a correção de regras lógicas.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        initial_bal = st.number_input("Saldo Inicial:", value=100, step=10)
    with col_b:
        withdrawal = st.number_input("Valor do Saque:", value=150, step=10)
        
    if st.button("🔍 Executar Prova Matemática"):
        verifier = AetherSymbolicVerifier()
        resultado_formal = verifier.verify_transaction_logic(initial_balance=initial_bal, withdrawal_amount=withdrawal)
        st.info(resultado_formal)

with tab3:
    st.header("Execução Isolada em Contentor Docker")
    st.markdown("Executa código Python de forma totalmente segura num container efêmero.")
    
    script_input = st.text_area("Script Python para executar no Sandbox:", "print('Olá do container isolado do AETHER-OMNI! Ambiente seguro ativo.')", height=100)
    
    if st.button("🐳 Disparar Execução no Docker"):
        with st.spinner("A iniciar container Docker isolado..."):
            sandbox = AetherSandboxManager()
            exec_result = sandbox.run_code_in_sandbox(script_input)
            
            if exec_result["status"] == "success":
                st.success("Execução concluída com sucesso!")
                st.code(exec_result["output"])
            else:
                st.error(f"Erro na execução: {exec_result['output']}")