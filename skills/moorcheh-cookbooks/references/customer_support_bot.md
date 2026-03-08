# Customer Support Bot

Build a customer support chatbot that answers questions from your FAQ and documentation using conversational RAG with chat history.

## Architecture

```
FAQ/Docs → Upload to Moorcheh → Customer asks → Search context → Generate answer with chat history → Response
```

## Prerequisites

- [Project Setup](project_setup.md)
- [Environment Requirements](environment_requirements.md)

## Implementation

### Step 1: Create and Populate the Support Namespace

```python
from moorcheh_sdk import MoorchehClient
import time

client = MoorchehClient(api_key="your-api-key")

# Create namespace for support docs
client.namespaces.create(namespace_name="customer-support", type="text")

# Upload FAQ documents
faqs = [
    {
        "id": "faq-billing-1",
        "text": "To cancel your subscription, go to Settings > Billing > Cancel Plan. Your access continues until the end of the billing period.",
        "category": "billing",
        "priority": "high"
    },
    {
        "id": "faq-account-1",
        "text": "To reset your password, click 'Forgot Password' on the login page. You'll receive a reset link via email within 5 minutes.",
        "category": "account",
        "priority": "high"
    },
    {
        "id": "faq-features-1",
        "text": "Our Pro plan includes unlimited searches, 10GB storage, API access, and priority support. Upgrade anytime from your dashboard.",
        "category": "features",
        "priority": "medium"
    }
]

client.documents.upload(namespace_name="customer-support", documents=faqs)
time.sleep(5)
```

### Step 2: Build the Chatbot

```python
class SupportBot:
    def __init__(self, namespace: str = "customer-support"):
        self.client = MoorchehClient(api_key="your-api-key")
        self.namespace = namespace
        self.chat_history = []

    def ask(self, question: str) -> str:
        """Answer a customer question with context from support docs."""
        response = self.client.answer.generate(
            namespace=self.namespace,
            query=question,
            top_k=3,
            temperature=0.3,
            chatHistory=self.chat_history,
            headerPrompt="You are a helpful customer support agent. Answer questions accurately based on the provided documentation. If you don't know the answer, say so and suggest contacting support@example.com.",
            footerPrompt="Be concise, friendly, and professional."
        )

        answer = response.get("answer", "I couldn't find an answer. Please contact support@example.com.")

        # Update chat history
        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "assistant", "content": answer})

        return answer

    def reset(self):
        """Reset conversation history."""
        self.chat_history = []

# Usage
bot = SupportBot()
print(bot.ask("How do I cancel my subscription?"))
print(bot.ask("Will I lose access immediately?"))  # Uses chat history
```

### Step 3: Add Category Filtering

```python
def ask_category(self, question: str, category: str = None) -> str:
    """Search within a specific category using metadata filters."""
    query = question
    if category:
        query = f"{question} #category:{category}"

    response = self.client.answer.generate(
        namespace=self.namespace,
        query=query,
        top_k=3,
        temperature=0.3
    )
    return response.get("answer", "No answer found.")

# Search only billing FAQs
bot.ask_category("How do I get a refund?", category="billing")
```

### Step 4: FastAPI Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Customer Support Bot")
bot = SupportBot()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str

# Store sessions
sessions = {}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if request.session_id not in sessions:
        sessions[request.session_id] = SupportBot()

    bot = sessions[request.session_id]
    reply = bot.ask(request.message)
    return ChatResponse(reply=reply)

@app.post("/chat/reset")
async def reset(session_id: str = "default"):
    if session_id in sessions:
        sessions[session_id].reset()
    return {"status": "reset"}
```

## Deployment

1. Upload your actual FAQ and documentation to the `customer-support` namespace
2. Customize the `headerPrompt` with your company name and tone
3. Deploy as a FastAPI service
4. Connect to your chat widget or support platform
