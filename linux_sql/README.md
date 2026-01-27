# Linux Cluster Monitoring Agent

## Introduction
The **Linux Cluster Monitoring Agent** is a lightweight monitoring solution designed to collect and store hardware specifications and real-time resource usage metrics from Linux servers. The system uses Bash-based agents deployed on each node in a Linux cluster to periodically capture CPU, memory, and disk statistics and persist them into a centralized PostgreSQL database.

This project is intended for infrastructure teams, data engineers, and platform engineers who need basic observability into system health without relying on heavyweight monitoring tools. The solution is simple, portable, and easy to deploy, making it suitable for learning environments and small-scale infrastructure monitoring.

**Technologies used:** Bash scripting, PostgreSQL, Docker, Linux system utilities, Git, and `cron`.

---

## Quick Start

```bash
# Start PostgreSQL using Docker
./scripts/psql_docker.sh start

# Create database tables
psql -h localhost -U postgres -d host_agent -f sql/ddl.sql

# Insert hardware specifications (run once per host)
./scripts/host_info.sh localhost 5432 host_agent postgres password

# Insert resource usage data (manual run)
./scripts/host_usage.sh localhost 5432 host_agent postgres password

# Configure cron job for continuous monitoring
crontab -e
```
Example cron entry:
```bash
* * * * * /bin/bash /home/rocky/dev/jarvis_data_eng_Singh/linux_sql/scripts/host_usage.sh localhost 5432 host_agent postgres password >> /home/rocky/dev/jarvis_data_eng_Singh/linux_sql/logs/host_usage.log 2>&1
```
---

## Implementation

This project is implemented using Bash scripts for data collection and SQL for data persistence. Automation is achieved through Docker for database provisioning and Linux cron for scheduled execution. The design emphasizes simplicity, clarity, and reproducibility.

---

## Architecture

The system follows a distributed agent-based architecture. Each Linux host runs a local monitoring agent that collects system metrics and sends them to a centralized PostgreSQL database. The database acts as the single source of truth for both hardware specifications and runtime usage data.
Multiple Linux hosts can connect to the same database instance, allowing the system to scale horizontally. PostgreSQL runs inside a Docker container to ensure consistent deployment across environments.

An architecture diagram showing three Linux hosts, monitoring agents, and a centralized database was created using draw.io and is stored in the assets/ directory.

---

## Scripts

