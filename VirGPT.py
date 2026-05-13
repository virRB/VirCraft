import requests

def askAI(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        return r.json()["response"]
    except Exception as e:
        print(f'Lol there was some error idk read it: {e}')
        return "Lol error"