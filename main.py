import argparse
from classifier_agent import ClassifierAgent
from json_agent import JSONAgent
from email_agent import EmailAgent
from memory import Memory

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent AI System CLI")
    parser.add_argument("--input", required=True, help="Path to input file (PDF, JSON, or email text).")
    args = parser.parse_args()

    mem = Memory()
    classifier = ClassifierAgent(mem)
    file_format, intent, data = classifier.classify(args.input)

    print(f"Detected format: {file_format}")
    print(f"Detected intent: {intent}")

    if file_format == "JSON":
        json_agent = JSONAgent(mem)
        extracted, anomalies = json_agent.process(data, intent, args.input)
        print("Extracted fields from JSON:")
        print(extracted)
        if anomalies:
            print("Anomalies:", anomalies)
    elif file_format == "Email":
        email_agent = EmailAgent(mem)
        crm_data = email_agent.process(data, args.input)
        print("Extracted data from Email:")
        for k, v in crm_data.items():
            print(f"  {k}: {v}")
    elif file_format == "PDF":
        print("Extracted text from PDF (first 200 chars):")
        print(data[:200] + "...")
    else:
        print("Unknown format. Cannot process.")

    print("Done. Logged to memory.")

if __name__ == "__main__":
    main()
