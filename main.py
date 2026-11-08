import json
import urllib.request
import urllib.error

MODEL = "gemma4:latest"
API_URL = "http://localhost:11434/api/chat"

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful personal AI assistant. "
            "Your name is MyAI. Explain things clearly, "
            "be friendly, and help the user learn Python."
        )
    }
]


def ask_ai(question):
    messages.append({
        "role": "user",
        "content": question
    })

    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except urllib.error.HTTPError as error:
        messages.pop()
        details = error.read().decode("utf-8", errors="replace")
        return f"Ollama API error ({error.code}): {details}"

    except urllib.error.URLError:
        messages.pop()
        return (
            "Cannot connect to Ollama. "
            "Make sure Ollama is installed and running."
        )

    except (KeyError, ValueError) as error:
        messages.pop()
        return f"Unexpected response from Ollama: {error}"


def main():
    print("=" * 45)
    print("          MyAI - Personal Assistant")
    print(f"          Model: {MODEL}")
    print("=" * 45)
    print("Ask me anything!")
    print("Commands: /clear to reset chat, /exit to quit")

    while True:
        try:
            question = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nMyAI: Goodbye!")
            break

        if not question:
            continue

        if question.lower() == "/exit":
            print("MyAI: Goodbye!")
            break

        if question.lower() == "/clear":
            messages[:] = messages[:1]
            print("MyAI: Conversation cleared!")
            continue

        print("\nMyAI: Thinking...")

        answer = ask_ai(question)
        print("\nMyAI:", answer)


if __name__ == "__main__":
    main()
