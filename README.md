# AI Studio Bridge

An unofficial, thread-safe Python bridge for automating [Google AI Studio](https://aistudio.google.com/) using Playwright. 

This library turns the Google AI Studio web interface into a programmable API. It is designed for developers who want to interact with Gemini models, extract text from files, and manage conversation flow programmatically.

## Features
*   **Thread-Safe:** Uses a dedicated worker thread with a command queue, making it perfect for integration into web backends (FastAPI, Flask) or larger applications.
*   **Browser Stealth:** Configured with stealth arguments to prevent common bot-detection triggers.
*   **File Handling:** Automatically handles file uploads, progress bars, and verbatim text extraction.
*   **Control:** Switch between Gemini models, set "Thinking" levels (High/Low), and retrieve responses as either Plain Text or Markdown.
*   **Optimized:** Blocks heavy media/assets for faster loading and includes CSS optimizations to disable animations.

---

## Installation

### 1. Requirements
Ensure you have Python installed. Then, install the required packages:

```bash
pip install playwright
```

### 2. Browser Binaries
Playwright requires the browser engines to be installed separately:

```bash
playwright install chromium
```

---

## The "First Run" Experience (Crucial)
This library uses **Persistent Contexts**. 
1.  The first time you run your code, it will open a browser window and navigate to the AI Studio URL.
2.  **You must manually log in** to your Google account within that browser window.
3.  The library will save your cookies and session state in a folder named `chrome_stealth_profile`.
4.  On every subsequent run, it will automatically use that session so you stay logged in.

---

## Quick Start & Usage

### 1. Initialize
Always instantiate the class once. It initializes the `queue` system and the background thread.

```python
from backend.browser_bridge import AIStudioBridge

bridge = AIStudioBridge()
```

### 2. Sending Prompts
```python
# Simple prompt
response = bridge.send_prompt("What is the capital of France?")

# Requesting Markdown formatting
md_response = bridge.send_prompt("Write a Python script to calculate Fibonacci", return_markdown=True)

# Using it in an existing chat (new_chat=False keeps history)
follow_up = bridge.send_prompt("Can you optimize that code?", new_chat=False)
```

### 3. File Extraction
The library handles the entire UI interaction: clicking the "+", selecting the file, waiting for the processing, and returning the text.

```python
# Provide an absolute path to the file
text_content = bridge.extract_text_from_file("/Users/me/documents/report.pdf")
print(text_content)
```

### 4. Model Management
```python
# Get current bridge state
state = bridge.get_bridge_state()
print(f"Current Model: {state['active']}")

# Switch models
bridge.set_model("Gemini 1.5 Pro")
```

---

## API Summary

| Method | Returns | Description |
| :--- | :--- | :--- |
| `send_prompt(msg, md, new_chat)` | String | Sends prompt, waits for AI, cleans result. |
| `extract_text_from_file(path)` | String | Uploads file, waits for processing, extracts text. |
| `get_bridge_state()` | Dict | Returns `{'models': [...], 'active': '...'}`. |
| `set_model(name)` | Boolean | Switches the model in the UI. |
| `reset()` | None | Navigates back to a clean state. |

---

## Troubleshooting & Best Practices

*   **Handling Timeouts:** Methods have an internal timeout of 300 seconds (5 minutes). If you are processing very large files or complex reasoning tasks, ensure your calling script is prepared to wait.
*   **The "Selector" Problem:** This library relies on specific CSS selectors. If Google updates their UI and the code stops working, you will need to inspect the page, find the new class names, and update the selectors in `browser_bridge.py`.
*   **Headless Server Environment:** If running on a Linux server without a display, set `headless=True` in your `browser_args` inside `browser_bridge.py`. You may also need `xvfb` to simulate a monitor.
*   **Thread Safety:** The `queue.Queue` system ensures that multiple calls (e.g., from a web server) are queued and processed one-by-one. **Do not** instantiate multiple `AIStudioBridge` objects, as they will conflict over the same browser profile.

## Disclaimer
This tool is for personal automation and development purposes. Please respect Google's [Terms of Service](https://policies.google.com/terms) and rate limits when using this library.

## License
This project is licensed under the MIT License. 
Copyright (c) 2026 [nestchao]. 
See the [LICENSE](LICENSE) file for details.