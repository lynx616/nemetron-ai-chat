# Nemotron AI Chat

A simple full-stack AI chat application built with **React + Vite** on the frontend and **FastAPI + Python** on the backend, using NVIDIA's **Nemotron 3 Ultra** model through the NVIDIA API.

The project is intended as a learning-friendly example of connecting a React chat UI to a Python API and an LLM provider.

## Tech Stack

### Frontend
- React 19
- Vite 8
- JavaScript
- Fetch API

### Backend
- Python
- FastAPI
- Uvicorn
- OpenAI Python SDK
- python-dotenv
- NVIDIA NIM API

### AI Model
- `nvidia/nemotron-3-ultra-550b-a55b`

## How It Works Till now

The request flow is:

```text
React Chat UI
      │
      │ POST /chat
      ▼
FastAPI Backend
      │
      │ NVIDIA API request
      ▼
Nemotron 3 Ultra
      │
      │ AI response
      ▼
FastAPI
      │
      ▼
React Chat UI
```

## Prerequisites

Install these before starting:

- **Python 3.11+**
- **Node.js 18+**
- **npm**
- A **NVIDIA API key** with access to the configured Nemotron model
- **Git**

> Python 3.11 or 3.12 is recommended for a smooth local setup.

## 1. Clone the Repository

```bash
git clone https://github.com/lynx616/nemetron-ai-chat.git
cd nemetron-ai-chat
```

## 2. Set Up the Backend

Open a terminal in the repository root and move into the backend directory:

```bash
cd backend
```

### Create a virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
```

If `py -3.11` is not available, use the Python version installed on your machine, for example:

```powershell
py -3.12 -m venv .venv
```

macOS/Linux:

```bash
python3 -m venv .venv
```

### Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

### Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The backend dependencies are pinned in `backend/requirements.txt`, including FastAPI, Uvicorn, the OpenAI SDK, and `python-dotenv`.

## 3. Configure the NVIDIA API Key

Create a file named `.env` inside the `backend` directory:

```text
backend/.env
```

Add:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

Do **not** commit this file to GitHub. Keep API keys private.

The backend reads the key with `python-dotenv` and uses the NVIDIA-compatible OpenAI client endpoint:

```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)
```

## 4. Start the Backend

From the `backend` directory, with the virtual environment activated:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### API Endpoint

The chat endpoint is:

```text
POST /chat
```

Request body:

```json
{
  "message": "Hello, how are you?"
}
```

Response:

```json
{
  "response": "..."
}
```

## 5. Set Up the Frontend

Open a **second terminal** and return to the project root:

```bash
cd nemetron-ai-chat/frontend
```

Install the JavaScript dependencies:

```bash
npm install
```

## 6. Start the Frontend

Run the Vite development server:

```bash
npm run dev
```

Vite will normally start the app at:

```text
http://localhost:5173
```

Open that address in your browser.

## 7. Run the Full App

You need **two terminals** running at the same time.

### Terminal 1 — Backend

```bash
cd nemetron-ai-chat/backend

# Windows PowerShell
.venv\Scripts\Activate.ps1

uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd nemetron-ai-chat/frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```


The frontend sends the user's message to the backend. The backend adds a system message, sends the conversation to NVIDIA's API, and returns the model response to the frontend.

## Environment Variables

The backend currently expects:

| Variable | Required | Description |
|---|---|---|
| `NVIDIA_API_KEY` | Yes | API key used to access NVIDIA's API |

Example:

```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxx
```

## Available Frontend Scripts

Run these from `frontend/`:

```bash
npm run dev
```

Starts the Vite development server.

```bash
npm run build
```

Creates a production build.

```bash
npm run preview
```

Previews the production build locally.

```bash
npm run lint
```

Runs ESLint.

## Troubleshooting

### `py -3.11` or `python` is not recognized

Check installed Python versions:

```powershell
py --list
```

Then create the virtual environment with one of the installed versions, for example:

```powershell
py -3.12 -m venv .venv
```

### PowerShell blocks virtual environment activation

You may need to allow locally created scripts for your user account:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

### Frontend cannot connect to the backend

Make sure the FastAPI server is running on port `8000`:

```bash
uvicorn app.main:app --reload --port 8000
```

The frontend is configured to call:

```text
http://127.0.0.1:8000/chat
```

Also make sure the frontend is running on:

```text
http://localhost:5173
```

The backend CORS configuration allows that frontend origin.

### AI request fails

Check that:

1. `backend/.env` exists.
2. `NVIDIA_API_KEY` is set correctly.
3. Your NVIDIA API key has access to the configured model.
4. The backend terminal does not show an API or authentication error.

### Port already in use

Start the backend on another port if necessary:

```bash
uvicorn app.main:app --reload --port 8001
```

If you change the backend port, also update the frontend API URL in `frontend/src/layouts/ChatBox.jsx`.

## Security Notes

- Never commit `.env` files containing secrets.
- Never expose your NVIDIA API key in frontend code.
- Keep provider API calls on the backend.
- Use environment variables for secrets rather than hard-coding them.
- For production, replace development CORS settings with your actual frontend domain.

## Development Notes

This project is currently a simple single-message chat implementation. The backend sends a system prompt plus the latest user message to Nemotron. Conversation history is kept in the frontend UI, but the complete previous conversation is not currently sent back to the model on every request.

## License

No license is currently specified for this repository.

## Author

Built by [@lynx616](https://github.com/lynx616).
