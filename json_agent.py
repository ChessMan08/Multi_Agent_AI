from memory import Memory

class JSONAgent:
    """
    JSON Agent: Processes structured JSON payloads, extracts fields into a target schema,
    and flags anomalies or missing fields.
    """
    def __init__(self, memory):
        self.memory = memory
        # Define expected schemas for different intents
        self.schemas = {
            "Invoice": ["invoice_number", "date", "customer", "items"],
            "RFQ": ["rfq_id", "product", "quantity"],
            "Complaint": ["complaint_id", "customer", "issue"],
            "Regulation": ["regulation_id", "title", "text"]
        }

    def process(self, json_data, intent, source):
        expected = self.schemas.get(intent, [])
        extracted = {}
        anomalies = []

        if expected:
            for field in expected:
                if field in json_data:
                    extracted[field] = json_data[field]
                else:
                    anomalies.append(f"Missing field: {field}")
            for field in json_data:
                if field not in expected:
                    anomalies.append(f"Unexpected field: {field}")
        else:
            for field, value in json_data.items():
                extracted[field] = value

        extracted_str = str(extracted)
        if anomalies:
            extracted_str += " | Anomalies: " + "; ".join(anomalies)

        timestamp = __import__('datetime').datetime.now().isoformat()
        thread_id = source 

        # Log the extracted fields and any anomalies
        self.memory.log(source=source, input_format="JSON", intent=intent,
                        extracted=extracted_str, thread_id=thread_id, timestamp=timestamp)
        return extracted, anomalies
