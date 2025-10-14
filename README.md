# Pipeline for Energy and Emission Monitoring During AI Model Training

## Overview
This project aims to build a Big Data pipeline that monitors energy consumption and CO₂ emissions during AI model training. 
Instead of using external tools such as CodeCarbon, we design a custom, distributed monitoring system that collects, processes, 
and stores relevant hardware and runtime metrics in real-time.

The project aligns with the Big Data Storage and Processing course objectives — implementing a complete end-to-end data pipeline 
using Apache Kafka, Apache Spark, and a NoSQL database under a Kappa Architecture.

## Problem Definition
AI model training is computationally intensive, and energy costs are often invisible. 
Currently, there is no unified, transparent system that tracks how much energy (and resulting emissions) is used per training run, per user, or per model.

This project addresses that gap by creating a scalable data pipeline that:
- Continuously collects low-level system metrics (CPU, GPU, RAM, etc.)
- Calculates energy and CO₂ consumption in near real time
- Stores and visualizes this information for sustainability tracking and optimization

## Objectives
- Design a Kappa-based streaming pipeline for energy/emission monitoring.
- Collect relevant system, model, and user metrics during AI training.
- Process and aggregate data using Spark Structured Streaming.
- Store results in NoSQL and distributed storage.
- Visualize emissions and training efficiency across runs and users.

## Architecture Overview (Kappa Model)
```
 ┌───────────────────────────────────────────────────────┐
 │                   Metrics Collector                   │
 │  (psutil, pynvml, system data → JSON messages)        │
 └───────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌───────────────────────────────────────────────────────┐
 │                Apache Kafka (Ingestion)               │
 │  Receives metric events from multiple training runs   │
 └───────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌───────────────────────────────────────────────────────┐
 │         Spark Structured Streaming (Processing)       │
 │  - Parse JSON messages                                │
 │  - Aggregate energy/CO₂ over time and users           │
 │  - Join with reference data (carbon intensity)        │
 └───────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌───────────────────────────────────────────────────────┐
 │            NoSQL Database (e.g., MongoDB)             │
 │  - Stores processed metrics for visualization         │
 └───────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌───────────────────────────────────────────────────────┐
 │          Visualization Dashboard (Streamlit)          │
 │  - Displays CO₂ emissions per run, per user           │
 │  - Trends, energy efficiency, hotspots                │
 └───────────────────────────────────────────────────────┘
```

## Main Components
The project is structured into five main components, each representing one stage of the Kappa data flow architecture:

| Component | Description | Technologies |
|------------|--------------|---------------|
| **1. Metrics Collector** | Collects CPU, GPU, RAM, and other system metrics and sends them as JSON messages. | Python, psutil, pynvml, confluent-kafka |
| **2. Kafka Ingestion Layer** | Serves as the message broker that ingests metric streams from multiple users or machines. | Apache Kafka |
| **3. Spark Streaming Processor** | Processes incoming metric streams, computes energy and CO₂ usage, and aggregates results. | PySpark Structured Streaming |
| **4. Storage Layer** | Stores aggregated data for short-term and long-term analysis. | MongoDB (hot data), HDFS (cold data) |
| **5. Visualization Dashboard** | Displays energy and emission metrics interactively. | Streamlit |

## Team Roles and Responsibilities
The group consists of five members, each responsible for one main component of the pipeline. This allows for modular development and parallel progress.

| Role | Responsibility | Short-Term Goals (Week 1–2) |
|------|----------------|-------------------------------|
| **Team Member A – Data Collector Developer** | Develops the Python-based system metrics collector. | Create a prototype that collects CPU/GPU/RAM data every few seconds and outputs JSON locally or to Kafka. |
| **Team Member B – Kafka Engineer** | Sets up and manages the Kafka broker and topics. | Deploy Kafka, create the topic `training.metrics`, and verify message ingestion. |
| **Team Member C – Spark Developer** | Implements the Spark Structured Streaming job. | Read test messages from Kafka or JSON files, perform initial transformations, and prepare aggregation logic. |
| **Team Member D – Storage Engineer** | Handles database and data model design. | Configure MongoDB and HDFS, define schema, and store test records. |
| **Team Member E – Visualization Engineer** | Builds the Streamlit dashboard. | Display example metrics from static JSON files to prepare for later MongoDB integration. |

## Parallel Development Strategy
Although the pipeline components are sequential, parallel development is enabled through simulation and modular design:

| Component | Independent Development Strategy |
|------------|----------------------------------|
| **Collector** | Can operate independently, saving JSON files locally before Kafka integration. |
| **Kafka** | Can be tested with manually produced JSON messages. |
| **Spark** | Can process static JSON files before connecting to Kafka. |
| **MongoDB** | Can be populated manually with test data to test queries and visualization. |
| **Dashboard** | Can display dummy data to finalize the UI before real data integration. |

## Development Plan (Two Weeks)
**Week 1: Local Prototypes**
- Collector produces JSON output with system metrics.
- Kafka runs locally and accepts test messages.
- Spark reads local JSON data and performs a simple aggregation.
- MongoDB schema and test insertions created.
- Streamlit dashboard visualizes static sample data.

**Week 2: Integration Phase**
- Connect Collector to Kafka.
- Integrate Kafka → Spark → MongoDB pipeline.
- Dashboard connects to MongoDB to show real-time updates.
- Add emission calculation and regional CO₂ intensity factors.

## What We Track — and Why
The following metrics are collected to understand hardware usage, energy draw, and contextual training details.

| Category | Example Metrics | Purpose |
|-----------|----------------|----------|
| CPU | Utilization %, Power (W), Core count | Estimate power draw from processor activity |
| GPU | Utilization %, Power (W), Memory usage | Measure major contributor to energy use |
| RAM | Used / Total memory | Understand memory load impact |
| IO / Network | Disk read/write, network traffic | Capture additional resource costs |
| System Info | Hostname, OS, Region | Context for grid intensity & configuration |
| Training Context | Run ID, User ID, Model name, Epoch | Enable per-run and per-user aggregation |
| CO₂ Intensity | g CO₂ / kWh (by region) | Convert energy to emissions |
| Timestamps | UTC time | Enable time series analysis |

## Data Flow & Processing
1. **Metrics Collector**  
   Collects local system metrics and sends JSON messages to Kafka (`training.metrics`).

2. **Kafka (Ingestion Layer)**  
   Acts as a distributed buffer for metric streams from multiple machines or users.

3. **Spark Structured Streaming**  
   Reads Kafka messages, performs windowed aggregations, computes energy (kWh) and emissions (kg CO₂), and writes results to MongoDB.

4. **Storage Layer**  
   MongoDB for recent data (hot storage) and HDFS for historical data (cold storage).

5. **Visualization Layer**  
   Streamlit dashboard showing per-user and per-run energy consumption and emissions.

## Data Schema (Spark)
| Column | Type | Description |
|--------|------|-------------|
| timestamp | Timestamp | Measurement time |
| run_id | String | Training run identifier |
| user_id | String | User who started training |
| cpu_utilization_pct | Double | CPU load |
| gpu_power_w | Double | GPU energy draw |
| ram_used_mb | Double | RAM usage |
| energy_kwh | Double | Estimated energy used |
| emissions_kg | Double | Estimated CO₂ emissions |
| region_iso | String | Country code |
| model_name | String | Model under training |

## Technology Stack
| Layer | Technology | Purpose |
|-------|-------------|----------|
| Ingestion | Apache Kafka | Distributed message queue |
| Processing | Apache Spark (PySpark) | Real-time stream processing |
| Storage | MongoDB / HDFS | Hot and cold data storage |
| Visualization | Streamlit | Dashboard for emissions & energy |
| Monitoring | Prometheus (optional) | System metrics tracking |
| Deployment | Kubernetes | Container orchestration |

## Current Progress
- Defined project concept and data model  
- Designed Kappa architecture  
- Drafted metrics collector (Python prototype)  
- Next steps: Implement Kafka ingestion, Spark consumer, and visualization

## References
- CodeCarbon GitHub Repository: https://github.com/mlco2/codecarbon  
- Apache Spark Structured Streaming Guide: https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html  
- ElectricityMap Carbon Intensity API: https://api.electricitymap.org/
