# main.py
from crew_manager import IntelligenceCrew
import os

def main():
    # Example usage:
    product_topic = "latest updates for AI Productivity Tools like Notion AI"
    # Or you can take input from the user:
    # product_topic = input("Enter the product category/topic for intelligence research: ")

    crew_instance = IntelligenceCrew(product_topic)
    report = crew_instance.run()

    # Save the report
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    report_filename = os.path.join(output_dir, f"competitive_intelligence_report_{product_topic.replace(' ', '_').replace('/', '_')}.md")
    with open(report_filename, "w") as f:
        f.write(report)

    print(f"\nFinal report saved to: {report_filename}")

if __name__ == "__main__":
    main()