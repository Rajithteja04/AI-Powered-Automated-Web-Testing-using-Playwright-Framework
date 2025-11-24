from celery_app import celery
from graph import build_code_generation_graph
from utils.zip_handler import ZipHandler
from models import db, ScriptHistory
from flask_login import current_user
import tempfile
import os
import json

@celery.task(bind=True)
def process_code_generation(self, requirement, browser, zip_path, user_id):
    """
    Background task for processing code generation requests.
    Updates task state for progress tracking.
    """
    try:
        # Update progress
        self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'Extracting project files...'})

        # Extract and analyze project
        extracted_code = ZipHandler.extract_project_zip(zip_path)

        # Detect framework
        framework = ZipHandler.detect_framework(extracted_code)

        # Clean up temp file
        os.unlink(zip_path)

        self.update_state(state='PROGRESS', meta={'progress': 30, 'message': 'Analyzing code and generating features...'})

        # Run code generation graph
        graph = build_code_generation_graph()
        state = graph.invoke({
            "requirement": requirement,
            "browser": browser,
            "extracted_code": extracted_code,
            "framework": framework
        })

        self.update_state(state='PROGRESS', meta={'progress': 80, 'message': 'Running tests...'})

        generated_code = state.get("generated_code", {})
        integration_instructions = state.get("integration_instructions", "")
        playwright_script = state.get("playwright_script", "N/A")
        execution_result = state.get("execution_result", "No result.")
        test_stats_report = state.get("test_stats_report", "")

        # Save to history
        with celery.flask_app.app_context():
            history_result = f"Generated Code:\n{str(generated_code)}\n\nIntegration Instructions:\n{integration_instructions}\n\nTest Script:\n{playwright_script}\n\nExecution Result:\n{execution_result}"
            if test_stats_report:
                history_result += f"\n\nStats:\n{test_stats_report}"

            history = ScriptHistory(
                user_id=user_id,
                requirement=f"[CODE GEN] {requirement}",
                script=str(generated_code),
                result=history_result
            )
            db.session.add(history)
            db.session.commit()

        self.update_state(state='PROGRESS', meta={'progress': 100, 'message': 'Complete!'})

        return {
            'generated_code': generated_code,
            'integration_instructions': integration_instructions,
            'playwright_script': playwright_script,
            'execution_result': execution_result,
            'test_stats_report': test_stats_report
        }

    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
