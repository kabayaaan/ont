from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from librouteros import connect
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atur sesuai kebutuhan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_mikrotik():
    return connect(
        username=os.getenv("MT_USER"),
        password=os.getenv("MT_PASS"),
        host=os.getenv("MT_HOST"),
        port=int(os.getenv("MT_PORT", 8728))
    )

@app.post("/inject-nat")
def inject_nat(username: str = Form(...)):
    api = connect_mikrotik()
    active_ppp = api.path("ppp", "active")

    ip_address = None
    for user in active_ppp:
        if user.get("name") == username:
            ip_address = user.get("address")
            break

    if not ip_address:
        return {"status": "error", "message": f"User '{username}' tidak ditemukan atau belum aktif."}

    nat = api.path("ip", "firewall", "nat")
    target_rule = None
    for rule in nat:
        if rule.get("comment") == "bravo1rmtont":
            target_rule = rule
            break

    if not target_rule:
        return {"status": "error", "message": "Rule NAT dengan comment 'bravo1rmtont' tidak ditemukan."}

    nat.update(
        id=target_rule[".id"],
        to_addresses=ip_address,
        to_ports="80"
    )

    return {
        "status": "success",
        "message": f"Rule NAT berhasil di-update untuk IP {ip_address}"
    }
