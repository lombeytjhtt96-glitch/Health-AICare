#!/bin/bash
echo "Gatauaku" | sudo -S -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
echo "Gatauaku" | sudo -S -u postgres createdb aicare_db 2>/dev/null || echo "DB already exists"

# Update pg_hba.conf to allow md5 from 127.0.0.1
HBA="/etc/postgresql/18/main/pg_hba.conf"
if ! grep -q "127.0.0.1/32.*md5" "$HBA" 2>/dev/null; then
    echo "Gatauaku" | sudo -S bash -c "echo 'host all all 127.0.0.1/32 md5' >> $HBA"
    echo "Gatauaku" | sudo -S bash -c "echo 'host all all ::1/128 md5' >> $HBA"
fi

# Reload PostgreSQL
echo "Gatauaku" | sudo -S pg_ctlcluster 18 main reload

echo "Testing..."
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d aicare_db -c "SELECT 'OK' as status;"
echo "DONE"
