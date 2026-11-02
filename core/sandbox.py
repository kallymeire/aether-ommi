import docker
import os
import structlog

logger = structlog.get_logger()

class AetherSandboxManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error("Erro ao conectar com o Docker Daemon", error=str(e))
            self.client = None

    def run_code_in_sandbox(self, code_snippet: str, language: str = "python") -> dict:
        """
        Executa um trecho de código dentro de um container Docker efêmero e isolado.
        """
        if not self.client:
            return {"status": "error", "output": "Docker não está disponível ou ativo na máquina."}

        temp_file = "temp_execution_target.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code_snippet)

        try:
            logger.info("A iniciar container Docker isolado...", language=language)
            image_name = "python:3.12-slim"
            
            clean_snippet = code_snippet.replace('"', '\\"')
            
            container = self.client.containers.run(
                image_name,
                command=f'python -c "{clean_snippet}"',
                detach=False,
                remove=True,
                stdout=True,
                stderr=True,
                mem_limit="512m",
                network_disabled=True
            )

            output = container.decode("utf-8")
            return {"status": "success", "output": output}

        except docker.errors.ContainerError as ce:
            return {"status": "failed", "output": ce.stderr.decode("utf-8") if hasattr(ce, 'stderr') else str(ce)}
        except Exception as e:
            return {"status": "error", "output": str(e)}
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == "__main__":
    sandbox = AetherSandboxManager()
    print("🐳 [AETHER-OMNI] A testar o gestor de Sandbox Docker...")
    test_code = "print('Olá do container isolado do AETHER-OMNI!')"
    resultado = sandbox.run_code_in_sandbox(test_code)
    print("Resultado da Execução no Docker:", resultado)