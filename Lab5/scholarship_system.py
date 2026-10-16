
"""Scholarship eligibility screening with a configurable merit formula."""

import ast
import json
import operator
from pathlib import Path


class ScholarshipScreener:
    """Evaluate scholarship applicants and persist their results."""

    INCOME_LIMIT = 800000
    CUTOFF = 85

    BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }
    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def __init__(self):
        """Initialize the default formula and an empty results dictionary."""
        self.results = {}
        self.merit_formula = "gpa * 10 + credits * 2"

    def _evaluate_expression(self, node, values):
        """Evaluate only numeric constants, approved names, and arithmetic."""
        if isinstance(node, ast.Expression):
            return self._evaluate_expression(node.body, values)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]

        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in self.BINARY_OPERATORS
        ):
            left = self._evaluate_expression(node.left, values)
            right = self._evaluate_expression(node.right, values)

            if isinstance(node.op, ast.Pow):
                raise ValueError("Exponentiation is not supported.")

            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if right == 0:
                    raise ValueError("Division by zero is not allowed.")

            return self.BINARY_OPERATORS[type(node.op)](left, right)

        if (
            isinstance(node, ast.UnaryOp)
            and type(node.op) in self.UNARY_OPERATORS
        ):
            return self.UNARY_OPERATORS[type(node.op)](
                self._evaluate_expression(node.operand, values)
            )

        raise ValueError("Formula contains an unsupported expression.")

    def calculate_merit_score(self, gpa, credit_count):
        """Calculate an applicant's score using the configured formula."""
        try:
            expression = ast.parse(self.merit_formula, mode="eval")
            values = {
                "gpa": float(gpa),
                "credits": float(credit_count),
            }
            score = self._evaluate_expression(expression, values)
        except (
            SyntaxError,
            TypeError,
            ValueError,
            ZeroDivisionError,
            OverflowError,
        ) as exc:
            raise ValueError("Invalid merit formula or input values.") from exc

        if not isinstance(score, (int, float)) or not (
            float("-inf") < score < float("inf")
        ):
            raise ValueError("The merit score must be a finite number.")

        return score

    def evaluate_applicant(self, student_id, test_scores, logs=None):
        """Validate and evaluate an applicant, storing the resulting decision."""
        if logs is None:
            logs = []

        gpa = test_scores.get("gpa")
        credit_count = test_scores.get("credits", 0)
        income = test_scores.get("income", 0)

        if (
            isinstance(gpa, bool)
            or not isinstance(gpa, (int, float))
            or not 0 <= gpa <= 10
        ):
            raise ValueError("GPA must be a number between 0 and 10.")

        if (
            isinstance(credit_count, bool)
            or not isinstance(credit_count, (int, float))
            or credit_count < 0
        ):
            raise ValueError("Credits must be a non-negative number.")

        if (
            isinstance(income, bool)
            or not isinstance(income, (int, float))
            or income < 0
        ):
            raise ValueError("Income must be a non-negative number.")

        score = self.calculate_merit_score(gpa, credit_count)
        eligible = (
            score >= self.CUTOFF and income < self.INCOME_LIMIT
        )

        self.results[student_id] = {
            "score": score,
            "eligible": eligible,
        }
        logs.append(f"{student_id} scored {score}")
        return eligible

    def change_formula(self, new_formula):
        """Validate a new arithmetic formula before accepting it."""
        previous_formula = self.merit_formula
        self.merit_formula = new_formula

        try:
            self.calculate_merit_score(1, 1)
        except ValueError:
            self.merit_formula = previous_formula
            raise

    def persist_results(self, file="scholarships.json"):
        """Write applicant results to a UTF-8 JSON file."""
        with Path(file).open("w", encoding="utf-8") as output_file:
            json.dump(self.results, output_file, indent=2)

    def load_results(self, file="scholarships.json"):
        """Load saved results, preserving current results if loading fails."""
        try:
            with Path(file).open("r", encoding="utf-8") as input_file:
                loaded_results = json.load(input_file)
        except (OSError, json.JSONDecodeError):
            return

        if isinstance(loaded_results, dict):
            self.results = loaded_results

    def print_shortlist(self):
        """Print the applicants who satisfy the scholarship criteria."""
        print("Shortlisted applicants:")
        for student_id, applicant in self.results.items():
            if applicant.get("eligible"):
                print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the sample scholarship-screening workflow."""
    screener = ScholarshipScreener()
    logs = []

    sample_applicants = [
        ("U001", {"gpa": 9.1, "credits": 4, "income": 450000}),
        ("U002", {"gpa": 7.2, "credits": 1, "income": 300000}),
        ("U003", {"gpa": 8.5, "credits": 3, "income": 1}),
        ("U004", {"gpa": 6.5}),
    ]

    for student_id, scores in sample_applicants:
        screener.evaluate_applicant(student_id, scores, logs)

    formula = input("Merit formula (Enter to keep default): ").strip()
    if formula:
        try:
            screener.change_formula(formula)
        except ValueError as exc:
            print(f"Formula not changed: {exc}")

    screener.evaluate_applicant(
        "U005",
        {"gpa": 8.4, "credits": 3, "income": 600000},
        logs,
    )
    screener.persist_results()
    screener.load_results()
    screener.print_shortlist()


if __name__ == "__main__":
    main()
