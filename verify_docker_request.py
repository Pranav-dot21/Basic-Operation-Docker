import json
import subprocess
import time
import urllib.request

container_name = "backend_test"

subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run = subprocess.run(
    ["docker", "run", "-d", "--name", container_name, "-p", "5000:5000", "backend"],
    capture_output=True,
    text=True,
)
if run.returncode != 0:
    raise SystemExit(f"Docker run failed: {run.stderr.strip()}")

try:
    time.sleep(3)
    with urllib.request.urlopen("http://127.0.0.1:5000/") as resp:
        print("ROOT status", resp.status)
        print("ROOT body", resp.read().decode())

    data = json.dumps({"input1": 3, "input2": 4, "operator": "+"}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:5000/calculate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        print("CALC status", resp.status)
        print("CALC body", resp.read().decode())
except urllib.error.HTTPError as err:
    print("CALC status", err.code)
    print("CALC body", err.read().decode())
finally:
    subprocess.run(["docker", "stop", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
