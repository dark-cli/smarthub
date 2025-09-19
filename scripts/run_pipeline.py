#!/usr/bin/env python3
import asyncio, time, json
import pandas as pd
from core.interface import Interface

CASES = [
    {"msg":"turn on the light","ctx":{"room":"kitchen"}},
    {"msg":"it's too bright here","ctx":{"room":"office"}},
    {"msg":"I'm cold","ctx":{"room":"bedroom"}},
    {"msg":"dim the living room lights","ctx":{"room":"kitchen"}},
    {"msg":"turn on the kitchen light","ctx":{"room":"bedroom"}},
    {"msg":"turn on the fan","ctx":{"room":"living_room"}},
    {"msg":"set the fan speed to 50% ","ctx":{"room":"hallway"}},
    # Direct, obvious
    {"msg": "turn on the kitchen light", "ctx": {"room": "kitchen"}},
    # Direct, context-driven (don’t mention room)
    {"msg": "switch off the lamp", "ctx": {"room": "bedroom"}},
    # Indirect, requires mapping “desk” to actual device
    {"msg": "can you light up my desk?", "ctx": {"room": "office"}},
    # Clever, uses “mirror” as a reference
    {"msg": "make the mirror bright", "ctx": {"room": "bathroom"}},
    # Context-driven, ambiguous but should infer location
    {"msg": "it’s too dark here", "ctx": {"room": "living_room"}},
    # Indirect, context & device mapping (“balcony”)
    {"msg": "I want to see outside", "ctx": {"room": "balcony"}},
    # Indirect, fan control (not just “on/off”)
    {"msg": "get some air moving", "ctx": {"room": "living_room"}},
    # Requires mapping “strip” to kitchen light, indirect
    {"msg": "illuminate the strip", "ctx": {"room": "kitchen"}},
    # Direct device command, not in same room, needs override
    {"msg": "turn off the garden light", "ctx": {"room": "living_room"}},
    # Indirect temp control, context only
    {"msg": "it's freezing", "ctx": {"room": "bedroom"}},
    # Clever, referencing “movie” scene as an action
    {"msg": "movie mode on", "ctx": {"room": "living_room"}},
    # Indirect, “nightlight” = Kids Room Nightlight
    {"msg": "turn on the nightlight", "ctx": {"room": "kids_room"}},
    # Indirect, AC temp by feeling
    {"msg": "make it cooler in here", "ctx": {"room": "bedroom"}},
    # Action by function, not device
    {"msg": "cycle the sprinklers", "ctx": {"room": "garden"}},
    # Super indirect, “the lamp’s too bright”, should dim
    {"msg": "the lamp's too bright", "ctx": {"room": "living_room"}},
]


async def main():
    iface = Interface(top_k=6)
    rows = []
    for c in CASES:
        t0 = time.perf_counter()
        res = await iface.handle_message(c["msg"], c["ctx"])
        dt = (time.perf_counter() - t0)
        rows.append({
            "message": res["message"],
            "context": json.dumps(res["context"], ensure_ascii=False),
            # "keywords": (res["keywords"] or ""),
            "devices": len(res["devices"]),
            "actions": len(res["actions"]),
            "decision": res["decision"],
            "time_ms": round(dt, 1),
        })
    df = pd.DataFrame(rows, columns=["message","context","devices","actions","decision","time_ms"])
    with pd.option_context("display.max_colwidth", 140):
        print(df.to_string(index=False))

if __name__ == "__main__":
    asyncio.run(main())
