# Linux Cluster Monitoring Agent

## Introduction
The Linux Cluster Monitoring Agent is a lightweight monitoring solution designed to collect and store hardware specifications and real-time resource usage metrics from Linux servers. The system uses Bash-based agents deployed on each node in a Linux cluster to periodically capture CPU, memory, and disk statistics and persist them into a centralized PostgreSQL database.

This project is intended for infrastructure teams, data engineers, and platform engineers who need basic observability into system health without relying on heavyweight monitoring tools. The solution is simple, portable, and easy to deploy, making it suitable for learning environments and small-scale infrastructure monitoring.

Technologies used in this project include Bash scripting, PostgreSQL, Docker, Linux system utilities, Git, and cron-based scheduling.

---

## Quick Start

```bash
# 1. Start PostgreSQL using Docker
./scripts/psql_docker.sh start

# 2. Create database tables
psql -h localhost -U postgres -d host_agent -f sql/ddl.sql

# 3. Insert hardware information (run once)
./scripts/host_info.sh localhost 5432 host_agent postgres password

# 4. Insert usage data (manual run)
./scripts/host_usage.sh localhost 5432 host_agent postgres password

# 5. Set up cron job (runs every minute)
crontab -e

Crontab entry
* * * * * /home/rocky/dev/jarvis_data_eng_Singh/linux_sql/scripts/host_usage.sh localhost 5432 host_agent postgres password >> /home/rocky/dev/jarvis_data_eng_Singh/linux_sql/logs/host_usage.log 2>&1

