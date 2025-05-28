import re
from memory import Memory

class EmailAgent:
    """
    Email Agent: Processes email content, extracts sender, intent, urgency,
    and formats data for CRM-style usage.
    """
    def __init__(self, memory):
        self.memory = memory

    def process(self, email_text, source):
        # Parse lines for From, Subject, and body
        lines = email_text.splitlines()
        sender = ""
        subject = ""
        body_lines = []
        in_body = False

        for line in lines:
            if line.lower().startswith("from:"):
                sender = line.split(":", 1)[1].strip()
            elif line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.strip() == "":
                in_body = True
                continue
            if in_body:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()
        content = subject + " " + body

        # Determine intent and urgency
        intent = self._determine_intent(content)
        urgency = ("High" if re.search(r"\burgent\b", content, re.IGNORECASE)
                   or re.search(r"\basap\b", content, re.IGNORECASE) else "Normal")

        # Format for CRM
        crm_data = {
            "sender": sender,
            "subject": subject,
            "body": body,
            "intent": intent,
            "urgency": urgency
        }

        extracted_str = str(crm_data)
        timestamp = __import__('datetime').datetime.now().isoformat()
        thread_id = source  # use file name as conversation ID

        # Log extracted data
        self.memory.log(source=source, input_format="Email", intent=intent,
                        extracted=extracted_str, thread_id=thread_id, timestamp=timestamp)
        return crm_data

    def _determine_intent(self, text):
        text_lower = text.lower()
        if "invoice" in text_lower:
            return "Invoice"
        if "rfq" in text_lower or "request for quotation" in text_lower:
            return "RFQ"
        if "complaint" in text_lower:
            return "Complaint"
        if "regulation" in text_lower:
            return "Regulation"
        return "General"
