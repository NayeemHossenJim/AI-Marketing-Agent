# AI Marketing Agent

AI-powered marketing Agent system built with Python, FastAPI, SQLite, and Groq.

The application can create marketing campaigns, generate marketing text using Groq, generate a marketing image URL, schedule campaigns, and simulate sending marketing messages to a phone number.

## Features

* Create marketing campaigns
* Store campaign data in SQLite
* Generate marketing text using Groq LLM
* Generate mock marketing image URL
* Send campaign message immediately
* Automatically send scheduled campaigns
* Support multiple campaigns
* REST API using FastAPI
* Logging support
* Docker support

## Technology Stack

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Groq
* Uvicorn

## Project Structure

```text
ai-marketing-automation/
├── app/
│   ├── api/
│   │   └── campaign_routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   ├── models/
│   │   └── campaign.py
│   ├── repositories/
│   │   └── campaign_repository.py
│   ├── schemas/
│   │   └── campaign.py
│   ├── services/
│   │   ├── campaign_service.py
│   │   ├── image_generator.py
│   │   ├── scheduler_service.py
│   │   ├── sms_sender.py
│   │   └── text_generator.py
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Requirements

Make sure Python is installed.

Recommended version:

```bash
python --version
```

Use Python 3.10 or higher.

## Setup Instructions

### 1. Clone or open the project folder

```bash
cd ai-marketing-agent
```

### 2. Create a virtual environment

For Windows:

```bash
python -m venv .venv
```

For Mac/Linux:

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

For Windows CMD:

```bash
.venv\Scripts\activate
```

For Windows Git Bash:

```bash
source .venv/Scripts/activate
```

For Mac/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the environment file

Copy `.env.example` and rename it to `.env`.

For Windows CMD:

```bash
copy .env.example .env
```

For Git Bash or Mac/Linux:

```bash
cp .env.example .env
```

### 6. Add Groq API key

Open `.env` and update the value:

```env
APP_NAME=AI Marketing Automation
DATABASE_URL=sqlite:///./campaigns.db
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
SCHEDULER_INTERVAL_SECONDS=5
```

If `GROQ_API_KEY` is missing, the app will still work with fallback marketing text.

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The app will run at:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint                            | Description                 |
| ------ | ----------------------------------- | --------------------------- |
| GET    | `/health`                           | Check if the app is running |
| POST   | `/campaigns`                        | Create a campaign           |
| GET    | `/campaigns`                        | List all campaigns          |
| GET    | `/campaigns/{campaign_id}`          | Get a single campaign       |
| POST   | `/campaigns/{campaign_id}/send-now` | Send a campaign immediately |

## How to Test

### 1. Health check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### 2. Create a campaign

Use a future `schedule_time`.

```bash
curl -X POST "http://127.0.0.1:8000/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "AI Course Launch",
    "prompt": "Promote our new AI course",
    "phone": "01913828774",
    "schedule_time": "2026-06-17 15:30:00"
  }'
```

Expected response:

```json
{
  "id": 1,
  "campaign_name": "AI Course Launch",
  "prompt": "Promote our new AI course",
  "phone": "01913828774",
  "schedule_time": "2026-06-17T15:30:00",
  "generated_text": null,
  "generated_image_url": null,
  "status": "pending",
  "error_message": null,
  "created_at": "2026-06-17T09:51:14.089835",
  "sent_at": null
}
```

At this stage, `generated_text` and `generated_image_url` are `null` because the campaign has only been created. It has not been sent yet.

### 3. List campaigns

```bash
curl "http://127.0.0.1:8000/campaigns"
```

Expected response:

```json
[
  {
    "id": 1,
    "campaign_name": "AI Course Launch",
    "prompt": "Promote our new AI course",
    "phone": "01913828774",
    "schedule_time": "2026-06-17T15:30:00",
    "generated_text": null,
    "generated_image_url": null,
    "status": "pending",
    "error_message": null,
    "created_at": "2026-06-17T09:51:14.089835",
    "sent_at": null
  }
]
```

### 4. Send campaign immediately

```bash
curl -X POST "http://127.0.0.1:8000/campaigns/1/send-now"
```

Expected response:

```json
{
  "id": 1,
  "campaign_name": "AI Course Launch",
  "prompt": "Promote our new AI course",
  "phone": "01913828774",
  "schedule_time": "2026-06-17T15:30:00",
  "generated_text": "Unlock the future with our new AI course! Learn from experts and boost your career. Limited spots available. Enroll now!",
  "generated_image_url": "https://dummyimage.com/1024x1024/111827/ffffff.png&text=Promote+our+new+AI+course",
  "status": "sent",
  "error_message": null,
  "created_at": "2026-06-17T09:51:14.089835",
  "sent_at": "2026-06-17T09:52:02.365956"
}
```

Expected console output:

```text
Sending marketing message to 01913828774
Campaign: AI Course Launch
Generated Text:
Unlock the future with our new AI course! Learn from experts and boost your career. Limited spots available. Enroll now!
Generated Image:
https://dummyimage.com/1024x1024/111827/ffffff.png&text=Promote+our+new+AI+course
```

### 5. Test automatic scheduled sending

Create a campaign with a schedule time close to the current time.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Flash Sale",
    "prompt": "Promote a 50 percent discount on online courses",
    "phone": "01913828774",
    "schedule_time": "2026-06-17 10:05:00"
  }'
```

Keep the server running.

The scheduler checks pending campaigns every few seconds. When the scheduled time arrives, the app will automatically generate the text, generate the image URL, print the simulated SMS output, and update the campaign status to `sent`.

Check the campaign list again:

```bash
curl "http://127.0.0.1:8000/campaigns"
```

The campaign status should change from:

```text
pending
```

to:

```text
sent
```


## Common Problems

### Server is not starting

Make sure the virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### Groq is not generating text

Check if `GROQ_API_KEY` is added correctly in `.env`.

If the key is missing or invalid, the project will use fallback text.

### Campaign is still pending

Check that the schedule time has already arrived.

Also keep the server running because the scheduler works while the app is running.

### Port already in use

Run the app on another port:

```bash
uvicorn app.main:app --reload --port 8001
```
