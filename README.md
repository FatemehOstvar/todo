# FastAPI To-Do Application

This repository contains a simple web API for managing to-do items. The application is built using FastAPI, with PostgreSQL as the database engine. It is containerized with Docker and includes automated testing and continuous integration via GitHub Actions.

## Overview

This project demonstrates the following:

- A minimal REST API for CRUD operations on to-do tasks
- Use of FastAPI for building modern Python web applications
- Integration with PostgreSQL using environment-based configuration
- Docker-based setup for portability and reproducibility
- CI pipeline using GitHub Actions for testing and Docker image builds

## Architecture

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11 (optional for local testing outside of Docker)

### Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/FatemehOstvar/todo.git
cd todo
