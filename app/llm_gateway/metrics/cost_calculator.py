# app/llm_gateway/metrics/cost_calculator.py

from decimal import Decimal

class CostCalculator:
    @staticmethod
    def calculate(*, model, input_tokens: int, output_tokens: int) -> float:
        """
        Returns  USD cost

        Pricing table can be expanded further
        """

        pricing = {
            "google.gemma-3-12b-it": {
                "input": Decimal("0.00011"),
                "output": Decimal("0.00034")
            }
        }

        if model not in pricing:
            return 0.0

        input_cost = Decimal(input_tokens)/Decimal(1000) * pricing[model]['input']
        output_cost = Decimal(output_tokens)/Decimal(1000) * pricing[model]['output']

        return float(input_cost + output_cost)