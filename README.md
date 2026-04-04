# Ekklesia
## Overview

**Ekklesia** helps churches stay connected with their members, even across long distances. Many churches in developing countries still rely on paper-based announcements, leaving members out of the loop if they miss services or don’t have direct contacts.

Ekklesia solves this by combining:

- A **Telegram bot** (soon WhatsApp) for members to receive updates and interact with their church
- A **web-based admin dashboard** for church leaders to manage events, content, and member data

**Key benefits**:

- Instant, real-time updates for members
- Access to church info from anywhere in the world
- Analytics for admins: `quiz results`, `event attendance`, `child dedications`, `marriages`, and other member activities.

## Project Proposal
Read the project proposal [here](docs//project_proposal.md)

## Architecture Overview
Read the architecture overview [here](docs//architectural_design.md)

## 🚀 5. Getting Started (Quick Start)
clone the repo and install packages with uv.

```sh
uv sync
```

### Backend
Thie will run fastapi on port `8002`
```sh
cd backend
# uv run uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 1 --reload
make dev 
```

### Polling
Since we are running locally, for telegram to work, we need to run a polling
```sh
cd backend
# uv run python -m app.bot.polling
make polling
```

###  Admin
This will run Python reflex
```sh
cd admin
# uv run reflex run --loglevel debug
make run
```