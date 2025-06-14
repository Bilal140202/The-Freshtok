# TikTok Latest Tracker

This project is a tool to find and display the latest TikTok posts based on a search query.

## Development

This project is set up to be developed in GitHub Codespaces.

- The backend is a FastAPI application located in the `backend` directory.
- The frontend is a React application (using Vite) located in the `frontend` directory.

### Running Locally (within Codespaces)

The dev container is configured to:
1. Install Python dependencies from `backend/requirements.txt`.
2. Install Node.js dependencies from `frontend/package.json`.
3. Install Playwright and its browser dependencies.
4. Forward ports `8000` (backend) and `5173` (frontend).

To run the backend:
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

To run the frontend:
```bash
cd frontend
npm run dev
```
