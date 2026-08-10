"""
Script untuk update URL Railway di Vercel env vars setelah Railway deploy selesai.
Jalankan: C:\Python314\python.exe update_railway_url.py <RAILWAY_URL>

Contoh: C:\Python314\python.exe update_railway_url.py https://health-aicare.up.railway.app
"""
import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python update_railway_url.py <RAILWAY_BACKEND_URL>")
    print("Example: python update_railway_url.py https://health-aicare.up.railway.app")
    sys.exit(1)

railway_url = sys.argv[1].rstrip("/")
ws_url = railway_url.replace("https://", "wss://").replace("http://", "ws://")

print(f"\n🚀 Updating Vercel env vars with Railway URL: {railway_url}\n")

frontend_dir = r"c:\Users\Asus\Downloads\Health-AICare\frontend"

updates = [
    ("NEXT_PUBLIC_API_URL", railway_url),
    ("NEXT_PUBLIC_BACKEND_BASE", railway_url),
    ("NEXT_PUBLIC_BACKEND_WS_BASE", ws_url),
]

for key, value in updates:
    print(f"  Setting {key} = {value}")
    result = subprocess.run(
        ["npx", "vercel", "env", "add", key, "production", "--force"],
        input=value,
        capture_output=True,
        text=True,
        cwd=frontend_dir,
        shell=True
    )
    if "✓" in result.stdout or "Overrode" in result.stdout:
        print(f"  ✅ {key} updated!")
    else:
        print(f"  ⚠️ {result.stdout} {result.stderr}")

print("\n✅ All done! Triggering Vercel redeploy...")

# Trigger redeploy via git
import os
os.system('cd "c:\\Users\\Asus\\Downloads\\Health-AICare" && git commit --allow-empty -m "chore: update Railway backend URL in Vercel" && git push origin main')

print("\n🎉 Vercel will rebuild in 1-2 minutes.")
print(f"   Frontend: https://health-aicare.vercel.app")
print(f"   Backend:  {railway_url}")
print(f"\nTest login: https://health-aicare.vercel.app/signin")
