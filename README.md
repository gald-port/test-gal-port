# FastAPI Server

A simple FastAPI server with basic API endpoints, health checks, logging, CORS, and error handling.

## Requirements

- Python 3.10+
- pip

## Installation

```bash
pip install fastapi uvicorn

Run
python main.py


The server will start at:

http://localhost:8000

API Documentation

FastAPI provides automatic API documentation:

http://localhost:8000/docs


Alternative documentation:

http://localhost:8000/redoc

Endpoints
Method	Endpoint	Description
GET	/	Server information
GET	/health	Health check
GET	/api	API status
GET	/api/status	Detailed API status
GET	/api/hello	Hello message
POST	/api/data	Receive JSON data
Example
curl http://localhost:8000/health


Response:

{
  "status": "ok",
  "uptime": 12.34
}

Project Structure
.
├── main.py
└── README.md

