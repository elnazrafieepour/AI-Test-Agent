from app.llm.client import LLMClient
from app.models.requirement_analysis import RequirementAnalysis


class TestEngineerAgent:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze_requirement(
        self,
        requirement: str,
    ) -> RequirementAnalysis:

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

For every test scenario:
- Provide a clear title
- Explain what should be tested
- Classify the scenario
- Assign a priority

For every risk:
- Explain the risk
- Assign a severity

For every ambiguity:
- Explain what is unclear
- Provide a question that should be asked to clarify it

Requirement:
{requirement}
"""

        return self.llm.ask_structured(
            prompt,
            RequirementAnalysis,
        )