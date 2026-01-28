#!/bin/bash

# host_info.sh: Collect host hardware info and insert into PostgreSQL
# Usage: ./host_info.sh psql_host psql_port db_name psql_user psql_password

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

# ---------- Collect hardware info ----------
hostname=$(hostname -f)
lscpu_out=$(lscpu)

cpu_number=$(echo "$lscpu_out" | egrep "^CPU\(s\):" | awk '{print $2}' | xargs)
cpu_architecture=$(echo "$lscpu_out" | egrep "^Architecture:" | awk '{print $2}' | xargs)
cpu_model=$(echo "$lscpu_out" | egrep "^Model name:" | sed 's/^Model name:\s*//' | xargs)

# Derive MHz from model string "@ 2.20GHz" -> 2200.000
cpu_mhz=$(echo "$lscpu_out" \
  | egrep "^Model name:" \
  | grep -oE '@[[:space:]]*[0-9]+\.[0-9]+GHz' \
  | grep -oE '[0-9]+\.[0-9]+' \
  | awk '{printf "%.3f", $1*1000}')

l2_cache=$(echo "$lscpu_out" | egrep "^L2 cache:" | awk '{print $3}' | xargs)
total_mem=$(grep "^MemTotal:" /proc/meminfo | awk '{print $2}' | xargs)
timestamp=$(date -u '+%F %T')

# ---------- Insert into DB ----------
insert_stmt="
INSERT INTO host_info (hostname, cpu_number, cpu_architecture, cpu_model, cpu_mhz, l2_cache, total_mem, \"timestamp\")
VALUES ('$hostname', $cpu_number, '$cpu_architecture', '$cpu_model', $cpu_mhz, $l2_cache, $total_mem, '$timestamp')
ON CONFLICT (hostname) DO NOTHING;
"

export PGPASSWORD="$psql_password"
psql -h "$psql_host" -p "$psql_port" -U "$psql_user" -d "$db_name" -c "$insert_stmt"

