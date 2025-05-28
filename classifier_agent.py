import json
import fitz  
from memory import Memory

class ClassifierAgent:
    """
    Classifier Agent: Determines input format (PDF, JSON, Email), classifies intent,
    and routes the data to the appropriate agent. Logs format and intent into memory.
    """
    def __init__(self, memory):
        self.memory = memory

    def classify(self, file_path):
        # Determine file format by extension
        file_lower = file_path.lower()
        if file_lower.endswith(".json"):
            file_format = "JSON"
            with open(file_path, 'r') as f:
                content = f.read()
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON file.")
            text = json.dumps(data)  
        elif file_lower.endswith(".pdf"):
            file_format = "PDF"
            # Extract text from PDF pages
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text() 
            data = None
        else:
            file_format = "Email"
            with open(file_path, 'r') as f:
                text = f.read()
            data = None

        intent = self._determine_intent(text)
        timestamp = __import__('datetime').datetime.now().isoformat()
        thread_id = file_path  

        # Log the format and intent in memory
        self.memory.log(source=file_path, input_format=file_format, intent=intent,
                        extracted="", thread_id=thread_id, timestamp=timestamp)
        return file_format, intent, data or text

    def _determine_intent(self, text):
        """Simple intent classification by keyword matching."""
        text_lower = text.lower()
        if "invoice" in text_lower:
            return "Invoice"
        if "rfq" in text_lower or "request for quotation" in text_lower:
            return "RFQ"
        if "complaint" in text_lower:
            return "Complaint"
        if "regulation" in text_lower:
            return "Regulation"
        return "Unknown"
