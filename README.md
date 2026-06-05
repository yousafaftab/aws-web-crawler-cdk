# AWS Web Crawler Monitoring System

A production-grade, serverless web monitoring platform built with **AWS CDK (Python)**. The system continuously crawls a managed list of URLs, measures their availability and latency, publishes metrics to CloudWatch, triggers SNS alerts when thresholds are breached, and exposes a REST API for full CRUD management of monitored websites — all deployed and promoted through an automated CI/CD pipeline.

---

## Architecture

```
  GitHub (main)
       │
       ▼
  AWS CodePipeline
  ├── Unit Tests
  ├── Beta Stage (auto-deploy)
  ├── Integration Tests
  ├── Manual Approval Gate
  └── Prod Stage
            │
            ▼
  ┌─────────────────────────────────────────────────────────┐
  │                     AWS Cloud                           │
  │                                                         │
  │  HTTP Clients ──► API Gateway ──► Lambda (API Handler)  │
  │                                         │               │
  │                                  DynamoDB (URLs table)  │
  │                                         │               │
  │  EventBridge (every 10 min) ──► Lambda (Web Crawler) ───┘
  │                                         │               │
  │                              ┌──────────┴──────────┐    │
  │                              ▼                     ▼    │
  │                       CloudWatch              SNS Topic │
  │                    Metrics & Alarms         (Email Alert)│
  │                              │                          │
  │                       Lambda (DB Writer)                │
  │                              │                          │
  │                       DynamoDB (Alarms table)           │
  └─────────────────────────────────────────────────────────┘
```

---

## Features

- **REST CRUD API** — API Gateway backed by Lambda to add, retrieve, update, and delete monitored websites
- **Automated Web Crawling** — Lambda invoked every 10 minutes via EventBridge to check all registered URLs
- **Real-Time Metrics** — URL availability (up/down) and latency published to a custom CloudWatch namespace
- **Per-URL Alerting** — CloudWatch alarms per website with SNS email notifications on threshold breach
- **Alarm Persistence** — Runtime alarms written to a dedicated DynamoDB table via a triggered Lambda
- **Blue/Green Deployment** — CodeDeploy with a 50% linear rollout and automatic rollback on alarm breach
- **Full CI/CD Pipeline** — GitHub-triggered CodePipeline with unit tests, integration tests, and a manual approval gate between Beta and Prod

---

## Tech Stack

| Layer | Technology |
|---|---|
| Infrastructure as Code | AWS CDK v2 (Python) |
| Compute | AWS Lambda (Python 3.6) |
| API | Amazon API Gateway (REST) |
| Database | Amazon DynamoDB |
| Monitoring | Amazon CloudWatch |
| Notifications | Amazon SNS |
| Scheduling | Amazon EventBridge |
| Container Registry | Amazon ECR |
| Deployment | AWS CodeDeploy (Linear 50%) |
| CI/CD | AWS CodePipeline + GitHub |

---

## Project Structure

```
web_crawler/
├── app.py                          # CDK app entry point
├── sprint_4/
│   ├── sprint_4_stack.py           # Core infrastructure stack
│   ├── yousafPipelineStack.py      # CI/CD pipeline stack
│   └── stages_stack.py             # Pipeline stage definitions
├── resources/
│   ├── WHApihandler.py             # API Gateway Lambda — CRUD handler
│   ├── WHlambda.py                 # Web crawler Lambda — availability & latency
│   ├── DBlambda.py                 # Alarm persistence Lambda
│   ├── cloudwatch_putmetric.py     # CloudWatch metrics helper
│   ├── cloudwatch_putalarm.py      # CloudWatch alarms helper
│   └── constants.py                # Thresholds, namespaces, pipeline commands
├── tests/
│   ├── unit/                       # CDK stack unit tests
│   └── integration/                # HTTP endpoint integration tests
├── pyrest/                         # Dockerized REST API test suite
│   └── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

---

## API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/websites?websiteId={id}` | Retrieve a website record by ID |
| `POST` | `/websites` | Register a new website for monitoring |
| `PATCH` | `/websites` | Update a website record |
| `DELETE` | `/websites` | Remove a website from monitoring |
| `GET` | `/webcrawler` | Retrieve all monitored websites |

---

## Monitoring Thresholds

| Metric | Namespace | Condition | Action |
|---|---|---|---|
| `url_availability` | `YousafNameSpace` | < 1.0 (site down) | SNS email alert |
| `url_latency` | `YousafNameSpace` | > 0.6 seconds | SNS email alert |

---

## Prerequisites

- Python >= 3.6
- Node.js >= 14
- AWS CDK CLI: `npm install -g aws-cdk`
- AWS CLI configured with sufficient permissions
- A GitHub personal access token stored in AWS Secrets Manager as `github-token_yousaf`
- AWS environment bootstrapped: `cdk bootstrap aws://<account-id>/<region>`

---

## Deployment

```bash
# Clone the repository
git clone <repo-url>
cd web_crawler

# Install Python dependencies
pip install -r requirements.txt

# Bootstrap your AWS environment (first time only)
cdk bootstrap aws://<account-id>/<region>

# Deploy the pipeline
cdk deploy YousafPipeline
```

Once deployed, every push to the `main` branch automatically triggers the CodePipeline.

---

## Running Tests

```bash
# Unit tests
pytest tests/unit/test_sprint_4_stack.py

# Integration tests (requires a deployed stack)
pytest tests/integration/test_httpreq_dynamodb.py
```

---

## Cleanup

```bash
cdk destroy YousafPipeline
```

> All Lambda functions, DynamoDB tables, and the ECR repository are configured with `RemovalPolicy.DESTROY` and will be removed when the stack is torn down.
