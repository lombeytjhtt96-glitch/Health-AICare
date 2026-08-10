import psycopg

# Test 1: localhost
try:
    conn = psycopg.connect('postgresql://postgres:postgres@127.0.0.1:5432/health_aicare_db?sslmode=disable')
    conn.close()
    print('127.0.0.1 OK')
except Exception as e:
    print(f'127.0.0.1 FAIL: {e}')

# Test 2: WSL IP
try:
    conn = psycopg.connect('postgresql://postgres:postgres@172.24.24.60:5432/health_aicare_db?sslmode=disable')
    conn.close()
    print('WSL IP OK')
except Exception as e:
    print(f'WSL IP FAIL: {e}')
