"""
Simple test for Change Impact Analysis module.

Run:
    python test_module.py
"""

from pathlib import Path

from change_impact import ChangeImpactService


def create_sample_repo():
    sample = Path("sample_repo")
    sample.mkdir(exist_ok=True)

    utils_file = sample / "utils.py"
    main_file = sample / "main.py"

    utils_file.write_text(
        """
def calculate_tax(amount):
    return amount * 0.18


class DataProcessor:
    def process(self):
        return "processed"
""",
        encoding="utf-8"
    )

    main_file.write_text(
        """
from utils import calculate_tax, DataProcessor


def generate_invoice(amount):
    tax = calculate_tax(amount)
    return amount + tax


class InvoiceProcessor(DataProcessor):
    def save(self):
        pass
""",
        encoding="utf-8"
    )

    return sample


def main():
    print("Creating sample repository...")
    repo_path = create_sample_repo()

    print("Building impact graph...")
    service = ChangeImpactService(repo_path)

    print("\nChecking impact if utils.py changes...\n")

    result = service.file_impact("utils.py")

    print("Affected code parts:")
    print("-" * 60)

    if not result["affected"]:
        print("No affected code parts found.")
    else:
        for item in result["affected"]:
            print(
                f"File: {item['file']}\n"
                f"Name: {item['name']}\n"
                f"Kind: {item['kind']}\n"
                f"Reason: {item['reason']}\n"
                f"Impact Level: {item['impact_level']}\n"
                f"Line: {item['line']}\n"
            )
            print("-" * 60)

    print("\nTest completed successfully.")


if __name__ == "__main__":
    main()
