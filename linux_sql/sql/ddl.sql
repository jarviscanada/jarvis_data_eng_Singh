-- ddl.sql: create tables for Linux Cluster Monitoring (run against host_agent)

CREATE TABLE IF NOT EXISTS host_info (
  id SERIAL PRIMARY KEY,
  hostname VARCHAR(255) UNIQUE NOT NULL,
  cpu_number SMALLINT NOT NULL,
  cpu_architecture VARCHAR(50) NOT NULL,
  cpu_model VARCHAR(255) NOT NULL,
  cpu_mhz NUMERIC(10,3) NOT NULL,
  l2_cache INT NOT NULL,              -- KiB
  total_mem BIGINT NOT NULL,          -- kB
  "timestamp" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS host_usage (
  "timestamp" TIMESTAMP NOT NULL,
  host_id INT NOT NULL,
  memory_free INT NOT NULL,           -- MB
  cpu_idle SMALLINT NOT NULL,         -- %
  cpu_kernel SMALLINT NOT NULL,       -- %
  disk_io INT NOT NULL,               -- current IO in progress
  disk_available INT NOT NULL,        -- MB
  CONSTRAINT host_usage_host_info_fk FOREIGN KEY (host_id) REFERENCES host_info(id)
);

