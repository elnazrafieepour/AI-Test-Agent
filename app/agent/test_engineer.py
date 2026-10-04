from app.llm.client import LLMClient


class TestEngineerAgent:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze_requirement(self, requirement: str) -> str:
        prompt = f"""
You are a Senior Software Test Engineer.

Analyze the following software requirement.

Identify:
1. Functional test scenarios
2. Negative scenarios
3. Boundary conditions
4. Validation rules
5. Potential risks
6. Missing or ambiguous requirements

Requirement:
{requirement}
"""

        return self.llm.ask(prompt)