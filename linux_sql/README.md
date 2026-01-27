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
`psql_docker.sh`
Manages the PostgreSQL database using Docker. This script simplifies database startup and shutdown and ensures a consistent runtime environment.
```bash
./scripts/psql_docker.sh start
./scripts/psql_docker.sh stop
```
`host_info.sh`
Collects static hardware information such as CPU configuration, memory size, and hostname. Since hardware rarely changes, this script is executed once per host.
```bash
./scripts/host_info.sh psql_host psql_port db_name psql_user psql_password
```
`host_usage.sh`
Collects dynamic system metrics including memory usage, CPU utilization, disk I/O, and available disk space. This script is designed to run repeatedly.
```bash
./scripts/host_usage.sh psql_host psql_port db_name psql_user psql_password
```
`crontab`
Linux cron is used to automate execution of host_usage.sh every minute, enabling continuous monitoring without manual intervention.

`queries.sql`
Contains analytical SQL queries that support operational analysis, such as identifying resource-intensive hosts and calculating average resource usage over time.

---

## Database Modeling

`host_info`
| Column Name      | Description                     |
| ---------------- | ------------------------------- |
| id               | Unique identifier for each host |
| hostname         | Fully qualified hostname        |
| cpu_number       | Number of CPU cores             |
| cpu_architecture | CPU architecture type           |
| cpu_model        | CPU model name                  |
| cpu_mhz          | CPU speed in MHz                |
| l2_cache         | L2 cache size (KB)              |
| total_mem        | Total memory (KB)               |
| timestamp        | Record creation time (UTC)      |

`host_usage`
| Column Name    | Description                     |
| -------------- | ------------------------------- |
| timestamp      | Time of metric collection (UTC) |
| host_id        | Reference to host_info table    |
| memory_free    | Free memory (MB)                |
| cpu_idle       | CPU idle percentage             |
| cpu_kernel     | CPU kernel usage percentage     |
| disk_io        | Disk I/O in progress            |
| disk_available | Available disk space (MB)       |

---

## Test
The Bash scripts and database DDL were tested manually on a Linux virtual machine. Testing steps included verifying database and table creation, validating schema definitions, executing scripts manually, and confirming successful data insertion.

Cron execution was validated by observing continuous row growth in the `host_usage` table and reviewing log files to ensure scripts executed successfully at one-minute intervals.

---

## Deployment
The application was deployed using Git for version control, Docker to provision the PostgreSQL database, and Linux cron for task automation. Monitoring scripts were executed directly on the Linux host, and scheduled cron jobs enabled continuous data collection without manual execution.

---

## Improvements
Potential future improvements include

* Add automatic detection of hardware configuration changes
* Implement alerting for abnormal resource usage patterns
* Introduce data retention and cleanup policies
* Improve error handling and logging across scripts

