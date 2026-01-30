#!/bin/bash

# host_usage.sh: Collect host usage info and insert into PostgreSQL
# Usage: ./host_usage.sh psql_host psql_port db_name psql_user psql_password

set -euo pipefail

if [ $# -ne 5 ]; then
  echo "ERROR: Invalid number of arguments"
  echo "Usage: $0 psql_host psql_port db_name psql_user psql_password"
  exit 1
fi

psql_host=$1
psql_port=$2
db_name=$3
psql_user=$4
psql_password=$5

hostname=$(hostname -f)
timestamp=$(date -u '+%F %T')

export PGPASSWORD="$psql_password"

# Find host_id from host_info
host_id=$(psql -h "$psql_host" -p "$psql_port" -U "$psql_user" -d "$db_name" -t -c \
  "SELECT id FROM host_info WHERE hostname='$hostname';" | xargs)

if [ -z "$host_id" ]; then
  echo "ERROR: host_id not found for hostname=$hostname. Run host_info.sh first."
  exit 1
fi

# Collect usage metrics
vmstat_out=$(vmstat --unit M)

memory_free=$(echo "$vmstat_out" | tail -1 | awk '{print $4}' | xargs)
cpu_kernel=$(echo "$vmstat_out" | tail -1 | awk '{print $14}' | xargs)
cpu_idle=$(echo "$vmstat_out" | tail -1 | awk '{print $15}' | xargs)

disk_io=$(vmstat -d | tail -1 | awk '{print $10}' | xargs)
disk_available=$(df -BM / | tail -1 | awk '{print $4}' | sed 's/M//' | xargs)

insert_stmt="
INSERT INTO host_usage (\"timestamp\", host_id, memory_free, cpu_idle, cpu_kernel, disk_io, disk_available)
VALUES ('$timestamp', $host_id, $memory_free, $cpu_idle, $cpu_kernel, $disk_io, $disk_available);
"

psql -h "$psql_host" -p "$psql_port" -U "$psql_user" -d "$db_name" -c "$insert_stmt"

