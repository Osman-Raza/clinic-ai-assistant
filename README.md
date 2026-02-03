# Cubhouse AI Chatbot

An AI-powered chatbot built to support a pediatric therapy clinic’s website by providing automated responses to common inquiries. The project demonstrates full-stack development, API integration, and production deployment of an AI-driven web feature.

## Overview

This chatbot was designed and implemented as part of a production web platform for Cubhouse Pediatric Therapy. It integrates OpenAI’s API to generate real-time conversational responses and is embedded directly into a public-facing website.

The project focuses on:
- Secure backend API handling
- Responsive frontend integration
- Clean, maintainable full-stack architecture
- Real-world deployment considerations

## Features

- AI-powered conversational responses using OpenAI’s API
- Custom prompt engineering for controlled, relevant outputs
- Python backend to securely manage API requests
- JavaScript-based frontend for real-time user interaction
- Responsive design for both mobile and desktop devices
- Deployed backend hosted on Render

## Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- Flask
- OpenAI API

**Deployment & Tools**
- Render (backend hosting)
- Git & GitHub
- Environment variables for secure API key management

## Architecture

- The frontend captures user input and sends requests to the backend via HTTP.
- The backend processes requests, communicates with the OpenAI API, and returns generated responses.
- API keys are stored securely using environment variables and are never exposed client-side.
- The chatbot UI is embedded directly into the production website.

## Setup & Installation

### Prerequisites
- Python 3.9+
- An OpenAI API key

### Clone the Repository
```bash
git clone https://github.com/Osman-Raza/clinic-ai-assistant.git
(create directory)
