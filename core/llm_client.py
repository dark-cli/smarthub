import httpx
import time



class OllamaClient:
    _client = None  # Class variable!

    def __init__(self, base_url=None):
        self.base = base_url or "http://127.0.0.1:11434"
        # Create the client ONCE for the whole class
        if OllamaClient._client is None:
            print("OllamaClient is not initialized")
            OllamaClient._client = httpx.Client(timeout=6000)

    def chat(self, system: str, messages, model: str, num_ctx=4096):
        # Your usual code...
        if isinstance(messages, list):
            user = "\n".join([m["content"] for m in messages])
        else:
            user = str(messages)
        prompt = (system.strip() + "\n" + user.strip()).strip()

        t0 = time.perf_counter()
        resp = OllamaClient._client.post(f"{self.base}/api/generate", json={
            "model": model,
            "system": system.strip(),
            "prompt": user.strip(),
            "num_ctx": num_ctx,
            "stream": False
        })
        resp.raise_for_status()
        result = resp.json()
        t1 = time.perf_counter()
        print(f"LLM call: {model:20} {(t1-t0)*1000:.1f} ms")
        return result["response"]