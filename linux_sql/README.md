# Linux Cluster Monitoring Agent

## Introduction
The **Linux Cluster Monitoring Agent** is a lightweight monitoring solution designed to collect and store hardware specifications and real-time resource usage metrics from Linux servers. The system uses Bash-based agents deployed on each node in a Linux cluster to periodically capture CPU, memory, and disk statistics and persist them into a centralized PostgreSQL database.

This project is intended for infrastructure teams, data engineers, and platform engineers who need basic observability into system health without relying on heavyweight monitoring tools. The solution is simple, portable, and easy to deploy, making it suitable for learning environments and small-scale infrastructure monitoring.

**Technologies used:** Bash scripting, PostgreSQL, Docker, Linux system utilities, Git, and `cron`.

---

## Architecture
The system follows a distributed agent-based architecture. Each Linux host runs local monitoring scripts that collect system metrics and hardware information. These agents send data to a centralized PostgreSQL database, which serves as the single source of truth.

The architecture supports multiple Linux hosts connecting to a single database instance, enabling horizontal scalability as new nodes are added.



---

## Quick Start

### 1. Start PostgreSQL using Docker
```bash
./scripts/psql_docker.sh start
```

## Create Database Tables
```bash
psql -h localhost -U postgres -d host_agent -f sql/ddl.sql
```
