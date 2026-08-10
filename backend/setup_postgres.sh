#!/bin/bash
set -e

echo "=== Setting up PostgreSQL ==="

# Set postgres password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

# Create database
sudo -u postgres createdb aicare_db 2>/dev/null || echo "Database aicare_db already exists"

# Find and update pg_hba.conf to allow md5 auth from 127.0.0.1
PG_VERSION=$(pg_lsclusters -h | awk '{print $1}' | head -1)
PG_CLUSTER=$(pg_lsclusters -h | awk '{print $2}' | head -1)
HBA_FILE="/etc/postgresql/${PG_VERSION}/${PG_CLUSTER}/pg_hba.conf"

echo "HBA file: $HBA_FILE"

# Check if md5 rule already exists
if sudo grep -q "127.0.0.1/32.*md5" "$HBA_FILE"; then
    echo "md5 auth already configured"
else
    echo "Adding md5 auth rules..."
    echo "host    all             all             127.0.0.1/32            md5" | sudo tee -a "$HBA_FILE"
    echo "host    all             all             ::1/128                 md5" | sudo tee -a "$HBA_FILE"
fi

# Reload PostgreSQL
sudo -u postgres pg_ctlcluster ${PG_VERSION} ${PG_CLUSTER} reload

echo "=== Testing connection ==="
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d aicare_db -c "SELECT 'Connection OK' as status;"

echo "=== PostgreSQL setup complete ==="
