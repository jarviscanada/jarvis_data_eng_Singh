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

Implementation

This project is implemented using Bash scripts to collect system metrics and SQL to persist and analyze the data. Automation is achieved through Docker for database provisioning and cron for scheduled execution of monitoring scripts.

Architecture

The system follows a distributed agent-based architecture. Each Linux host runs local monitoring scripts that collect system metrics. These agents send data to a centralized PostgreSQL database, which acts as the single source of truth for hardware and usage information.

The architecture supports multiple Linux hosts connecting to one database instance, allowing the solution to scale horizontally as more nodes are added.

An architecture diagram illustrating multiple Linux hosts, monitoring agents, and a centralized PostgreSQL database was created using draw.io and is stored in the assets directory.

Scripts
psql_docker.sh

This script manages a PostgreSQL instance using Docker. It abstracts database startup and shutdown, ensuring a consistent and reproducible database environment.
./scripts/psql_docker.sh start|stop

host_info.sh

Collects static hardware information such as CPU configuration, cache size, memory size, and hostname. This script is designed to run once per host since hardware specifications are assumed to be static.
host_info.sh
./scripts/host_info.sh psql_host psql_port db_name psql_user psql_password

host_usage.sh

Collects dynamic system metrics including free memory, CPU idle percentage, CPU kernel usage, disk I/O, and available disk space. This script is designed to run repeatedly.
./scripts/host_usage.sh psql_host psql_port db_name psql_user psql_password

crontab

Linux cron is used to schedule host_usage.sh to run every minute. This enables continuous data collection without manual intervention.

queries.sql

This file contains analytical SQL queries used to answer operational questions such as identifying hosts with high resource usage, calculating average memory consumption over time, and monitoring overall cluster health.

Database Modeling
host_info
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

host_usage
| Column Name    | Description                     |
| -------------- | ------------------------------- |
| timestamp      | Time of metric collection (UTC) |
| host_id        | Reference to host_info table    |
| memory_free    | Free memory (MB)                |
| cpu_idle       | CPU idle percentage             |
| cpu_kernel     | CPU kernel usage percentage     |
| disk_io        | Disk I/O in progress            |
| disk_available | Available disk space (MB)       |


Test

The Bash scripts and database DDL were tested manually on a Linux virtual machine. Testing steps included verifying database and table creation, confirming schema correctness, executing scripts manually, and validating successful data insertion into the database.

Cron execution was verified by observing periodic row growth in the host_usage table and reviewing log files to confirm successful insert operations every minute.

Deployment

The application was deployed using Git for source control, Docker to provision the PostgreSQL database, and cron for task automation. Monitoring scripts were executed directly on the Linux host, and scheduled cron jobs ensured continuous monitoring without manual execution.

Improvements

Support automatic detection and handling of hardware configuration changes

Add alerting mechanisms for abnormal resource usage

Implement data retention and cleanup policies

Improve error handling and logging in monitoring scripts
