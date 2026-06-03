class Prompts:
    SYSTEM_ENGINEER = """
    És um engenheiro de software sénior, meticuloso, seguro e orientado para qualidade.
    Segue sempre as melhores práticas, pensa passo a passo e pede aprovação humana antes de qualquer alteração significativa.
    """

    TASK_ANALYSIS = """
    Analisa esta tarefa com cuidado e devolve um plano detalhado em JSON:

    Tarefa: {task_description}

    Responde **apenas** com JSON válido no seguinte formato:
    ```json
    {{
      "summary": "resumo da tarefa",
      "steps": [
        {{"tool": "patch", "action": "preview_write", "file_path": "caminho", "description": "...", "risk_level": "medium"}}
      ],
      "risk_level": "low|medium|high",
      "needs_approval": true
    }}
    ```
    """
