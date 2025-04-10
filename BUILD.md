# BUILD.md

## Overview

This system includes:
- React frontend (Vite)
- FastAPI backend
- Ollama LLM integration
- MinIO for CSV file storage
- Docker Compose for orchestration
- CUDA/NVIDIA support for WSL2 (for Ollama)

## Prerequisites

- Docker & Docker Compose
- NVIDIA GPU with CUDA support (and WSL2 if on Windows)
- `nvidia-docker2` installed and configured

## Running the Project

1. **Build and Start the Containers:**

   ```bash
   docker-compose up --build
   ```

2. **Access the Services:**

   - Frontend: http://localhost:3000  
   - Backend API: http://localhost:8000  
   - MinIO Console: http://localhost:9000  

3. **Using the App:**

   - Upload a `.csv` file from the frontend UI.
   - Copy the returned file ID.
   - Enter your question and submit it.
   - The answer from the LLM will be displayed.

4. **Shut Down:**

   ```bash
   docker-compose down
   ```

## Configuration Notes

- Ensure the Ollama model container is correctly configured and running at `http://ollama:5000/api`.
- You can change the Ollama API URL via the `OLLAMA_API_URL` environment variable in the backend.

## Development Notes

- Frontend is located under `frontend/`
- Backend is located under `backend/`
- Dockerfiles are provided for both.
- The `docker-compose.yml` sets up networking and dependencies between services.