# 🌍 Pipeline for Energy and Emission Monitoring During AI Model Training

## 🧭 1. Problem Definition
### Selected Problem
Modern AI models consume substantial amounts of computational power and energy, leading to high CO₂ emissions. However, there is a lack of continuous and scalable monitoring systems that track energy usage and environmental impact during model training.

### Suitability for Big Data
- Continuous monitoring of hardware metrics (GPU, CPU, IO, network, etc.) produces **high-frequency time-series data**.  
- Each training run can generate **thousands of data points per second** across distributed nodes.  
- Real-time ingestion, aggregation, and visualization of these metrics require **streaming data pipelines** and **scalable storage systems**.  

This makes the problem highly suitable for a **Big Data processing architecture**, where Spark, Kafka, and NoSQL technologies can be applied.

### Scope and Limitations
- Focus on real-time ingestion and processing of monitoring data.  
- Simulated or small-scale real hardware metrics during development.  
- Out of scope: model training optimization itself (focus is on monitoring infrastructure).  

---

## 2. Architecture and Design

### 2.1 Architecture Model: **Kappa Architecture**
The system is designed following the **Kappa Architecture**, as all data (historical and live) is processed via a unified stream-processing pipeline.

### 2.2 High-Level Overview
```
          ┌────────────────────────────────────────┐
          │   Training Environment (PyTorch, etc.) │
          │ Generates real-time hardware metrics   │
          └────────────────────────────────────────┘
                             │
                             ▼
          ┌────────────────────────────────────────┐
          │ Data Ingestion Layer (Kafka Producer)   │
          │ Collects metrics (CPU, GPU, power, etc.)│
          └────────────────────────────────────────┘
                             │
                             ▼
          ┌────────────────────────────────────────┐
          │ Data Processing Layer (Spark Streaming) │
          │ - Parses JSON from Kafka                │
          │ - Calculates energy & CO₂ emissions     │
          │ - Performs windowed aggregations        │
          └────────────────────────────────────────┘
                             │
                             ▼
          ┌────────────────────────────────────────┐
          │ Data Storage Layer                      │
          │ - Hot data: MongoDB / Cassandra (NoSQL) │
          │ - Cold data: HDFS (Parquet)             │
          └────────────────────────────────────────┘
                             │
                             ▼
          ┌────────────────────────────────────────┐
          │ Visualization Layer (Streamlit / Grafana)│
          │ Real-time dashboard & aggregated reports │
          └────────────────────────────────────────┘
```

---

## 3. Data Design and Processing

### 3.1 Data Ingestion
- Metrics are collected from the **training environment** using Python scripts.  
- Each record (JSON) includes:
  ```json
  {
    "timestamp": "2025-10-13T12:34:56Z",
    "run_id": "run_2025_10_13_1234",
    "gpu_power_w": 128.4,
    "gpu_utilization_pct": 92.1,
    "cpu_power_w": 75.2,
    "region_iso": "DEU",
    "grid_carbon_intensity_g_per_kwh": 420
  }
  ```
- Records are sent to **Kafka** via a producer.

### 3.2 Data Processing (Apache Spark)
Using **Structured Streaming**, Spark consumes data from Kafka and performs:
- **Window aggregations** (e.g., total energy per 5-second window)  
- **Custom UDFs** to compute energy and CO₂ values:
  ```python
  energy_kwh = power_w * delta_t / 3_600_000
  co2_kg = energy_kwh * grid_carbon_intensity / 1000
  ```
- **Advanced transformations**: joins with grid emission data, pivot by device type, and cumulative totals.  
- **Watermarking** ensures proper handling of late data.

### 3.3 Data Storage
| Type | Technology | Purpose |
|------|-------------|----------|
| **Hot Storage** | MongoDB / Cassandra | Real-time queries and dashboards |
| **Cold Storage** | HDFS (Parquet) | Historical analytics and ML-based forecasting |
| **Schema Registry** | Kafka + Avro | Defines and validates message structure |

Partitioning Strategy:
- Partition by `run_id` and date (`YYYY-MM-DD`)  
- Bucketing by `region_iso` for fast aggregation  

### 3.4 Data Visualization
The dashboard displays:
- Total energy and emissions per run  
- Real-time power and CO₂ curves  
- Comparisons across models, hardware, and regions  
- Exportable reports (PDF/CSV)

Tools: **Streamlit**, **Grafana**, or **Kibana**.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Data Ingestion | Apache Kafka | Real-time message streaming |
| Processing | Apache Spark (PySpark) | Structured streaming and batch aggregation |
| Storage | HDFS (cold) + MongoDB (hot) | Persistent and scalable storage |
| Visualization | Streamlit / Grafana | Dashboard and analytics |
| Deployment | Kubernetes | Scalable cluster management |
| Monitoring | Prometheus + Grafana | System metrics and logs |

---

## 📊 5. Example Data Flow (End-to-End)
```
Training Script → Kafka Producer → Kafka Topic
→ Spark Structured Streaming → Energy/CO₂ computation
→ MongoDB (real-time) + HDFS (batch storage)
→ Streamlit Dashboard for visualization
```

### Example Aggregation Query (Spark SQL)
```sql
SELECT
  run_id,
  window(timestamp, "5 minutes").start AS window_start,
  SUM(energy_kwh) AS total_energy,
  SUM(co2_kg) AS total_emissions
FROM energy_stream
GROUP BY run_id, window(timestamp, "5 minutes")
ORDER BY window_start;
```

---

## 6. Current Progress

| Area | Description | Status |
|------|--------------|--------|
| Topic definition | Energy & emission monitoring pipeline | done |
| Architecture design | Defined end-to-end data flow | in progress |
| Tech stack selection | Spark, Kafka, MongoDB, HDFS | in progress |
| Data ingestion script | Produces mock training metrics | Planned |
| Spark streaming setup | Prototype under testing | Planned |
| Visualization | Basic Streamlit dashboard | Planned |

---

## 7. Next Steps
1. Implement **Kafka producers** to simulate multiple training nodes.  
2. Build the **Spark Structured Streaming job** to process metrics in real-time.  
3. Store aggregated results in **MongoDB** and raw data in **HDFS**.  
4. Develop **Streamlit dashboard** for visualization and analytics.  
5. Containerize the system and deploy it on **Kubernetes** for scalability.  

---

## 8. Lessons to Document Later
As development progresses, the following lesson categories will be documented:
- **Data Ingestion:** handling streaming metrics and schema evolution  
- **Data Processing:** Spark performance tuning and window aggregations  
- **Data Storage:** partitioning strategies and compression formats  
- **System Integration:** scaling Kafka & Spark clusters under Kubernetes  
- **Monitoring:** pipeline observability using Prometheus + Grafana  

---

## 9. Long-Term Vision
The final goal is a **real-time sustainability monitoring platform** capable of:
- Tracking emissions from distributed AI training systems  
- Supporting multiple data centers and hardware configurations  
- Providing analytics and optimization insights based on energy efficiency  

This project will demonstrate **end-to-end Big Data pipeline design**—from ingestion to visualization—while addressing a **real-world sustainability problem** in AI research.
