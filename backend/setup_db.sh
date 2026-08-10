#!/bin/bash
# Run as postgres unix user to set up the database
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE aicare_db;" 2>/dev/null || echo "DB already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aicare_db TO postgres;"
# Allow password auth from localhost - update pg_hba.conf
PG_HBA=$(sudo -u postgres psql -t -c "SHOW hba_file;" | xargs)
echo "pg_hba.conf: $PG_HBA"
# Add md5 auth for host connections if not already there
if ! sudo grep -q "host.*all.*postgres.*127.0.0.1" "$PG_HBA" 2>/dev/null; then
    echo "host    all             postgres        127.0.0.1/32            md5" | sudo tee -a "$PG_HBA"
    echo "host    all             all             127.0.0.1/32            md5" | sudo tee -a "$PG_HBA"
fi
sudo -u postgres pg_ctlcluster $(pg_lsclusters -h | awk '{print $1}') $(pg_lsclusters -h | awk '{print $2}') reload 2>/dev/null || true
echo "DONE"
