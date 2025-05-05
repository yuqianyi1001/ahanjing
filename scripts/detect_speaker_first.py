import os
import json
import re
import requests

T0099_DIR = os.path.join(os.path.dirname(__file__), '..', 'T0099.md')
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), '..', 'T0099_speaker_first.json')
OLLAMA_MODEL = 'qwen3:1.7b' #'qwen3:0.6b'
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
MAX_CHARS = 500

def get_md_files(directory):
    return sorted([
        f for f in os.listdir(directory)
        if f.endswith('.md') and os.path.isfile(os.path.join(directory, f))
    ])

def ask_ollama(text):
    prompt = (
        f"{text}\n\n"
        "Question: In this Sutra, does the Buddha speak first, or does a disciple or someone else ask a question first? "
        "don't count '如是我聞' as Buddha speak."
        "Please answer with one word: 'Buddha', 'disciple', or 'other'."
    )
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        print(data)
        answer = data.get("response", "").strip().lower()
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)

        if 'buddha' in answer:
            return 'Buddha'
        elif 'disciple' in answer:
            return 'disciple'
        elif 'other' in answer:
            return 'other'
        else:
            return 'unknown'
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        return 'unknown'

def main():
    # Load existing results if the JSON file exists
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = {}

    files = get_md_files(T0099_DIR)
    for fname in files:
        if fname in results:
            print(f"Skipping {fname}, already processed.")
            continue

        print(f"Processing {fname}...")
        fpath = os.path.join(T0099_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)

        answer = ask_ollama(content)
        results[fname] = answer
        print(f"{fname}: {answer}")

        # Save results incrementally
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Final results saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()

