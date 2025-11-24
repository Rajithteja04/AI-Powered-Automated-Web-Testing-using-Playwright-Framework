#!/usr/bin/env python3
"""
Simple test to isolate code generation issues.
"""

from agents.code_generator import generate_code
from agents.integration_guide import generate_integration_guide

# Mock state
class MockState:
    def __init__(self, requirement, extracted_code, generated_code=None):
        self.requirement = requirement
        self.extracted_code = extracted_code
        self.generated_code = generated_code or {}
        self.framework = 'flask'

mock_extracted_code = {
    'app.py': 'from flask import Flask\napp = Flask(__name__)',
    'routes.py': 'from flask import Blueprint\nmain = Blueprint("main", __name__)',
    'models.py': '',
    'forms.py': '',
    'config.py': '',
    'templates': {},
    'static': {'css': {}, 'js': {}},
    'project_structure': ['app.py', 'routes.py']
}

state = MockState('Add a contact page', mock_extracted_code)

print('Testing code generation...')
try:
    result = generate_code(state)
    print('Code generation successful')
    print('Generated keys:', list(result.get('generated_code', {}).keys()))
except Exception as e:
    print(f'Code generation failed: {e}')

print('Testing integration guide...')
try:
    state.generated_code = result.get('generated_code', {})
    guide_result = generate_integration_guide(state)
    print('Integration guide successful')
    print('Guide length:', len(guide_result.get('integration_instructions', '')))
except Exception as e:
    print(f'Integration guide failed: {e}')
