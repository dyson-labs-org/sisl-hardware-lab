# START_HERE

## Immediate goal

Prove Phase 1 of the SISL hackathon demo:

1. A spread signal can be transmitted across bandwidth
2. The passive observer does not see an obvious new signal
3. The intended receiver can recover the payload with the correct spreading code
4. The wrong code fails to recover the payload

Do not start with crypto. Do not start with SCRAP. Do not start with end-to-end protocol work.

The first milestone is purely RF + DSSS.

## Working order

### Step 1: Keep the Python repo healthy
Before major changes:

```powershell
ruff check src tests
pytest
python examples/quickstart.py