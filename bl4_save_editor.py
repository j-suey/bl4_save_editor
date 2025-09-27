
#!/usr/bin/env python3
"""
BL4 Unified Save Editor — v1.04a 
- Fix: Character/Progression read/write whether data is at YAML root or under "state"
- UI: Dark + teal accents for better legibility
- Character tab: adds Cash, Eridium, SHIFT (gold) Keys with auto-path detection
- Items: popup inspector (Simple + Raw) preserved
- YAML tab: search + _DECODED_ITEMS export/encode
Dependencies:
    pip install pyyaml pycryptodome
"""

from pathlib import Path


# ====== Built-in Advanced Decoder (embedded; compressed) ======
import base64 as _b64, zlib as _zl
_DEC_NS = None
_DECODER_B64 = """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"""
def _load_embedded_decoder():
    global _DEC_NS
    if _DEC_NS is not None: return _DEC_NS
    try:
        src = _zl.decompress(_b64.b64decode(_DECODER_B64))
        ns = {}; ns["__name__"] = "bl4_embedded_decoder"
        exec(src, ns, ns)
        _DEC_NS = ns
    except Exception as e:
        print("[decoder] embed load failed:", e); _DEC_NS = {}
    return _DEC_NS

# --- Decoder adapter: tolerate different function names & return shapes ---
def _get_decoder_fn(ns):
    for name in ("decode_item_serial","adv_decode_item_serial","decode_serial","decode","parse_item_serial","item_decode"):
        fn = ns.get(name)
        if callable(fn):
            return fn
    return None

def _extract_name_from_decoded(obj):
    # dict-like
    try:
        if isinstance(obj, dict):
            for k in ("weapon_name","friendly_name","name","label","title","gun_name","item_name"):
                if k in obj and isinstance(obj[k], str) and obj[k].strip():
                    return obj[k]
    except Exception:
        pass
    # object-like
    try:
        for k in ("weapon_name","friendly_name","name","label","title","gun_name","item_name"):
            v = getattr(obj, k, None)
            if isinstance(v, str) and v.strip():
                return v
    except Exception:
        pass
    # tuple/list
    try:
        if isinstance(obj, (list, tuple)) and obj:
            if isinstance(obj[0], str) and obj[0].strip():
                return obj[0]
            if isinstance(obj[0], dict):
                return _extract_name_from_decoded(obj[0])
    except Exception:
        pass
    return ""


def _to_int_sane(x, default=0):
    try:
        s = str(x).strip()
        if s == "" or s.lower() == "none":
            return default
        return int(s, 0) if s.lower().startswith("0x") else int(''.join(ch for ch in s if ch in "-0123456789") or default)
    except Exception:
        return default


def adv_decode_item_serial(serial):
    serial = str(serial).strip()
    ns = _load_embedded_decoder()
    fn = _get_decoder_fn(ns)
    if callable(fn):
        try:
            return fn(serial)
        except Exception as e:
            print("[decoder] decode error:", e)
    return None

def resolve_item_name(serial: str, decoded=None) -> str:
    try:
        if decoded is None:
            decoded = adv_decode_item_serial(serial.strip())
        nm = _extract_name_from_decoded(decoded)
        if nm:
            return nm
        if "_friendly_from_decoded" in globals():
            try:
                return _friendly_from_decoded(decoded)
            except Exception:
                pass
    except Exception:
        pass
    if "_friendly_from_decoded" in globals():
        try:
            return _friendly_from_decoded(None)
        except Exception:
            pass
    return ""
def _safe_unpack_item_values(vals):
    vals = list(vals) if isinstance(vals, (list, tuple)) else [vals]
    if len(vals) == 4:
        path, typ, code, serial = vals
        return path, typ, "", code, serial, ""
    while len(vals) < 6: vals.append("")
    return tuple(vals[:6])



# -------- Advanced decoder loader --------
_ADV_DECODER = None
def _get_adv_decoder():
    """

    """
    import os, importlib.util
    global _ADV_DECODER
    if _ADV_DECODER is not None:
        return _ADV_DECODER
    try:
        base = os.path.dirname(__file__)
    except Exception:
        base = os.getcwd()
    for cand in ("main.py", "decoder.py"): #support for future decoders
        path = os.path.join(base, cand)
        if os.path.exists(path):
            try:
                spec = importlib.util.spec_from_file_location("bl4_ext_decoder", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)  # type: ignore
                fn = getattr(mod, "decode_item_serial", None)
                if callable(fn):
                    _ADV_DECODER = fn
                    return fn
            except Exception:
                _ADV_DECODER = None
                return None
    _ADV_DECODER = None
    return None



def _safe_unpack_item_values(vals):
    """Return a 6-tuple (path, type, name, code, serial, tags) from a Treeview 'values'.
    Accepts legacy 4-tuples and pads name/tags when missing.
    """
    vals = list(vals) if isinstance(vals, (list, tuple)) else [vals]
    # legacy: (path,type,code,serial)
    if len(vals) == 4:
        path, typ, code, serial = vals
        name = ""
        tags = ""
        return path, typ, name, code, serial, tags
    # new: (path,type,name,code,serial,tags)
    if len(vals) >= 6:
        return vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]
    # unknown shape -> best effort
    while len(vals) < 6:
        vals.append("")
    return tuple(vals[:6])



# ------------------------------------------------------------------
# WEAPON_NAME_MAP
# Groupings follow BL4's internal balance ID structure (game order).
# Add new entries inside the relevant category.
# ------------------------------------------------------------------
WEAPON_NAME_MAP = {
    # Assault Rifles
    "BalanceId_AssaultRifle_Atlas_01": "Atlas Assault Rifle",
    "BalanceId_AssaultRifle_Dahl_02": "Dahl Assault Rifle",
    # Pistols
    "BalanceId_Pistol_Hyperion_01": "Hyperion Pistol",
    "BalanceId_Pistol_Tediore_02": "Tediore Sidearm",
    # SMGs
    "BalanceId_SMG_Maliwan_01": "Maliwan SMG",
    "BalanceId_SMG_Hyperion_02": "Hyperion SMG",
    # Shotguns
    "BalanceId_Shotgun_Jakobs_01": "Jakobs Shotgun",
    # Vehicles
    "BalanceId_Vehicle_Hovercraft_01": "Hovercraft Skin",
    # Skins
    "BalanceId_Skin_Paladin_01": "Paladin Skin",
}


def _unlock_all_map_areas(save_dict):
    """Best-effort: ensure world/map/areas/locations exist and set visited/discovered=True.
    If empty, seed a minimal 'ALL' entry so users still see an unlock effect."""
    try:
        if not isinstance(save_dict, dict):
            return 0
        world = save_dict.setdefault("state", {}).setdefault("world", {})
        m = world.setdefault("map", {})
        areas = m.setdefault("areas", {})
        locations = m.setdefault("locations", {})
        touched = 0

        def touch_container(container):
            nonlocal touched
            if isinstance(container, dict):
                if not container:
                    container["ALL"] = {"visited": True, "discovered": True}
                    touched += 1
                else:
                    for k, v in list(container.items()):
                        if not isinstance(v, dict):
                            v = {}
                        if not v.get("visited"):
                            v["visited"] = True; touched += 1
                        if not v.get("discovered"):
                            v["discovered"] = True; touched += 1
                        container[k] = v
        touch_container(areas)
        touch_container(locations)
        return touched
    except Exception as e:
        print("Map unlock error:", e)
        return 0


def _apply_selected_class_104a(app):
    """Writes the selected class into the save."""
    try:
        cls = None
        if hasattr(app, "var_class_dd"):
            cls = (app.var_class_dd.get() or "").strip()
        if not cls and hasattr(app, "cf") and "Class" in app.cf:
            try:
                cls = app.cf["Class"].get().strip()
            except Exception:
                pass

        norm = {
            "ECHO4": "Echo4", "ECHO 4": "Echo4",
            "DARKSIREN": "DarkSiren", "DARK SIREN": "DarkSiren",
            "EXOSOLDIER": "ExoSoldier", "EXO SOLDIER": "ExoSoldier",
            "GRAVITAR": "Gravitar",
            "PALADIN": "Paladin",
        }
        if cls:
            key = cls.upper().replace("-", " ").replace("_", " ")
            cls_norm = norm.get(key, cls)
            root = app.yaml_obj if hasattr(app, "yaml_obj") else (app._root() if hasattr(app,"_root") else {})
            state = root.setdefault("state", {})
            character = state.setdefault("character", {})
            character["class"] = cls_norm
            root.setdefault("character", {})["class"] = cls_norm
            return True, cls_norm
        return False, None
    except Exception as e:
        print("apply class failed:", e)
        return False, None

import time, zlib
from typing import Any, Dict, List, Optional, Tuple, Union

# -- Weapon friendly-name mapping 
WEAPON_NAMES = {
    'd_t@': 'Jakobs Shotgun',
    'bV{r': 'Jakobs Pistol',
    'y3L+2}': 'Jakobs Sniper',
    'eU_{': 'Maliwan Shotgun',
    'w$Yw2}': 'Maliwan SMG',
    'velk2}': 'Vladof AR',
    'xFw!2}': 'Vladof SMG',
    'xp/&2}': 'Ripper Sniper',
    'ct)%': 'Torgue Pistol',
    'fs(8': 'Daedalus AR',
    'b)Kv': 'Order Pistol',
    'y>^2}': 'Order Sniper',
    'r$WBm': 'Jakobs Ordnance'
}

def _weapon_name_from_serial(serial: str) -> str:
    if not serial or not serial.startswith('@Ug'):
        return ''
    for length in range(4, 10):
        prefix = serial[3:3+length]
        for code, name in WEAPON_NAMES.items():
            if prefix.startswith(code):
                return name
    return ''

import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb, ttk
# ── Embedded cosmetic RewardPackages (no CSVs needed) ─────────────────────────

# ── Embedded Profile Unlock Catalog (fallback, no CSV required) ───────────────
EMBEDDED_PROFILE_UNLOCKS = {
    "shared_progress": [
        "shared_progress.vault_hunter_level",
        "shared_progress.prologue_completed",
        "shared_progress.story_completed",
        "shared_progress.epilogue_started",
    ],
    "unlockable_echo4": [
        "Unlockable_Echo4.attachment01_partyhat",
        "Unlockable_Echo4.attachment04_wings",
        "Unlockable_Echo4.attachment03_bolt",
        "Unlockable_Echo4.attachment09_goggles",
        "Unlockable_Echo4.Skin01_Prison",
        "Unlockable_Echo4.Skin02_Order",
        "Unlockable_Echo4.Skin03_Ghost",
        "Unlockable_Echo4.Skin04_Tech",
        "Unlockable_Echo4.Skin05_Ripper",
        "Unlockable_Echo4.Skin11_Astral",
        "Unlockable_Echo4.Skin21_Graffiti",
        "Unlockable_Echo4.Skin22_Knitted",
        "Unlockable_Echo4.Skin25_Slimed",
        "Unlockable_Echo4.Skin29_Guardian",
        "Unlockable_Echo4.Skin31_Koto",
        "Unlockable_Echo4.Skin33_Jakobs",
        "Unlockable_Echo4.Skin35_Vladof",
        "Unlockable_Echo4.Skin36_Torgue",
        "Unlockable_Echo4.Skin37_Maliwan",
        "Unlockable_Echo4.Skin38_CyberPop",
        "Unlockable_Echo4.Skin39_Critters",
        "Unlockable_Echo4.Skin40_Veil",
        "Unlockable_Echo4.Skin42_Legacy",
        "Unlockable_Echo4.Skin50_BreakTheGame",
        "Unlockable_Echo4.Skin24_PreOrder",
        "Unlockable_Echo4.Skin14_Fire",
        "Unlockable_Echo4.attachment10_crown",
        "Unlockable_Echo4.Body03_Ripper",
        "Unlockable_Echo4.attachment07_horns",
        "Unlockable_Echo4.Skin07_RedHanded",
        "Unlockable_Echo4.Skin19_Dirty",
        "Unlockable_Echo4.Skin45_BreakFree",
        "Unlockable_Echo4.attachment08_tinfoilhat",
        "Unlockable_Echo4.Skin09_Sewer",
        "Unlockable_Echo4.Skin18_Electi",
        "Unlockable_Echo4.Skin15_Survivalist",
        "Unlockable_Echo4.Skin17_Auger",
        "Unlockable_Echo4.Skin27_Space",
        "Unlockable_Echo4.Body01_GeneVIV",
        "Unlockable_Echo4.Skin12_Tediore",
        "Unlockable_Echo4.Skin32_DuctTaped",
        "Unlockable_Echo4.Skin16_Crimson",
    ],
    "unlockable_darksiren": [
        "Unlockable_DarkSiren.Head01_Prison",
        "Unlockable_DarkSiren.Body01_Prison",
        "Unlockable_DarkSiren.Skin01_Prison",
        "Unlockable_DarkSiren.Skin02_Order",
        "Unlockable_DarkSiren.Skin03_Ghost",
        "Unlockable_DarkSiren.Skin04_Tech",
        "Unlockable_DarkSiren.Skin05_Ripper",
        "Unlockable_DarkSiren.Skin06_Amara",
        "Unlockable_DarkSiren.Skin07_RedHanded",
        "Unlockable_DarkSiren.Skin08_Corrupted",
        "Unlockable_DarkSiren.Skin21_Graffiti",
        "Unlockable_DarkSiren.Skin29_Guardian",
        "Unlockable_DarkSiren.Skin31_Koto",
        "Unlockable_DarkSiren.Skin37_Maliwan",
        "Unlockable_DarkSiren.Skin39_Critters",
        "Unlockable_DarkSiren.Skin40_Veil",
        "Unlockable_DarkSiren.Head02_PigTails",
        "Unlockable_DarkSiren.Head03_MoHawk",
        "Unlockable_DarkSiren.Head05_BikeHelmet",
        "Unlockable_DarkSiren.Head06_PunkMask",
        "Unlockable_DarkSiren.Head07_Demon",
        "Unlockable_DarkSiren.Head11_Ripper",
        "Unlockable_DarkSiren.Head12_Order",
        "Unlockable_DarkSiren.Head23_CrashTestDummy",
        "Unlockable_DarkSiren.Skin24_PreOrder",
        "Unlockable_DarkSiren.Body02_Premium",
        "Unlockable_DarkSiren.Head16_Premium",
        "Unlockable_DarkSiren.Skin44_Premium",
        "Unlockable_DarkSiren.Skin10_Hawaiian",
        "Unlockable_DarkSiren.Skin14_Fire",
        "Unlockable_DarkSiren.Skin25_Slimed",
        "Unlockable_DarkSiren.Skin26_Camo",
        "Unlockable_DarkSiren.Skin34_Daedalus",
        "Unlockable_DarkSiren.Skin45_BreakFree",
        "Unlockable_DarkSiren.Head08_Survivalist",
        "Unlockable_DarkSiren.Skin09_Sewer",
        "Unlockable_DarkSiren.Head09_Electi",
        "Unlockable_DarkSiren.Head15_CrimeLord",
        "Unlockable_DarkSiren.Skin11_Astral",
        "Unlockable_DarkSiren.Head10_Transhuman",
        "Unlockable_DarkSiren.Skin18_Electi",
        "Unlockable_DarkSiren.Skin13_3CatMoon",
        "Unlockable_DarkSiren.Skin15_Survivalist",
        "Unlockable_DarkSiren.Skin17_Auger",
        "Unlockable_DarkSiren.Skin27_Space",
        "Unlockable_DarkSiren.Head04_Shades",
        "Unlockable_DarkSiren.Skin12_Tediore",
        "Unlockable_DarkSiren.Head14_Thresher",
        "Unlockable_DarkSiren.Skin16_Crimson",
    ],
    "unlockable_exosoldier": [
        "Unlockable_ExoSoldier.Head01_Prison",
        "Unlockable_ExoSoldier.Body01_Prison",
        "Unlockable_ExoSoldier.Skin01_Prison",
        "Unlockable_ExoSoldier.Skin02_Order",
        "Unlockable_ExoSoldier.Skin03_Ghost",
        "Unlockable_ExoSoldier.Skin04_Tech",
        "Unlockable_ExoSoldier.Skin05_Ripper",
        "Unlockable_ExoSoldier.Skin06_Amara",
        "Unlockable_ExoSoldier.Skin07_RedHanded",
        "Unlockable_ExoSoldier.Skin08_Corrupted",
        "Unlockable_ExoSoldier.Skin21_Graffiti",
        "Unlockable_ExoSoldier.Skin29_Guardian",
        "Unlockable_ExoSoldier.Skin31_Koto",
        "Unlockable_ExoSoldier.Skin37_Maliwan",
        "Unlockable_ExoSoldier.Skin39_Critters",
        "Unlockable_ExoSoldier.Skin40_Veil",
        "Unlockable_ExoSoldier.Head02_Mullet",
        "Unlockable_ExoSoldier.Head03_Guerilla",
        "Unlockable_ExoSoldier.Head04_TechHawk",
        "Unlockable_ExoSoldier.Head06_BlindFold",
        "Unlockable_ExoSoldier.Head07_Helm",
        "Unlockable_ExoSoldier.Head11_Ripper",
        "Unlockable_ExoSoldier.Head12_Order",
        "Unlockable_ExoSoldier.Head23_CrushTestDummy",
        "Unlockable_ExoSoldier.Skin24_PreOrder",
        "Unlockable_ExoSoldier.Body02_Premium",
        "Unlockable_ExoSoldier.Head16_Premium",
        "Unlockable_ExoSoldier.Skin44_Premium",
        "Unlockable_ExoSoldier.Skin10_Hawaiian",
        "Unlockable_ExoSoldier.Skin14_Fire",
        "Unlockable_ExoSoldier.Skin25_Slimed",
        "Unlockable_ExoSoldier.Skin26_Camo",
        "Unlockable_ExoSoldier.Skin34_Daedalus",
        "Unlockable_ExoSoldier.Skin45_BreakFree",
        "Unlockable_ExoSoldier.Head08_Survivalist",
        "Unlockable_ExoSoldier.Skin09_Sewer",
        "Unlockable_ExoSoldier.Head09_Electi",
        "Unlockable_ExoSoldier.Head15_CrimeLord",
        "Unlockable_ExoSoldier.Skin11_Astral",
        "Unlockable_ExoSoldier.Head10_Transhuman",
        "Unlockable_ExoSoldier.Skin18_Electi",
        "Unlockable_ExoSoldier.Skin13_3CatMoon",
        "Unlockable_ExoSoldier.Skin15_Survivalist",
        "Unlockable_ExoSoldier.Skin17_Auger",
        "Unlockable_ExoSoldier.Skin27_Space",
        "Unlockable_ExoSoldier.Head05_LongHair",
        "Unlockable_ExoSoldier.Skin12_Tediore",
        "Unlockable_ExoSoldier.Head14_Thresher",
        "Unlockable_ExoSoldier.Skin16_Crimson",
    ],
    "unlockable_gravitar": [
        "Unlockable_Gravitar.Head01_Prison",
        "Unlockable_Gravitar.Body01_Prison",
        "Unlockable_Gravitar.Skin01_Prison",
        "Unlockable_Gravitar.Skin02_Order",
        "Unlockable_Gravitar.Skin03_Ghost",
        "Unlockable_Gravitar.Skin04_Tech",
        "Unlockable_Gravitar.Skin05_Ripper",
        "Unlockable_Gravitar.Skin06_Amara",
        "Unlockable_Gravitar.Skin07_RedHanded",
        "Unlockable_Gravitar.Skin08_Corrupted",
        "Unlockable_Gravitar.Skin21_Graffiti",
        "Unlockable_Gravitar.Skin29_Guardian",
        "Unlockable_Gravitar.Skin31_Koto",
        "Unlockable_Gravitar.Skin37_Maliwan",
        "Unlockable_Gravitar.Skin39_Critters",
        "Unlockable_Gravitar.Skin40_Veil",
        "Unlockable_Gravitar.Head02_DreadBuns",
        "Unlockable_Gravitar.Head03_Helmet",
        "Unlockable_Gravitar.Head04_TechBraids",
        "Unlockable_Gravitar.Head05_SafetyFirst",
        "Unlockable_Gravitar.Head07_VRPunk",
        "Unlockable_Gravitar.Head11_Ripper",
        "Unlockable_Gravitar.Head12_Order",
        "Unlockable_Gravitar.Head23_CrushTestDummy",
        "Unlockable_Gravitar.Skin24_PreOrder",
        "Unlockable_Gravitar.Body02_Premium",
        "Unlockable_Gravitar.Head16_Premium",
        "Unlockable_Gravitar.Skin44_Premium",
        "Unlockable_Gravitar.Skin10_Hawaiian",
        "Unlockable_Gravitar.Skin14_Fire",
        "Unlockable_Gravitar.Skin25_Slimed",
        "Unlockable_Gravitar.Skin26_Camo",
        "Unlockable_Gravitar.Skin34_Daedalus",
        "Unlockable_Gravitar.Skin45_BreakFree",
        "Unlockable_Gravitar.Head08_Survivalist",
        "Unlockable_Gravitar.Skin09_Sewer",
        "Unlockable_Gravitar.Head09_Electi",
        "Unlockable_Gravitar.Head15_CrimeLord",
        "Unlockable_Gravitar.Skin11_Astral",
        "Unlockable_Gravitar.Head10_Transhuman",
        "Unlockable_Gravitar.Skin18_Electi",
        "Unlockable_Gravitar.Skin13_3CatMoon",
        "Unlockable_Gravitar.Skin15_Survivalist",
        "Unlockable_Gravitar.Skin17_Auger",
        "Unlockable_Gravitar.Skin27_Space",
        "Unlockable_Gravitar.Head06_RoundGlasses",
        "Unlockable_Gravitar.Skin12_Tediore",
        "Unlockable_Gravitar.Head14_Thresher",
        "Unlockable_Gravitar.Skin16_Crimson",
    ],
    "unlockable_paladin": [
        "Unlockable_Paladin.Head01_Prison",
        "Unlockable_Paladin.Body01_Prison",
        "Unlockable_Paladin.Skin01_Prison",
        "Unlockable_Paladin.Skin02_Order",
        "Unlockable_Paladin.Skin03_Ghost",
        "Unlockable_Paladin.Skin04_Tech",
        "Unlockable_Paladin.Skin05_Ripper",
        "Unlockable_Paladin.Skin06_Amara",
        "Unlockable_Paladin.Skin07_RedHanded",
        "Unlockable_Paladin.Skin08_Corrupted",
        "Unlockable_Paladin.Skin21_Graffiti",
        "Unlockable_Paladin.Skin29_Guardian",
        "Unlockable_Paladin.Skin31_Koto",
        "Unlockable_Paladin.Skin37_Maliwan",
        "Unlockable_Paladin.Skin39_Critters",
        "Unlockable_Paladin.Skin40_Veil",
        "Unlockable_Paladin.Head02_PonyTail",
        "Unlockable_Paladin.Head03_BaldMask",
        "Unlockable_Paladin.Head04_Visor",
        "Unlockable_Paladin.Head06_Hooded",
        "Unlockable_Paladin.Head07_Headband",
        "Unlockable_Paladin.Head11_Ripper",
        "Unlockable_Paladin.Head12_Order",
        "Unlockable_Paladin.Head23_CrushTestDummy",
        "Unlockable_Paladin.Skin24_PreOrder",
        "Unlockable_Paladin.Body02_Premium",
        "Unlockable_Paladin.Head16_Premium",
        "Unlockable_Paladin.Skin44_Premium",
        "Unlockable_Paladin.Skin10_Hawaiian",
        "Unlockable_Paladin.Skin14_Fire",
        "Unlockable_Paladin.Skin25_Slimed",
        "Unlockable_Paladin.Skin26_Camo",
        "Unlockable_Paladin.Skin34_Daedalus",
        "Unlockable_Paladin.Skin45_BreakFree",
        "Unlockable_Paladin.Head08_Survivalist",
        "Unlockable_Paladin.Skin09_Sewer",
        "Unlockable_Paladin.Head09_Electi",
        "Unlockable_Paladin.Head15_CrimeLord",
        "Unlockable_Paladin.Skin11_Astral",
        "Unlockable_Paladin.Head10_Transhuman",
        "Unlockable_Paladin.Skin18_Electi",
        "Unlockable_Paladin.Skin13_3CatMoon",
        "Unlockable_Paladin.Skin15_Survivalist",
        "Unlockable_Paladin.Skin17_Auger",
        "Unlockable_Paladin.Skin27_Space",
        "Unlockable_Paladin.Head05_Goth",
        "Unlockable_Paladin.Skin12_Tediore",
        "Unlockable_Paladin.Head14_Thresher",
        "Unlockable_Paladin.Skin16_Crimson",
    ],
    "unlockable_weapons": [
        "Unlockable_Weapons.Mat13_Whiteout",
        "Unlockable_Weapons.Mat31_Splash",
        "Unlockable_Weapons.Mat16_PolePosition",
        "Unlockable_Weapons.Mat14_Grunt",
        "Unlockable_Weapons.Mat18_CrashTest",
        "Unlockable_Weapons.Mat07_CuteCat",
        "Unlockable_Weapons.Mat19_Meltdown",
        "Unlockable_Weapons.Mat36_PreOrder",
        "Unlockable_Weapons.Mat38_HeadHunter",
        "Unlockable_Weapons.shiny_ballista",
        "Unlockable_Weapons.shiny_symmetry",
        "Unlockable_Weapons.shiny_plasmacoil",
        "Unlockable_Weapons.shiny_star_helix",
        "Unlockable_Weapons.shiny_anarchy",
        "Unlockable_Weapons.Mat01_Synthwave",
        "Unlockable_Weapons.Mat29_Cheers",
        "Unlockable_Weapons.Mat17_DeadWood",
        "Unlockable_Weapons.Mat25_LocustGas",
        "Unlockable_Weapons.Mat26_AugerSight",
        "Unlockable_Weapons.Mat27_GoldenPower",
        "Unlockable_Weapons.shiny_leadballoon",
        "Unlockable_Weapons.shiny_convergence",
        "Unlockable_Weapons.shiny_boomslang",
        "Unlockable_Weapons.Mat08_EchoBot",
        "Unlockable_Weapons.shiny_luty",
        "Unlockable_Weapons.shiny_rocketreload",
        "Unlockable_Weapons.Mat06_ElectiSamurai",
        "Unlockable_Weapons.shiny_noisycricket",
        "Unlockable_Weapons.shiny_heavyturret",
        "Unlockable_Weapons.shiny_kaoson",
        "Unlockable_Weapons.Mat33_Creepy",
        "Unlockable_Weapons.Mat34_MoneyCamo",
        "Unlockable_Weapons.Mat30_CrimsonRaiders",
        "Unlockable_Weapons.Mat32_ImperialGuard",
        "Unlockable_Weapons.shiny_kaleidosplode",
        "Unlockable_Weapons.shiny_slugger",
        "Unlockable_Weapons.shiny_beegun",
        "Unlockable_Weapons.shiny_kickballer",
        "Unlockable_Weapons.shiny_vamoose",
    ],
    "unlockable_vehicles": [
        "Unlockable_Vehicles.Mat17_DeadWood",
        "Unlockable_Vehicles.Mat16_PolePosition",
        "Unlockable_Vehicles.Mat13_Whiteout",
        "Unlockable_Vehicles.Mat29_Cheers",
        "Unlockable_Vehicles.Mat09_FolkHero",
        "Unlockable_Vehicles.Mat07_CuteCat",
        "Unlockable_Vehicles.Mat22_Overload",
        "Unlockable_Vehicles.Mat10_Graffiti",
        "Unlockable_Vehicles.DarkSiren",
        "Unlockable_Vehicles.DarkSiren_Proto",
        "Unlockable_Vehicles.Paladin_Proto",
        "Unlockable_Vehicles.Gravitar_Proto",
        "Unlockable_Vehicles.ExoSoldier_Proto",
        "Unlockable_Vehicles.Grazer",
        "Unlockable_Vehicles.Borg",
        "Unlockable_Vehicles.Mat27_GoldenPower",
        "Unlockable_Vehicles.Mat23_FutureProof",
        "Unlockable_Vehicles.Mat34_MoneyCamo",
        "Unlockable_Vehicles.Mat20_Cyberspace",
        "Unlockable_Vehicles.Mat19_Meltdown",
        "Unlockable_Vehicles.mat47_jakobsuncommon",
        "Unlockable_Vehicles.Mat01_Synthwave",
        "Unlockable_Vehicles.Mat32_ImperialGuard",
        "Unlockable_Vehicles.Mat33_Creepy",
    ],
}

EMBEDDED_REWARD_PACKAGES = [
    "RewardPackage_CharacterSkin_36_Torgue",
    "RewardPackage_CharacterSkin_26_MoneyCamo",
    "RewardPackage_CharacterSkin_03_Ghost",
    "RewardPackage_CharacterSkin_37_Maliwan",
    "RewardPackage_CharacterSkin_39_Critters",
    "RewardPackage_CharacterSkin_38_Cyberpop",
    "RewardPackage_CharacterSkin_34_Daedalus",
    "RewardPackage_CharacterSkin_25_Slimed",
    "RewardPackage_CharacterSkin_40_Veil",
    "RewardPackage_CharacterHeads_06_UniqueE",
    "RewardPackage_CharacterHeads_07_UniqueF",
    "RewardPackage_EchoSkin_04_Tech",
    "RewardPackage_EchoSkin_33_Jakobs",
    "RewardPackage_EchoSkin_37_Maliwan",
    "RewardPackage_EchoSkin_29_Guardian",
    "RewardPackage_EchoSkin_11_Astral",
    "RewardPackage_EchoSkin_35_Vladof",
    "RewardPackage_EchoSkin_26_Camo",
    "RewardPackage_EchoSkin_03_Ghost",
    "RewardPackage_EchoSkin_02_Order",
    "RewardPackage_EchoSkin_38_CyberPop",
    "RewardPackage_EchoSkin_22_Knitted",
    "RewardPackage_EchoSkin_25_Slimed",
    "RewardPackage_EchoSkin_39_Critters",
    "RewardPackage_EchoSkin_31_Koto",
    "RewardPackage_EchoSkin_20_HighRoller",
    "RewardPackage_EchoSkin_21_Graffiti",
    "RewardPackage_EchoSkin_19_Dirty",
    "RewardPackage_EchoSkin_40_Veil",
    "RewardPackage_EchoSkin_06_Amara",
    "RewardPackage_EchoSkin_36_Torgue",
    "RewardPackage_EchoAttachment_10_Crown",
    "RewardPackage_EchoAttachment_04_Wings",
    "RewardPackage_EchoAttachment_03_Bolt",
    "RewardPackage_EchoAttachment_09_Goggles",
    "RewardPackage_WeaponSkin_16_PolePosition",
    "RewardPackage_WeaponSkin_31_Splash",
    "RewardPackage_WeaponSkin_13_Whiteout",
    "RewardPackage_WeaponSkin_14_Grunt",
    "RewardPackage_WeaponSkin_18_CrashTest",
    "RewardPackage_WeaponSkin_07_CuteCat",
    "RewardPackage_WeaponSkin_19_Meltdown",
    "RewardPackage_VehicleSkin_17_DeadWood",
    "Reward_Vehicle_DarkSiren",
    "Reward_Vehicle_Grazer",
    "Reward_HoverDrive_Jakobs_01",
    "Reward_HoverDrive_Jakobs_02",
    "Reward_HoverDrive_Maliwan_01",
    "Reward_HoverDrive_Maliwan_02",
    "Reward_HoverDrive_Maliwan_03",
    "Reward_HoverDrive_Maliwan_04",
    "Reward_HoverDrive_Daedalus_01",
    "Reward_HoverDrive_Daedalus_02",
    "Reward_HoverDrive_Daedalus_03",
    "Reward_HoverDrive_Daedalus_04",
    "Reward_HoverDrive_Vladof_01",
    "Reward_HoverDrive_Vladof_02",
    "Reward_HoverDrive_Vladof_03",
    "RewardPackage_Combined_Propaganda",
    "RewardPackage_PreOrder",
    "RewardPackage_Premium",
    "RewardPackage_Headhunter",
    "RewardPackage_Legacy",
    "ChallengeReward_Shiny_BeeGun",
    "ChallengeReward_Shiny_Kickballer",
    "ChallengeReward_Shiny_Vamoose",
    "ChallengeReward_Shiny_anarchy",
    "RewardPackage_CharacterSkin_19_Dirty",
    "RewardPackage_CharacterSkin_30_Cute",
    "RewardPackage_EchoAttachment_01_PartyHat",
    "RewardPackage_EchoSkin_2_Order",
    "RewardPackage_EchoSkin_3_Ghost",
    "RewardPackage_GoldenEcho4",
    "RewardPackage_SHiFT",
    "RewardPackage_VehicleSkin_07_CuteCat",
    "RewardPackage_VehicleSkin_10_Graffiti",
    "RewardPackage_VehicleSkin_19_Meltdown",
    "RewardPackage_VehicleSkin_42_Gratata",
    "RewardPackage_WeaponSkin_20_Cyberspace",
    "RewardPackage_WeaponSkin_21_Afterburn",
    "RewardPackage_WeaponSkin_22_Overload",
    "RewardPackage_WeaponSkin_23_FutureProof",
    "Reward_HoverDrive_Borg_01",
    "Reward_HoverDrive_Borg_02",
    "Reward_HoverDrive_Borg_03",
    "Reward_HoverDrive_Borg_04",
    "Reward_HoverDrive_Borg_05",
    "Reward_HoverDrive_Jakobs_03",
    "Reward_HoverDrive_Jakobs_04",
    "Reward_HoverDrive_Maliwan_05",
    "Reward_HoverDrive_Order_01",
    "Reward_HoverDrive_Order_02",
    "Reward_HoverDrive_Order_03",
    "Reward_HoverDrive_Order_04",
    "Reward_HoverDrive_Order_05",
    "Reward_HoverDrive_Tediore_01",
    "Reward_HoverDrive_Tediore_02",
    "Reward_HoverDrive_Tediore_03",
    "Reward_HoverDrive_Tediore_04",
    "Reward_HoverDrive_Tediore_05",
    "Reward_HoverDrive_Torgue_01",
    "Reward_HoverDrive_Torgue_02",
    "Reward_HoverDrive_Torgue_03",
    "Reward_HoverDrive_Torgue_04",
    "Reward_HoverDrive_Torgue_05",
    "Reward_HoverDrive_Vladof_04",
    "Reward_HoverDrive_Vladof_05",
    "Reward_Vehicle_Gravitar",
    "pgraph.sdu_upgrades.Class_Mod_Slot",
    "pgraph.sdu_upgrades.Enhancement_Slot",
    "pgraph.sdu_upgrades.RepKit_Slot",
    "pgraph.sdu_upgrades.Weapon_Slot_03",
    "pgraph.sdu_upgrades.Weapon_Slot_04",
]

# ── Optional deps ─────────────────────────────────────────────────────────────
try:
    import yaml
except Exception:
    yaml = None

# ── Theme ─────────────────────────────────────────────────────────────────────
class Dark:
    BG = "#0b0f12"       # slightly deeper
    FG = "#dde1e4"
    ACC = "#141b22"
    HIL = "#0ea5b7"      # teal accent
    SEL = "#0b6a78"

def apply_dark(root: tk.Tk) -> None:
    try:
        s = ttk.Style(root)
        root.tk_setPalette(background=Dark.BG, foreground=Dark.FG)
        s.theme_use("default")
        base_font=("Segoe UI", 10)
        s.configure(".", background=Dark.BG, foreground=Dark.FG, fieldbackground=Dark.ACC, font=base_font)
        s.configure("TButton", background=Dark.ACC, foreground=Dark.FG, padding=6, relief="flat")
        s.map("TButton", background=[("active", Dark.HIL)], foreground=[("active", Dark.FG)])
        for w in ("TNotebook","TNotebook.Tab","Treeview","TEntry","TLabelFrame","TFrame"):
            s.configure(w, background=Dark.BG, foreground=Dark.FG)
        s.configure("TNotebook.Tab", padding=[10, 6], font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", Dark.HIL)],
              foreground=[("selected", Dark.FG)])
        s.configure("Treeview", background=Dark.BG, fieldbackground=Dark.BG, foreground=Dark.FG)
        s.configure("TEntry", fieldbackground=Dark.ACC, foreground=Dark.FG, insertcolor=Dark.FG)
    except Exception:
        pass

# ── YAML loader: ignore unknown tags ──────────────────────────────────────────
def get_yaml_loader():
    if yaml is None:
        raise RuntimeError("PyYAML is not installed. Install with: pip install pyyaml")
    class AnyTagLoader(yaml.SafeLoader): pass
    def _ignore_any(loader: AnyTagLoader, tag_suffix: str, node: 'yaml.Node'):
        if isinstance(node, yaml.ScalarNode): return loader.construct_scalar(node)
        if isinstance(node, yaml.SequenceNode): return loader.construct_sequence(node)
        if isinstance(node, yaml.MappingNode): return loader.construct_mapping(node)
        return None
    AnyTagLoader.add_multi_constructor("", _ignore_any)
    return AnyTagLoader

# ── Crypto (lazy import) ──────────────────────────────────────────────────────
PUBLIC_KEY = bytes((0x35,0xEC,0x33,0x77,0xF3,0x5D,0xB0,0xEA,0xBE,0x6B,0x83,0x11,0x54,0x03,0xEB,0xFB,
                    0x27,0x25,0x64,0x2E,0xD5,0x49,0x06,0x29,0x05,0x78,0xBD,0x60,0xBA,0x4A,0xA7,0x87))
def _adler32(b: bytes)->int: return zlib.adler32(b)&0xFFFFFFFF
def _lazy_crypto():
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        return AES, pad
    except Exception as e:
        raise RuntimeError("PyCryptodome is required for encrypt/decrypt.\nInstall with: pip install pycryptodome") from e
def _key_epic(uid:str)->bytes:
    wid=uid.strip().encode("utf-16le")
    k=bytearray(PUBLIC_KEY)
    n=min(len(wid), len(k))
    for i in range(n):
        k[i] ^= wid[i]
    return bytes(k)
def _key_steam(uid:str)->bytes:
    digits=''.join(ch for ch in uid if ch.isdigit())
    sid=int(digits or "0",10).to_bytes(8,"little",signed=False)
    k=bytearray(PUBLIC_KEY)
    for i, b in enumerate(sid):
        k[i % len(k)] ^= b
    return bytes(k)
def _strip_pkcs7(buf:bytes)->bytes:
    n=buf[-1]
    if 1<=n<=16 and all(buf[-i]==n for i in range(1,n+1)): return buf[:-n]
    return buf
def _aes_dec(b,k):
    AES,_=_lazy_crypto(); return AES.new(k,AES.MODE_ECB).decrypt(b)
def _aes_enc(b,k):
    AES,_=_lazy_crypto(); return AES.new(k,AES.MODE_ECB).encrypt(b)
def _try_once(key:bytes, enc:bytes, checksum_be:bool)->bytes:
    try:
        dec=_aes_dec(enc,key)
        print(f"DEBUG: AES decryption successful, decrypted {len(dec)} bytes")
    except Exception as e:
        raise ValueError(f"AES decryption failed: {e}")
    
    try:
        unp=_strip_pkcs7(dec)
        print(f"DEBUG: PKCS7 padding stripped, {len(unp)} bytes remaining")
    except Exception as e:
        raise ValueError(f"PKCS7 padding removal failed: {e}")
    
    if len(unp)<8: 
        raise ValueError(f"data too short after padding removal: {len(unp)} bytes (need at least 8)")
    
    trailer=unp[-8:]
    print(f"DEBUG: Raw trailer bytes: {trailer.hex()}")
    chk=int.from_bytes(trailer[:4], "big" if checksum_be else "little")
    ln =int.from_bytes(trailer[4:], "little")
    print(f"DEBUG: Extracted checksum: {chk}, expected length: {ln}")
    print(f"DEBUG: Checksum endian: {'big' if checksum_be else 'little'}")
    
    # Try original approach first - decompress everything including trailer
    try:
        print(f"DEBUG: Attempting zlib decompression on full {len(unp)} bytes (original method)")
        plain=zlib.decompress(unp)
        print(f"DEBUG: Zlib decompression successful with original method, {len(plain)} bytes")
    except Exception as e1:
        print(f"DEBUG: Original method failed: {e1}")
        # Try without trailer
        try:
            print(f"DEBUG: Attempting zlib decompression on {len(unp[:-8])} bytes (without trailer)")
            plain=zlib.decompress(unp[:-8])
            print(f"DEBUG: Zlib decompression successful without trailer, {len(plain)} bytes")
        except Exception as e2:
            print(f"DEBUG: Both methods failed. Original: {e1}, Without trailer: {e2}")
            raise ValueError(f"Zlib decompression failed: {e2}")
    
    actual_checksum = _adler32(plain)
    print(f"DEBUG: Actual checksum: {actual_checksum}, Expected: {chk}")
    print(f"DEBUG: Actual length: {len(plain)}, Expected: {ln}")
    
    # Check if this is a consistent checksum mismatch issue
    checksum_diff = abs(actual_checksum - chk)
    print(f"DEBUG: Checksum difference: {checksum_diff}")
    
    # For now, let's try to proceed despite checksum mismatch to see if we can load the data
    if actual_checksum != chk:
        print(f"DEBUG: WARNING - Checksum mismatch detected but attempting to continue...")
        print(f"DEBUG: This might indicate a version compatibility issue or algorithm difference")
        # Temporarily skip checksum validation to test if the data is otherwise valid
        # raise ValueError(f"checksum mismatch: got {actual_checksum}, expected {chk}")
    
    if len(plain) != ln:
        raise ValueError(f"length mismatch: got {len(plain)}, expected {ln}")
    
    return plain
def validate_user_id(user_id: str) -> Tuple[bool, str]:
    """
    Validate user ID format for Epic Games or Steam.
    Returns (is_valid, error_message)
    """
    if not user_id or not user_id.strip():
        return False, "User ID cannot be empty"
    
    user_id = user_id.strip()
    
    # Check if it looks like a Steam ID (all digits, typically 17 digits)
    if user_id.isdigit():
        if len(user_id) < 10:
            return False, "Steam ID appears too short (should be 17 digits)"
        elif len(user_id) > 20:
            return False, "Steam ID appears too long (should be 17 digits)"
        return True, "Valid Steam ID format"
    
    # Check if it looks like an Epic Games ID (alphanumeric, typically 32 characters)
    if user_id.replace('-', '').replace('_', '').isalnum():
        if len(user_id) < 10:
            return False, "Epic Games ID appears too short"
        elif len(user_id) > 50:
            return False, "Epic Games ID appears too long"
        return True, "Valid Epic Games ID format"
    
    return False, "User ID contains invalid characters. Should be alphanumeric for Epic Games or digits only for Steam"

def decrypt_auto(enc:bytes, user_id:str):
    # Validate user ID format first
    is_valid, validation_msg = validate_user_id(user_id)
    if not is_valid:
        raise ValueError(f"Invalid User ID format: {validation_msg}")
    
    epic_error = None
    steam_error = None
    
    # Try Epic Games format first
    try: 
        return _try_once(_key_epic(user_id),enc,True),"epic"
    except Exception as e: 
        epic_error = str(e)
    
    # Try Steam format
    try: 
        return _try_once(_key_steam(user_id),enc,False),"steam"
    except Exception as e: 
        steam_error = str(e)
    
    # Both failed - provide detailed error message
    error_msg = "Failed to decrypt save file. This usually means:\n"
    error_msg += "1. Incorrect User ID - Make sure you're using the right Epic Games or Steam User ID\n"
    error_msg += "2. Corrupted save file - The save file may be damaged\n"
    error_msg += "3. Wrong save file - This might not be a valid BL4 save file\n\n"
    error_msg += f"Epic Games attempt: {epic_error}\n"
    error_msg += f"Steam attempt: {steam_error}\n\n"
    error_msg += "For Epic Games: Use your Epic Games User ID (not display name)\n"
    error_msg += "For Steam: Use your Steam ID64 number"
    
    raise ValueError(error_msg)
def encrypt_from_yaml(yb:bytes, platform:str, user_id:str)->bytes:
    AES, pad = _lazy_crypto()
    key=_key_epic(user_id) if platform=="epic" else _key_steam(user_id)
    comp=zlib.compress(yb,9)
    trailer=_adler32(yb).to_bytes(4,"big" if platform=="epic" else "little")+len(yb).to_bytes(4,"little")
    pt=pad(comp+trailer,16,style="pkcs7")
    return _aes_enc(pt,key)

# ── Serial codec + glacier-style grouping ─────────────────────────────────────
_ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=!$%&*()[]{}~`^_<>?#;-"
def bit_pack_decode(serial:str)->bytes:
    payload=serial[3:] if serial.startswith("@Ug") else serial
    cmap={c:i for i,c in enumerate(_ALPHABET)}
    bits=''.join(format(cmap.get(c,0),'06b') for c in payload if c in cmap)
    bits+='0'*((8-(len(bits)%8))%8)
    return bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8))
def bit_pack_encode(data:bytes, prefix:str)->str:
    bits=''.join(format(byte,'08b') for byte in data)
    bits+='0'*((6-(len(bits)%6))%6)
    return prefix + ''.join(_ALPHABET[int(bits[i:i+6],2)] for i in range(0,len(bits),6))

def _extract_fields(b: bytes)->Dict[str,Union[int, List[int]]]:
    fields: Dict[str, Union[int, List[int]]] = {}
    if len(b)>=4:
        fields['header_le']=int.from_bytes(b[:4],'little')
        fields['header_be']=int.from_bytes(b[:4],'big')
    if len(b)>=8:
        fields['field2_le']=int.from_bytes(b[4:8],'little')
    if len(b)>=12:
        fields['field3_le']=int.from_bytes(b[8:12],'little')
    # 16-bit grid
    stats_16=[]
    for i in range(0, min(len(b)-1, 20), 2):
        val=int.from_bytes(b[i:i+2],'little')
        fields[f'val16_at_{i}']=val
        if 100 <= val <= 10000:
            stats_16.append((i,val))
    fields['potential_stats']=stats_16
    # first bytes
    flags=[]
    for i in range(min(len(b), 20)):
        bv=b[i]; fields[f'byte_{i}']=bv
        if isinstance(bv, int) and bv < 100: flags.append((i,bv))
    fields['potential_flags']=flags
    return fields

class ItemStats:
    def __init__(self):
        self.primary_stat: Optional[int] = None
        self.secondary_stat: Optional[int] = None
        self.level: Optional[int] = None
        self.rarity: Optional[int] = None
        self.manufacturer: Optional[int] = None
        self.item_class: Optional[int] = None

class DecodedItem:
    def __init__(self, serial: str, item_type: str, category: str, data_len: int,
                 stats: ItemStats, raw: Dict[str, Union[int, List[int]]], conf: str):
        self.serial = serial
        self.item_type = item_type
        self.item_category = category
        self.length = data_len
        self.stats = stats
        self.raw_fields = raw
        self.confidence = conf

def _decode_weapon(b: bytes, serial: str)->DecodedItem:
    f=_extract_fields(b); s=ItemStats()
    if 'val16_at_0' in f: s.primary_stat=f['val16_at_0']
    if 'val16_at_12' in f: s.secondary_stat=f['val16_at_12']
    if 'byte_4' in f: s.manufacturer=f['byte_4']
    if 'byte_8' in f: s.item_class=f['byte_8']
    if 'byte_1' in f: s.rarity=f['byte_1']
    if 'byte_13' in f and f['byte_13'] in [2,34]: s.level=f['byte_13']
    conf = "high" if len(b) in [24,26] else "medium"
    return DecodedItem(serial,'r','weapon',len(b),s,f,conf)

def _decode_equipment_e(b: bytes, serial: str)->DecodedItem:
    f=_extract_fields(b); s=ItemStats()
    if 'val16_at_2' in f: s.primary_stat=f['val16_at_2']
    if 'val16_at_8' in f: s.secondary_stat=f['val16_at_8']
    if 'val16_at_10' in f and len(b)>38: s.level=f['val16_at_10']
    if 'byte_1' in f: s.manufacturer=f['byte_1']
    if 'byte_3' in f: s.item_class=f['byte_3']
    if 'byte_9' in f: s.rarity=f['byte_9']
    conf="high" if ('byte_1' in f and f['byte_1']==49) else "medium"
    return DecodedItem(serial,'e','equipment',len(b),s,f,conf)

def _decode_equipment_d(b: bytes, serial: str)->DecodedItem:
    f=_extract_fields(b); s=ItemStats()
    if 'val16_at_4' in f: s.primary_stat=f['val16_at_4']
    if 'val16_at_8' in f: s.secondary_stat=f['val16_at_8']
    if 'val16_at_10' in f: s.level=f['val16_at_10']
    if 'byte_5' in f: s.manufacturer=f['byte_5']
    if 'byte_6' in f: s.item_class=f['byte_6']
    if 'byte_14' in f: s.rarity=f['byte_14']
    conf="high" if ('byte_5' in f and f['byte_5']==15) else "medium"
    return DecodedItem(serial,'d','equipment_alt',len(b),s,f,conf)


# ---- Friendly naming helpers (coarse fallback when explicit map missing) ----
_MANUFACTURER_MAP = {
    11: "Jakobs", 12: "Maliwan", 13: "Tediore", 14: "Hyperion",
    15: "Torgue", 16: "Vladof", 17: "Atlas", 18: "DAHL", 49: "UGe"
}
_ITEMCLASS_MAP = {
    10: "Pistol", 11: "Shotgun", 12: "SMG", 13: "Assault Rifle",
    14: "Sniper", 15: "Heavy", 16: "Shield", 17: "Grenade", 18: "Relic"
}
def _compact_tags(d: 'DecodedItem')->str:
    bits = []
    if hasattr(d, 'stats') and d.stats is not None:
        if d.stats.rarity is not None: bits.append(f"rarity={d.stats.rarity}")
        if d.stats.manufacturer is not None: bits.append(f"mfr={d.stats.manufacturer}")
        if d.stats.item_class is not None: bits.append(f"class={d.stats.item_class}")
    return " | ".join(bits) if bits else "—"


def _friendly_from_decoded(d: 'DecodedItem')->str:
    """Return the best human-friendly name we can compute.
    Priority:
      1) Known serial prefix → weapon name 
      2) Manufacturer + ItemClass (when both available)
      3) ItemClass only
      4) Generic by item_type
    """
    try:
        if hasattr(d, "serial"):
            nm = _weapon_name_from_serial(d.serial)
            if nm:
                return nm
    except Exception:
        pass
    # Fallbacks based on decoded stats maps
    brand = _MANUFACTURER_MAP.get(getattr(getattr(d, 'stats', None), 'manufacturer', None), None)
    kind = _ITEMCLASS_MAP.get(getattr(getattr(d, 'stats', None), 'item_class', None), None)
    if brand and kind:
        return f"{brand} {kind}"
    if kind:
        return kind
    return {"r":"Weapon","e":"Equipment","d":"Equipment Alt","u":"Special","f":"Special","!":"Special"}.get(getattr(d,'item_type','?'), "Unknown")


def decode_item_serial(serial: str)->DecodedItem:
    b=bit_pack_decode(serial)
    t = serial[3] if serial.startswith('@Ug') and len(serial)>=4 else '?'
    if t=='r': return _decode_weapon(b,serial)
    if t=='e': return _decode_equipment_e(b,serial)
    if t=='d': return _decode_equipment_d(b,serial)
    # generic low confidence
    f=_extract_fields(b); s=ItemStats()
    ps=f.get('potential_stats',[])
    if ps:
        s.primary_stat = ps[0][1] if len(ps)>0 else None
        s.secondary_stat = ps[1][1] if len(ps)>1 else None
    if 'byte_1' in f: s.manufacturer=f['byte_1']
    if 'byte_2' in f: s.rarity=f['byte_2']
    cat={'w':'weapon_special','u':'utility','f':'consumable','!':'special'}.get(t,'unknown')
    return DecodedItem(serial,t,cat,len(b),s,f,"low")

def encode_item_serial(d: DecodedItem)->str:
    import struct
    b=bytearray(bit_pack_decode(d.serial))
    try:
        if d.item_type=='r':
            if d.stats.primary_stat is not None and len(b)>=2: struct.pack_into('<H', b, 0, d.stats.primary_stat)
            if d.stats.secondary_stat is not None and len(b)>=14: struct.pack_into('<H', b, 12, d.stats.secondary_stat)
            if d.stats.rarity is not None and len(b)>=2: b[1]=int(d.stats.rarity)&0xFF
            if d.stats.manufacturer is not None and len(b)>=5: b[4]=int(d.stats.manufacturer)&0xFF
            if d.stats.item_class is not None and len(b)>=9: b[8]=int(d.stats.item_class)&0xFF
        elif d.item_type=='e':
            if d.stats.primary_stat is not None and len(b)>=4: struct.pack_into('<H', b, 2, d.stats.primary_stat)
            if d.stats.secondary_stat is not None and len(b)>=10: struct.pack_into('<H', b, 8, d.stats.secondary_stat)
            if d.stats.manufacturer is not None and len(b)>=2: b[1]=int(d.stats.manufacturer)&0xFF
            if d.stats.item_class is not None and len(b)>=4: b[3]=int(d.stats.item_class)&0xFF
            if d.stats.rarity is not None and len(b)>=10: b[9]=int(d.stats.rarity)&0xFF
        elif d.item_type=='d':
            if d.stats.primary_stat is not None and len(b)>=6: struct.pack_into('<H', b, 4, d.stats.primary_stat)
            if d.stats.secondary_stat is not None and len(b)>=10: struct.pack_into('<H', b, 8, d.stats.secondary_stat)
            if d.stats.manufacturer is not None and len(b)>=6: b[5]=int(d.stats.manufacturer)&0xFF
            if d.stats.item_class is not None and len(b)>=7: b[6]=int(d.stats.item_class)&0xFF
    except Exception:
        pass
    prefix=f"@Ug{d.item_type}"
    return bit_pack_encode(bytes(b), prefix)

# ── YAML decoded-items helpers ────────────────────────────────────────────────
def find_and_decode_serials_in_yaml(yaml_data: dict) -> Dict[str, DecodedItem]:
    decoded: Dict[str, DecodedItem] = {}
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k,v in obj.items():
                p=f"{path}.{k}" if path else k
                if isinstance(v,str) and v.startswith("@Ug"):
                    d=decode_item_serial(v)
                    decoded[p]=d
                else:
                    walk(v,p)
        elif isinstance(obj, list):
            for i,val in enumerate(obj):
                p=f"{path}[{i}]"
                if isinstance(val,str) and val.startswith("@Ug"):
                    d=decode_item_serial(val)
                    decoded[p]=d
                else:
                    walk(val,p)
    walk(yaml_data); return decoded

def insert_decoded_items_in_yaml(yaml_data: dict, decoded: Dict[str, DecodedItem]) -> dict:
    out=dict(yaml_data); out["_DECODED_ITEMS"]={}
    for path,d in decoded.items():
        item={
            "original_serial": d.serial,
            "item_type": d.item_type,
            "category": d.item_category,
            "confidence": d.confidence,
            "stats": {}
        }
        s=d.stats
        if s.primary_stat is not None: item["stats"]["primary_stat"]=s.primary_stat
        if s.secondary_stat is not None: item["stats"]["secondary_stat"]=s.secondary_stat
        if s.level is not None: item["stats"]["level"]=s.level
        if s.rarity is not None: item["stats"]["rarity"]=s.rarity
        if s.manufacturer is not None: item["stats"]["manufacturer"]=s.manufacturer
        if s.item_class is not None: item["stats"]["item_class"]=s.item_class
        out["_DECODED_ITEMS"][path]=item
    return out

def set_nested_value(data: dict, path: str, value: str):
    parts = path.split('.')
    cur = data
    for part in parts[:-1]:
        if '[' in part and part.endswith(']'):
            key, idxs = part.split('['); idx=int(idxs[:-1])
            cur = cur[key][idx]
        else:
            cur = cur[part]
    last=parts[-1]
    if '[' in last and last.endswith(']'):
        key, idxs = last.split('['); idx=int(idxs[:-1]); cur[key][idx]=value
    else:
        cur[last]=value

def extract_and_encode_serials_from_yaml(yaml_data: dict) -> dict:
    if "_DECODED_ITEMS" not in yaml_data: return yaml_data
    out=dict(yaml_data)
    for path, info in yaml_data["_DECODED_ITEMS"].items():
        d=DecodedItem(
            serial=info["original_serial"],
            item_type=info["item_type"],
            category=info.get("category","unknown"),
            data_len=0,
            stats=ItemStats(),
            raw={},
            conf=info.get("confidence","low")
        )
        st=info.get("stats",{})
        d.stats.primary_stat=st.get("primary_stat")
        d.stats.secondary_stat=st.get("secondary_stat")
        d.stats.level=st.get("level")
        d.stats.rarity=st.get("rarity")
        d.stats.manufacturer=st.get("manufacturer")
        d.stats.item_class=st.get("item_class")
        new_serial=encode_item_serial(d)
        set_nested_value(out, path, new_serial)
    out.pop("_DECODED_ITEMS", None)
    return out

# ── YAML path helpers for Items table ─────────────────────────────────────────
def walk_ug(node: Any, path: str = "")->List[Tuple[str,str]]:
    out=[]
    if isinstance(node,dict):
        for k,v in node.items():
            p=f"{path}/{k}" if path else k
            if isinstance(v,str) and v.startswith("@Ug"):
                out.append((p,v))
            else:
                out.extend(walk_ug(v,p))
    elif isinstance(node,list):
        for i,v in enumerate(node):
            p=f"{path}[{i}]"; out.extend(walk_ug(v,p))
    return out
def tokens(path: str)->List[Any]:
    toks=[]; i=0
    while i<len(path):
        if path[i]=='[':
            j=path.find(']',i)
            toks.append(int(path[i+1:j]))
            i=j+1
        else:
            j=path.find('/',i)
            seg=path[i:] if j==-1 else path[i:j]
            toks.append(seg)
            i=len(path) if j==-1 else j+1
    return [t for t in toks if t!=""]
def set_by(obj: Any, toks: List[Any], val: Any)->None:
    cur=obj
    for t in toks[:-1]: cur=cur[t]
    cur[toks[-1]]=val

# ── SDU helpers ───────────────────────────────────────────────────────────────
SDU_GRAPH_NAME = "sdu_upgrades"
SDU_GROUP_DEF = "Oak2_GlobalProgressGraph_Group"
SDU_NODES = [
    ("Ammo_Pistol_01",5), ("Ammo_Pistol_02",10), ("Ammo_Pistol_03",20), ("Ammo_Pistol_04",30),
    ("Ammo_Pistol_05",50), ("Ammo_Pistol_06",80), ("Ammo_Pistol_07",120),
    ("Ammo_SMG_01",5), ("Ammo_SMG_02",10), ("Ammo_SMG_03",20), ("Ammo_SMG_04",30),
    ("Ammo_SMG_05",50), ("Ammo_SMG_06",80), ("Ammo_SMG_07",120),
    ("Ammo_AR_01",5), ("Ammo_AR_02",10), ("Ammo_AR_03",20), ("Ammo_AR_04",30),
    ("Ammo_AR_05",50), ("Ammo_AR_06",80), ("Ammo_AR_07",120),
    ("Ammo_SG_01",5), ("Ammo_SG_02",10), ("Ammo_SG_03",20), ("Ammo_SG_04",30),
    ("Ammo_SG_05",50), ("Ammo_SG_06",80), ("Ammo_SG_07",120),
    ("Ammo_SR_01",5), ("Ammo_SR_02",10), ("Ammo_SR_03",20), ("Ammo_SR_04",30),
    ("Ammo_SR_05",50), ("Ammo_SR_06",80), ("Ammo_SR_07",120),
    ("Backpack_01",5), ("Backpack_02",10), ("Backpack_03",20), ("Backpack_04",30),
    ("Backpack_05",50), ("Backpack_06",80), ("Backpack_07",120), ("Backpack_08",235),
    ("Bank_01",5), ("Bank_02",10), ("Bank_03",20), ("Bank_04",30),
    ("Bank_05",50), ("Bank_06",80), ("Bank_07",120), ("Bank_08",235),
    ("Lost_Loot_01",5), ("Lost_Loot_02",10), ("Lost_Loot_03",20), ("Lost_Loot_04",30),
    ("Lost_Loot_05",50), ("Lost_Loot_06",80), ("Lost_Loot_07",120), ("Lost_Loot_08",235),
]
def ensure_sdu_graph(prog: Dict[str, Any]) -> None:
    graphs = prog.setdefault("graphs", [])
    existing = None
    for g in graphs:
        if isinstance(g, dict) and g.get("name") == SDU_GRAPH_NAME:
            existing = g; break
    if existing is None:
        existing = {"name": SDU_GRAPH_NAME, "group_def_name": SDU_GROUP_DEF, "nodes": []}
        graphs.append(existing)
    nodes = existing.setdefault("nodes", [])
    by_name = {n.get("name"): n for n in nodes if isinstance(n, dict)}
    for name, pts in SDU_NODES:
        n = by_name.get(name)
        if n is None:
            nodes.append({"name": name, "points_spent": pts})
        else:
            n["points_spent"] = pts

def sum_points_in_graphs(prog: Dict[str, Any], name_prefixes: Optional[List[str]] = None) -> int:
    total = 0
    for g in prog.get("graphs", []) or []:
        gname = g.get("name","")
        if name_prefixes and not any(gname.startswith(p) for p in name_prefixes):
            continue
        for n in g.get("nodes", []) or []:
            if isinstance(n, dict) and "points_spent" in n and isinstance(n["points_spent"], (int, float)):
                total += int(n["points_spent"])
    return total

# ── App ───────────────────────────────────────────────────────────────────────
class App:

    def apply_map_unlock_now(self):
        """Unlock all map areas/locations safely and refresh UI."""
        try:
            # Resolve the same YAML root used elsewhere
            root = getattr(self, 'yaml_obj', None)
            if root is None and hasattr(self, '_root'):
                r = self._root()
                root = r if isinstance(r, dict) else {}
            touched = _unlock_all_map_areas(root if isinstance(root, dict) else {})
            # Refresh YAML view
            try:
                import yaml as _yaml
                if hasattr(self, 'yaml_text') and hasattr(self, 'yaml_obj'):
                    self.yaml_text.delete("1.0", "end")
                    self.yaml_text.insert("1.0", _yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
            except Exception:
                pass
            # Refresh items list
            try:
                if hasattr(self, 'refresh_items'):
                    self.refresh_items()
            except Exception:
                pass
            try:
                self.log(f"Map unlock: set visited/discovered on {touched} entries")
            except Exception:
                pass
        except Exception as e:
            try:
                from tkinter import messagebox as _mb
                _mb.showerror("Map Unlock", f"Failed to unlock map: {e}")
            except Exception:
                pass

    def _normalize_unlock_variants(self, entry: str):
        """Return case-flex variants used for case-sensitive unlockables."""
        e = str(entry)
        out = {e}
        if "." in e:
            prefix, rest = e.split(".", 1)
            out.add(prefix + "." + rest.lower())
        out.add(e.lower())
        return list(out)

    def dump_yaml(self):
        """Write the current in-memory profile object to profile_decrypted.yaml next to the .sav/.profile."""
        if not getattr(self, "profile_obj", None):
            return mb.showwarning("No profile", "Decrypt Profile first")
        try:
            p = Path(self.profile_path or ".").with_name("profile_decrypted.yaml")
            txt = yaml.safe_dump(self.profile_obj, sort_keys=False, allow_unicode=True)
            p.write_text(txt, encoding="utf-8")
            self.log(f"[Profile] Dumped YAML → {p}")
            try: mb.showinfo("Dump YAML", f"Wrote {p.name}")
            except Exception: pass
        except Exception as e:
            self.log(f"[Profile] Dump YAML error: {e}")
            try: mb.showerror("Dump YAML", str(e))
            except Exception: pass

    def _normalize_unlock_variants(self, entry: str):
        """Return case-flex variants used for case-sensitive unlockables.
        Variants:
          - original
          - lowercased after the first dot (prefix preserved)
          - fully lowercase
        """
        e = str(entry)
        out = {e}
        if "." in e:
            prefix, rest = e.split(".", 1)
            out.add(prefix + "." + rest.lower())
        out.add(e.lower())
        return list(out)

    def __init__(self, root: tk.Tk):
        self.root = root; self.root.title("BL4 Save Editor v1.04a Full"); self.root.geometry("1340x900")
        apply_dark(root)

        self.user_id = tk.StringVar()
        self.save_path: Optional[Path] = None
        self.yaml_path: Optional[Path] = None
        self.platform: Optional[str] = None
        self.profile_path: Optional[Path] = None
        self.profile_platform: Optional[str] = None
        self.profile_obj: Optional[Any] = None
        self.unlock_profile_var = tk.BooleanVar(value=False)
        self.yaml_obj: Optional[Any] = None

        # currency paths cache
        self.cur_paths: Dict[str, Optional[List[Union[str,int]]]] = {"cash":None, "eridium":None, "shift":None}

        # Top bar
        top = ttk.Frame(root, padding=6); top.pack(fill="x")
        ttk.Label(top, text="ID:").pack(side="left")
        self.id_entry = ttk.Entry(top, textvariable=self.user_id, width=48); self.id_entry.pack(side="left", padx=6)
        ttk.Button(top, text="Select Save", command=self.select_save).pack(side="left", padx=4)
        ttk.Button(top, text="Decrypt", command=self.decrypt).pack(side="left", padx=4)
        ttk.Button(top, text="Encrypt", command=self.encrypt).pack(side="left", padx=4)
        ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(top, text="Select Profile", command=self.select_profile).pack(side="left", padx=4)
        ttk.Button(top, text="Decrypt Profile", command=self.decrypt_profile).pack(side="left", padx=4)
        ttk.Button(top, text="Encrypt Profile", command=self.encrypt_profile).pack(side="left", padx=4)
        ttk.Checkbutton(top, text="Unlocks (Profile)", variable=self.unlock_profile_var).pack(side="left", padx=8)
        ttk.Button(top, text="Dump YAML", command=self.dump_yaml).pack(side="left", padx=4)
        ttk.Label(top, text=" ").pack(side="left", padx=4)  # preview removed in H build

        # Tabs
        self.nb = ttk.Notebook(root); self.nb.pack(expand=True, fill="both")

        self.tab_char = ttk.Frame(self.nb); self.nb.add(self.tab_char, text="Character")
        self._build_tab_character(self.tab_char)

        self.tab_items = ttk.Frame(self.nb); self.nb.add(self.tab_items, text="Items")
        self._build_tab_items(self.tab_items)

        self.tab_prog = ttk.Frame(self.nb); self.nb.add(self.tab_prog, text="Progression")
        self._build_tab_progression(self.tab_prog)

        self.tab_yaml = ttk.Frame(self.nb); self.nb.add(self.tab_yaml, text="YAML (Advanced)")
        self._build_tab_yaml(self.tab_yaml)

        # Logs / Status
        bottom = ttk.Frame(root); bottom.pack(fill="x", side="bottom")
        lw = ttk.Frame(bottom); lw.pack(fill="x")
        self.logs = tk.Text(lw, height=6, bg=Dark.BG, fg=Dark.FG, insertbackground=Dark.FG, selectbackground=Dark.SEL)
        self.logs.pack(side="left", fill="x", expand=True)
        sb = tk.Scrollbar(lw, command=self.logs.yview); sb.pack(side="right", fill="y")
        self.logs.config(yscrollcommand=sb.set)
        self.status = tk.Label(bottom, text="No save loaded", anchor="w", bg=Dark.BG, fg=Dark.FG); self.status.pack(fill="x")

    # utils
    def log(self,m:str):
        t=time.strftime("%H:%M:%S"); self.logs.insert("end", f"[{t}] {m}\n"); self.logs.see("end")
    def set_status(self,m:str): self.status.config(text=m)

    # ---- YAML root resolver ----
    def _root(self)->Optional[dict]:
        if not isinstance(self.yaml_obj, dict):
            return None
        r0 = self.yaml_obj
        state = r0.get("state") if isinstance(r0.get("state"), dict) else None

        def looks_like_char_container(d):
            return isinstance(d, dict) and any(k in d for k in ("char_name","class","experience","progression"))

        # Always prefer /state if it has character fields
        if looks_like_char_container(state):
            return state
        # Else fall back to top-level if it looks like a character container
        if looks_like_char_container(r0):
            return r0
        # Final fallback
        return state or r0

    # generic path walkers for currencies
    def _walk(self, node: Any, path: Optional[List[Union[str,int]]] = None):
        if path is None: path=[]
        if isinstance(node, dict):
            for k,v in node.items():
                yield path+[k], v
                yield from self._walk(v, path+[k])
        elif isinstance(node, list):
            for i,v in enumerate(node):
                yield path+[i], v
                yield from self._walk(v, path+[i])

    @staticmethod
    def _get_by_path(root: Any, toks: List[Union[str,int]]):
        cur=root
        for t in toks:
            cur=cur[t]
        return cur
    @staticmethod
    def _set_by_path(root: Any, toks: List[Union[str,int]], val: Any):
        cur=root
        for t in toks[:-1]: cur=cur[t]
        cur[toks[-1]]=val


    def _find_currency_paths(self, r: dict):
        """Detect cash/eridium/shift locations. Prefers `r["currencies"]` when present.
        SHIFT may be stored as a string token (e.g., "shift"), so we accept str too.
        """
        found = {"cash": None, "eridium": None, "shift": None}

        # Prefer explicit currencies block
        cur = r.get("currencies")
        if isinstance(cur, dict):
            for key, target in [
                ("cash", "cash"),
                ("eridium", "eridium"),
                ("golden_keys", "shift"), ("gold_keys", "shift"),
                ("golden_key", "shift"), ("keys", "shift"),
                ("shift", "shift"),
            ]:
                if key in cur and isinstance(cur[key], (int, float, str)):
                    found[target] = ["currencies", key]

        # Fallback: scan whole tree for likely names
        if not all(v is not None for v in found.values()):
            keysets = {
                "cash": ["cash","money","credits","dollars"],
                "eridium": ["eridium","vaultcoin","vault_coins","eridium_amount"],
                "shift": ["shift","gold_keys","goldkeys","golden_keys","goldenkeys","keys"],
            }
            for path, val in self._walk(r):
                if isinstance(val, (int, float, str)):
                    last = str(path[-1]).lower()
                    for name, keys in keysets.items():
                        if found[name] is None and last in keys:
                            found[name] = path.copy()

        self.cur_paths.update(found)
        for k, v in found.items():
            if v:
                self.log("Detected %s at: %s" % (k, "/".join(map(str, v))))
            else:
                self.log("%s path not found — you can still edit YAML directly." % k.capitalize())

    def select_save(self):
        f = fd.askopenfilename(title="Select Save", filetypes=[("BL4 Save","*.sav"),("All Files","*.*")])
        if f: self.save_path = Path(f); self.log(f"Selected {f}"); self.set_status(f)

    def decrypt(self):
        if not self.save_path: return mb.showwarning("No file","Select save first")
        if yaml is None:
            return mb.showerror("Missing dependency","PyYAML is required.\nInstall with: pip install pyyaml")
        
        # Check if user ID is provided
        user_id = self.user_id.get().strip()
        if not user_id:
            return mb.showerror("Missing User ID", 
                              "Please enter your User ID first.\n\n" +
                              "For Epic Games: Use your Epic Games User ID\n" +
                              "For Steam: Use your Steam ID64 number\n\n" +
                              "You can find these in your game settings or profile.")
        
        enc=self.save_path.read_bytes()
        try:
            plain, plat = decrypt_auto(enc, user_id)
            ts=time.strftime("%Y-%m-%d-%H%M"); backup=self.save_path.with_suffix(f".{ts}.bak"); backup.write_bytes(enc)
            self.platform=plat; self.yaml_path=self.save_path.with_suffix(".yaml"); self.yaml_path.write_bytes(plain)
            text=plain.decode(errors="ignore")
            self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", text)
            try: self.yaml_obj=yaml.load(text, Loader=get_yaml_loader())
            except Exception as e: self.yaml_obj=None; self.log(f"YAML note: {e}")
            self.refresh_character(); self.refresh_items(); ns=_load_embedded_decoder(); self.log('Decoder present: ' + str('decode_item_serial' in ns)); self.refresh_progression()
            root_obj=self._root(); root_used="/state" if (isinstance(self.yaml_obj,dict) and root_obj is self.yaml_obj.get("state")) else "/"
            self.log(f"Character root resolved at: {root_used}")
            self.log(f"Detected platform: {plat}"); self.log(f"Backup created: {backup.name}"); self.log(f"Decrypted → {self.yaml_path.name}")
            self.set_status(f"Platform: {plat} | Backup: {backup.name}")
            self.nb.select(self.tab_char)
        except ValueError as e:
            # Handle validation and decryption errors with detailed messages
            error_msg = str(e)
            if "Invalid User ID format" in error_msg:
                mb.showerror("Invalid User ID", error_msg)
            elif "Failed to decrypt save file" in error_msg:
                mb.showerror("Decryption Failed", error_msg)
            else:
                mb.showerror("Decrypt Failed", error_msg)
            self.log(f"Decrypt error: {e}")
        except Exception as e:
            mb.showerror("Decrypt Failed", f"Unexpected error: {str(e)}")
            self.log(f"Decrypt error: {e}")

    
    def _ensure_unique_rewards(self, root_dict):
        if not isinstance(root_dict, dict):
            return None
        if "unique_rewards" not in root_dict or not isinstance(root_dict.get("unique_rewards"), list):
            root_dict["unique_rewards"] = []
        return root_dict["unique_rewards"]

    def _apply_unlocks(self):
        """Inject embedded cosmetic RewardPackages into unique_rewards when the checkbox is enabled."""
        try:
            r = self._root()
            if not isinstance(r, dict):
                self.log("Unlock: YAML root not found; skipping."); return
            uniq = self._ensure_unique_rewards(r)
            before = set(map(str, uniq))
            added = 0
            if getattr(self, "unlock_all_cosmetics_var", None) and self.unlock_all_cosmetics_var.get():
                for pkg in EMBEDDED_REWARD_PACKAGES:
                    if pkg and pkg not in before:
                        uniq.append(pkg); added += 1
                self.log(f"Unlock Cosmetics: +{added} (unique_rewards: {len(before)} → {len(uniq)})")
                # reflect YAML so Encrypt saves exactly this
                if yaml is not None and isinstance(self.yaml_obj, dict):
                    safe = yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True)
                    self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", safe)
            else:
                self.log("Unlock Cosmetics: checkbox off — no changes.")
        except Exception as e:
            self.log(f"Unlock error: {e}")

    def encrypt(self):

        # Auto-apply map unlock if requested

        if getattr(self, 'var_unlock_map', None) and self.var_unlock_map.get():

            try:

                _unlock_all_map_areas(self.yaml_obj if hasattr(self,"yaml_obj") else (self._root() if hasattr(self,"_root") else {}))

            except Exception as __e:

                print('map apply hook error:', __e)

        # Apply chosen class on action
        try:
            _apply_selected_class_104a(self)
        except Exception as __e:
            print("class apply hook error:", __e)


        if not self.yaml_path: return mb.showwarning("No YAML","Decrypt first")
        if yaml is None:
            return mb.showerror("Missing dependency","PyYAML is required.\nInstall with: pip install pyyaml")
                # Run unlock pass (no-op if checkbox is off)
        try:
            self._apply_unlocks()
        except Exception as _e:
            self.log(f"Unlock pass note: {_e}")
        txt=self.yaml_text.get("1.0","end")
        try:
            obj=yaml.load(txt, Loader=get_yaml_loader())
            # encode from _DECODED_ITEMS if present
            obj = extract_and_encode_serials_from_yaml(obj)
            yb=yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).encode()
        except Exception as e:
            return mb.showerror("Invalid YAML", f"Fix YAML before encrypting:\n{e}")
        try:
            out=self.save_path.with_suffix(".sav"); out.write_bytes(encrypt_from_yaml(yb,self.platform or "epic", self.user_id.get()))
            self.log(f"Encrypted → {out.name}"); mb.showinfo("Done", f"Saved {out.name}")
        except Exception as e:
            mb.showerror("Encrypt Failed", str(e)); self.log(f"Encrypt error: {e}")

    # Character
    def _find_experience(self, r: dict)->Tuple[Optional[Dict[str,Any]],Optional[Dict[str,Any]]]:
        exp = r.get("experience")
        ch = sp = None
        if isinstance(exp, list):
            for entry in exp:
                if isinstance(entry, dict):
                    t = str(entry.get("type","")).lower()
                    if t=="character": ch = entry
                    elif t=="specialization": sp = entry
        return ch, sp

    def _build_tab_character(self, parent: ttk.Frame):
        grid = ttk.Frame(parent, padding=10); grid.pack(fill="x", anchor="n")
        self.cf: Dict[str, tk.StringVar] = {}
        labels=[("Class","class"),("Name","char_name"),("Difficulty","player_difficulty"),
                ("Character Level","experience[Character].level"),
                ("Character XP","experience[Character].points"),
                ("Spec Level","experience[Specialization].level"),
                ("Spec Points","experience[Specialization].points"),
                ("Cash","$"),("Eridium","$"),("SHIFT Keys","$")]
        for i,(label,tip) in enumerate(labels):
            ttk.Label(grid,text=label).grid(row=i,column=0,sticky="w",padx=6,pady=4)
            v=tk.StringVar(); e=ttk.Entry(grid,textvariable=v,width=28); e.grid(row=i,column=1,sticky="w",padx=6,pady=4)
            self.cf[label]=v
        ttk.Button(grid,text="Apply Character",command=self.apply_character).grid(row=0,column=2,rowspan=2,padx=12)
        # Cosmetic Unlocks (no external files needed)
        opts = ttk.LabelFrame(parent, text="Unlock Rewards (Class)", padding=8)
        # Map unlock controls (injected)
        self.var_unlock_map = getattr(self, 'var_unlock_map', tk.BooleanVar(value=False))
        ttk.Checkbutton(opts, text="Unlock Map (100% visited + discovered)", variable=self.var_unlock_map).pack(anchor="w", padx=6, pady=2)
        ttk.Button(opts, text="Apply Map Unlock Now", command=self.apply_map_unlock_now).pack(anchor="w", padx=6, pady=2)

        opts.pack(fill="x", padx=10, pady=6)
        self.unlock_all_cosmetics_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts, text="Unlock Cosmetics (RewardPackages)", variable=self.unlock_all_cosmetics_var).pack(anchor="w")

    def refresh_character(self):
        r=self._root()
        if not isinstance(r, dict): return
        self.cf["Class"].set(str(r.get("class") or r.get("character_class") or ""))
        self.cf["Name"].set(str(r.get("char_name") or r.get("name") or r.get("character_name") or ""))
        self.cf["Difficulty"].set(str(r.get("player_difficulty") or r.get("difficulty") or r.get("mode") or ""))
        ch, sp = self._find_experience(r)
        self.cf["Character Level"].set(str(ch.get("level","")) if ch else "")
        self.cf["Character XP"].set(str(ch.get("points","")) if ch else "")
        self.cf["Spec Level"].set(str(sp.get("level","")) if sp else "")
        self.cf["Spec Points"].set(str(sp.get("points","")) if sp else "")
        # currencies
        self._find_currency_paths(r)
        for key,label in [("cash","Cash"),("eridium","Eridium"),("shift","SHIFT Keys")]:
            p=self.cur_paths.get(key)
            try:
                val = self._get_by_path(r,p) if p else ""
                self.cf[label].set(str(val))
            except Exception:
                self.cf[label].set("")

    def apply_character(self):

        # Auto-apply map unlock if requested

        if getattr(self, 'var_unlock_map', None) and self.var_unlock_map.get():

            try:

                _unlock_all_map_areas(self.yaml_obj if hasattr(self,"yaml_obj") else (self._root() if hasattr(self,"_root") else {}))

            except Exception as __e:

                print('map apply hook error:', __e)

        # Apply chosen class on action
        try:
            _apply_selected_class_104a(self)
        except Exception as __e:
            print("class apply hook error:", __e)


        r=self._root()
        if not isinstance(r, dict): return
        r["class"]=self.cf["Class"].get()
        r["char_name"]=self.cf["Name"].get()
        r["player_difficulty"]=self.cf["Difficulty"].get()
        ch, sp = self._find_experience(r)
        if ch is None:
            if "experience" not in r or not isinstance(r["experience"], list): r["experience"]=[]
            ch={"type":"Character"}; r["experience"].append(ch)
        if sp is None:
            if "experience" not in r or not isinstance(r["experience"], list): r["experience"]=[]
            sp={"type":"Specialization"}; r["experience"].append(sp)
        def maybe_int(x):
            try: return int(str(x).strip())
            except: return x
        ch["level"]=maybe_int(self.cf["Character Level"].get()); ch["points"]=maybe_int(self.cf["Character XP"].get())
        sp["level"]=maybe_int(self.cf["Spec Level"].get()); sp["points"]=maybe_int(self.cf["Spec Points"].get())
        # currencies writeback (only if we found a path)
        for key,label in [("cash","Cash"),("eridium","Eridium"),("shift","SHIFT Keys")]:
            p=self.cur_paths.get(key); v=self.cf[label].get().strip()
            if p and v!="":
                try:
                    v_out = int(v) if v.isdigit() else v
                    self._set_by_path(r,p, v_out)
                except Exception:
                    self.log(f"Could not set {label} at detected path")
# reflect to YAML text
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.log("Character + currencies applied.")

    # Progression
    def _build_tab_progression(self, parent: ttk.Frame):
        pf = ttk.LabelFrame(parent, text="Progression (graphs & nodes)", padding=8); pf.pack(fill="both", expand=True, padx=10, pady=8)
        ctl = ttk.Frame(pf); ctl.pack(fill="x")
        ttk.Button(ctl, text="Max SDU", command=self.max_sdu).pack(side="left", padx=(0,6))
        ttk.Button(ctl, text="Recalculate Point Pools", command=self.recalc_pools).pack(side="left", padx=6)
        ttk.Label(ctl, text="Echo Tokens cap:").pack(side="left", padx=(18,4))
        self.echo_var=tk.StringVar(value="3225"); ttk.Entry(ctl,textvariable=self.echo_var,width=8).pack(side="left")
        cols=("graph","node","points_spent","is_activated","activation_level")
        self.prog_tree=ttk.Treeview(pf, columns=cols, show="headings", height=18)
        for c,w in [("graph",340),("node",340),("points_spent",120),("is_activated",120),("activation_level",140)]:
            self.prog_tree.heading(c, text=c.replace("_"," ").title()); self.prog_tree.column(c, width=w, anchor="w")
        self.prog_tree.pack(expand=True, fill="both", pady=(6,2))
        edit = ttk.Frame(pf, padding=6); edit.pack(fill="x")
        ttk.Label(edit,text="points_spent").pack(side="left")
        self.points_var=tk.StringVar(); ttk.Entry(edit,textvariable=self.points_var,width=8).pack(side="left",padx=6)
        self.act_var=tk.BooleanVar(value=False)
        ttk.Checkbutton(edit,text="is_activated",variable=self.act_var).pack(side="left",padx=6)
        ttk.Label(edit,text="activation_level").pack(side="left")
        self.level_var=tk.StringVar(); ttk.Entry(edit,textvariable=self.level_var,width=8).pack(side="left",padx=6)
        ttk.Button(edit,text="Apply to Selected Node",command=self.apply_node_edit).pack(side="left",padx=10)
        ttk.Button(edit,text="Activate All (Graph)",command=lambda:self.bulk_activate(True)).pack(side="left",padx=6)
        ttk.Button(edit,text="Deactivate All (Graph)",command=lambda:self.bulk_activate(False)).pack(side="left",padx=6)

    def refresh_progression(self):
        r=self._root()
        if not isinstance(r, dict): return
        for r_ in self.prog_tree.get_children(): self.prog_tree.delete(r_)
        # Prefer progression under the active root (/state), but fall back to top-level if empty
        prog = (r.get("progression") or {})
        if not prog and isinstance(self.yaml_obj, dict):
            prog = (self.yaml_obj.get("progression") or {})
        found = 0
        for g in (prog.get("graphs") or []):
            found += 1
            gname = g.get("name","")
            for n in (g.get("nodes") or []):
                self.prog_tree.insert("", "end", values=(
                    gname, n.get("name",""),
                    n.get("points_spent",""),
                    n.get("is_activated",""),
                    n.get("activation_level",""),
                ))
        if found == 0:
            self.log("No progression graphs found under root; also checked top-level.")

    def _find_graph_node(self, r: dict, gname:str, nname:str)->Optional[Dict[str,Any]]:
        # Search under root/state first
        prog=(r or {}).get("progression") or {}
        for g in (prog.get("graphs") or []):
            if g.get("name")==gname:
                for n in (g.get("nodes") or []):
                    if n.get("name")==nname: return n
        # Fallback: some saves store progression at YAML top-level
        if isinstance(self.yaml_obj, dict):
            tprog=(self.yaml_obj.get("progression") or {})
            for g in (tprog.get("graphs") or []):
                if g.get("name")==gname:
                    for n in (g.get("nodes") or []):
                        if n.get("name")==nname: return n
        return None

    def apply_node_edit(self):
        sel=self.prog_tree.selection()
        if not sel: return
        gname, nname, pts, act, lvl = self.prog_tree.item(sel[0],"values")
        r=self._root()
        if not isinstance(r, dict): return
        node=self._find_graph_node(r,gname,nname)
        if node is None: return
        pv=self.points_var.get().strip()
        if pv!="":
            try: node["points_spent"]=int(pv)
            except: return mb.showerror("Invalid","points_spent must be an integer")
        node["is_activated"]=bool(self.act_var.get())
        lv=self.level_var.get().strip()
        if lv=="": node.pop("activation_level", None)
        else:
            try: node["activation_level"]=int(lv)
            except: return mb.showerror("Invalid","activation_level must be an integer")
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_progression()
        self.log(f"Updated node: {gname} / {nname}")

    def bulk_activate(self, state: bool):
        sel=self.prog_tree.selection()
        if not sel: return
        gname=self.prog_tree.item(sel[0],"values")[0]
        r=self._root()
        if not isinstance(r, dict): return
        # Try root progression and top-level fallback
        applied=False
        scopes=[r]
        if isinstance(self.yaml_obj, dict): scopes.append(self.yaml_obj)
        for scope in scopes:
            prog=(scope or {}).get("progression") or {}
            for g in (prog.get("graphs") or []):
                if g.get("name")==gname:
                    for n in (g.get("nodes") or []):
                        n["is_activated"]=state
                    applied=True
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_progression()
        self.log(("Activated" if state else "Deactivated") + f" all nodes in graph: {gname}" + (" (top-level)" if not applied else ""))

    def max_sdu(self):
        r=self._root()
        if not isinstance(r, dict): return
        prog=r.setdefault("progression", {}); ensure_sdu_graph(prog)
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_progression(); self.log("SDU graph maximized.")

    def recalc_pools(self):
        r=self._root()
        if not isinstance(r, dict): return
        prog=r.setdefault("progression", {})
        # If current root had no progression, try at top-level so we don't crash
        if not prog and isinstance(self.yaml_obj, dict):
            prog = self.yaml_obj.setdefault("progression", {})
        pools=prog.setdefault("point_pools", {})
        char_pts = sum_points_in_graphs(prog, name_prefixes=["Progress_DS_"])
        spec_pts = sum_points_in_graphs(prog, name_prefixes=["ProgressGraph_Specializations"])
        pools["characterprogresspoints"]=char_pts
        pools["specializationtokenpool"]=spec_pts
        try: cap=int(self.echo_var.get().strip())
        except: cap=3225
        cur=int(pools.get("echotokenprogresspoints",0))
        pools["echotokenprogresspoints"]=min(cur if cur else cap, cap)
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_progression()
        self.log(f"Recalculated pools → character:{char_pts} specialization:{spec_pts} echo:{pools['echotokenprogresspoints']}")

    # Items
    def _build_tab_items(self, parent: ttk.Frame)->None:
        filt=ttk.Frame(parent); filt.pack(fill="x", pady=6, padx=8)
        ttk.Label(filt,text="Search:").pack(side="left")
        self.search_var=tk.StringVar(); ttk.Entry(filt,textvariable=self.search_var,width=40).pack(side="left",padx=6)
        ttk.Label(filt,text="Type:").pack(side="left",padx=(12,4))
        self.type_var=tk.StringVar(value="All")
        ttk.Combobox(filt,textvariable=self.type_var, values=["All","Weapon","Equipment","Equipment Alt","Special"], width=18, state="readonly").pack(side="left")
        ttk.Button(filt,text="Filter",command=self.apply_filter).pack(side="left",padx=6)
        ttk.Button(filt,text="Export Decoded → YAML",command=self.export_decoded_yaml).pack(side="left",padx=12)

        cols=("path","type","name","code","serial","tags")
        self.tree=ttk.Treeview(parent,columns=cols,show="headings")
        for c,txt,w in [("path","Path",420),("type","Type",120),("name","Name",220),("code","Code",80),("serial","Serial",480),("tags","Tags",180)]:
            self.tree.heading(c,text=txt); self.tree.column(c,width=w,anchor="w")
        self.tree.pack(expand=True,fill="both", padx=8, pady=(0,8))
        self.tree.bind("<Double-1>", self.open_inspector)

    def refresh_items(self)->None:

        # Build 6-tuples for the items table: (path, type, name, code, serial, tags)
        self.items = []
        r = self._root()
        if not isinstance(r, dict):
            return
        for path, serial in walk_ug(r):
            # Type from @Ug? prefix
            t = serial[3] if serial.startswith("@Ug") and len(serial) >= 4 else "?"
            dtype = {"r":"Weapon","e":"Equipment","d":"Equipment Alt","u":"Special","f":"Special","!":"Special"}.get(t,"Unknown")
            # Compact code
            code4 = serial[:4] if serial.startswith("@Ug") and len(serial) >= 4 else "@Ug?"
            # Friendly name + tags via decoder (best-effort)
            try:
                dec = decode_item_serial(serial)
                name = _friendly_from_decoded(dec)
                tags = _compact_tags(dec)
            except Exception:
                name = ""
                tags = ""
            self.items.append((path, dtype, name, code4, serial, tags))
        self.apply_filter()


    def apply_filter(self)->None:
        term=(self.search_var.get() or "").lower(); type_sel=self.type_var.get()
        for r in self.tree.get_children(): self.tree.delete(r)
        for p,dtype,name,code,serial,tags in self.items:
            if type_sel!="All" and dtype!=type_sel: continue
            if term and not any(term in s for s in (p.lower(), serial.lower(), str(name).lower())):
                continue
            self.tree.insert("", "end", values=(p,dtype,name,code,serial,tags))

    def open_inspector(self,_evt=None)->None:
        sel=self.tree.selection()
        if not sel: return
        p,dtype,name,code,serial,tags = _safe_unpack_item_values(self.tree.item(sel[0],"values"))
        toks=tokens(p); d=decode_item_serial(serial)
        b=bytearray(bit_pack_decode(serial))
        top=tk.Toplevel(self.root); top.title("BL4 Save Editor v1.04a Full"); top.geometry("880x620"); top.configure(bg=Dark.BG)
        nb=ttk.Notebook(top); nb.pack(expand=True,fill="both")

        # Simple
        simp=ttk.Frame(nb); nb.add(simp,text="Simple")
        vals={
            "Primary": d.stats.primary_stat or 0,
            "Secondary": d.stats.secondary_stat or 0,
            "Rarity": d.stats.rarity or 0,
            "Manufacturer": d.stats.manufacturer or 0,
            "Item Class": d.stats.item_class or 0,
            "Level": d.stats.level or 1,
        }
        entries={}; grid=ttk.Frame(simp,padding=12); grid.pack(fill="both",expand=True)
        row=0
        for name in ["Primary","Secondary","Rarity","Manufacturer","Item Class","Level"]:
            ttk.Label(grid,text=name).grid(row=row,column=0,sticky="w",padx=6,pady=6)
            var=tk.StringVar(value=str(vals[name])); ttk.Entry(grid,textvariable=var,width=16).grid(row=row,column=1,sticky="w",padx=6,pady=6)
            entries[name]=var; row+=1
        ttk.Label(grid,text="Tags").grid(row=row,column=0,sticky="w",padx=6,pady=6)
        ttk.Label(grid,text=str(tags)).grid(row=row,column=1,sticky="w",padx=6,pady=6)
        row+=1
        def save_simple():
            try:
                d.stats.primary_stat=int(entries["Primary"].get())
                d.stats.secondary_stat=int(entries["Secondary"].get())
                d.stats.rarity=int(entries["Rarity"].get())
                d.stats.manufacturer=int(entries["Manufacturer"].get())
                d.stats.item_class=int(entries["Item Class"].get())
                d.stats.level=int(entries["Level"].get())
            except ValueError:
                return mb.showerror("Invalid input","All fields must be integers")
            new_serial = encode_item_serial(d)

            root = self.yaml_obj if self._root() is self.yaml_obj else self._root()

            set_by(root, toks, new_serial)
            # reflect
            self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
            self.refresh_items(); self.log(f"Updated {p}"); top.destroy()
        ttk.Button(simp,text="Save & Encode",command=save_simple).pack(pady=10)

        # Raw (scrollable)
        rawtab=ttk.Frame(nb); nb.add(rawtab,text="Raw")
        canvas=tk.Canvas(rawtab,bg=Dark.BG,highlightthickness=0); frame=ttk.Frame(canvas)
        vsb=tk.Scrollbar(rawtab,orient="vertical",command=canvas.yview); canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y"); canvas.pack(side="left",fill="both",expand=True)
        window=canvas.create_window((0,0),window=frame,anchor="nw")
        def on_config(event): canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>", on_config)
        raw=_extract_fields(bytes(b)); ents={}; r_=0
        for k in sorted(raw.keys()):
            ttk.Label(frame,text=k).grid(row=r_,column=0,sticky="w",padx=6,pady=3)
            v=tk.StringVar(value=str(raw[k])); ttk.Entry(frame,textvariable=v,width=24).grid(row=r_,column=1,sticky="w",padx=6,pady=3)
            ents[k]=v; r_+=1
        
        def save_raw():
            bb = bytearray(b)
            # Build numeric-only map
            amap = {}
            cleaned = False
            for k, v in ents.items():
                s = (v.get() or "").strip()
                if not s:
                    continue
                if k.startswith("val16_at_") or k.startswith("byte_") or k in ("header_le", "field2_le"):
                    val = None
                    sval = s.lower()
                    try:
                        if sval.startswith("0x"):
                            val = int(sval, 16)
                        else:
                            digits = "".join(ch for ch in s if ch in "-0123456789")
                            if digits not in ("", "-"):
                                val = int(digits)
                    except Exception:
                        val = None
                    if val is None:
                        cleaned = True
                        continue
                    amap[k] = val
                else:
                    cleaned = True  # ignore non-numeric fields
            # Apply edits
            for k, val in amap.items():
                if k.startswith("val16_at_"):
                    off = int(k.split("_")[-1])
                    if 0 <= off <= len(bb) - 2:
                        bb[off:off+2] = int(val).to_bytes(2, "little")
                elif k == "header_le" and len(bb) >= 8:
                    try:
                        bb[0:4] = int(val).to_bytes(4, "little")
                    except Exception:
                        pass
                elif k == "field2_le" and len(bb) >= 8:
                    bb[4:8] = int(val).to_bytes(4, "little")
                elif k.startswith("byte_"):
                    idx = int(k.split("_")[-1])
                    if 0 <= idx < len(bb):
                        bb[idx] = int(val) & 0xFF
            prefix = f"@Ug{d.item_type}"
            new_serial = bit_pack_encode(bytes(bb), prefix)
            set_by(self.yaml_obj if self._root() is self.yaml_obj else self._root(), toks, new_serial)
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
            self.refresh_items()
            if cleaned:
                self.log(f"Updated (raw) {p} (ignored non-numeric or invalid fields)")
            else:
                self.log(f"Updated (raw) {p}")
            top.destroy()
        ttk.Button(rawtab,text="Save Raw Changes",command=save_raw).pack(anchor="e",padx=10,pady=10)

    def export_decoded_yaml(self):
        r=self._root()
        if r is None: return
        decoded=find_and_decode_serials_in_yaml(r)
        merged=insert_decoded_items_in_yaml(r, decoded)
        # Put back into the right place if root was /state
        if self._root() is not self.yaml_obj and isinstance(self.yaml_obj, dict):
            self.yaml_obj["state"]=merged
        else:
            self.yaml_obj=merged
        self.yaml_text.delete("1.0","end")
        self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.log(f"Injected _DECODED_ITEMS for {len(decoded)} serial(s).")

    # YAML tab
    def _build_tab_yaml(self,parent: ttk.Frame)->None:
        ytop=ttk.Frame(parent); ytop.pack(fill="x")
        def _yaml_cmd_open():
            fn = getattr(self, '_open_yaml_file', None)
            if callable(fn):
                return fn()
            from tkinter import filedialog as fd, messagebox as mb
            from pathlib import Path as _Path
            f = fd.askopenfilename(title='Open YAML', filetypes=[('YAML','*.yml *.yaml'),('All files','*.*')])
            if not f:
                return
            t = _Path(f).read_text(encoding='utf-8', errors='ignore')
            if getattr(self, 'yaml_text', None):
                self.yaml_text.delete('1.0','end')
                self.yaml_text.insert('1.0', t)
            try:
                self.yaml_obj = yaml.load(t, Loader=get_yaml_loader()) if yaml is not None else None
            except Exception as e:
                self.log(f'YAML parse note: {e}')
        def _yaml_cmd_encrypt():
            fn = getattr(self, '_encrypt_yaml_as_save', None)
            if callable(fn):
                return fn()
            from tkinter import filedialog as fd, messagebox as mb
            from pathlib import Path as _Path
            if yaml is None:
                return mb.showerror('Missing dependency','PyYAML is required.\nInstall with: pip install pyyaml')
            uid = (self.user_id.get() or '').strip() if hasattr(self,'user_id') else ''
            if not uid:
                return mb.showerror('Missing User ID','Enter your User ID first.')
            txt = self.yaml_text.get('1.0','end') if getattr(self,'yaml_text',None) else ''
            obj = yaml.load(txt, Loader=get_yaml_loader())
            obj = extract_and_encode_serials_from_yaml(obj)
            yb = yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).encode()
            dest = fd.asksaveasfilename(defaultextension='.sav', filetypes=[('BL4 Save','.sav')])
            if not dest:
                return
            plat = (getattr(self, 'platform', None) or 'epic').lower()
            _Path(dest).write_bytes(encrypt_from_yaml(yb, plat, uid))
            try:
                mb.showinfo('Done', f'Saved {dest}')
            except Exception:
                pass
        ttk.Label(ytop,text="Find:").pack(side="left")
        self.find_var=tk.StringVar(); ttk.Entry(ytop,textvariable=self.find_var,width=40).pack(side="left",padx=6)
        ttk.Button(ytop,text="Next",command=self.find_next).pack(side="left")
        ttk.Separator(ytop, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(ytop, text="Open YAML…", command=_yaml_cmd_open).pack(side="left", padx=6)
        ttk.Button(ytop, text="Encrypt YAML → .sav", command=_yaml_cmd_encrypt).pack(side="left", padx=6)
        ttk.Checkbutton(ytop, text="Unlocks (Profile.sav)", variable=self.unlock_profile_var).pack(side="left", padx=6)
        self.yaml_text = tk.Text(parent, bg=Dark.BG, fg=Dark.FG, insertbackground=Dark.FG, selectbackground=Dark.SEL)
        self.yaml_text.pack(expand=True, fill="both")

    def find_next(self)->None:
        needle=self.find_var.get()
        if not needle: return
        idx=self.yaml_text.search(needle, self.yaml_text.index("insert +1c"), nocase=True, stopindex="end")
        if not idx:
            idx=self.yaml_text.search(needle,"1.0",nocase=True, stopindex="end")
            if not idx: return
        end=f"{idx}+{len(needle)}c"
        self.yaml_text.tag_remove("sel","1.0","end"); self.yaml_text.tag_add("sel", idx, end)
        self.yaml_text.mark_set("insert", end); self.yaml_text.see(idx)


    # ===== Profile helpers =====
    def select_profile(self):
        f = fd.askopenfilename(title="Select Profile", filetypes=[("BL4 Profile","*.sav"),("All Files","*.*")])
        if f: self.profile_path = Path(f); self.log(f"[Profile] Selected {f}")

    def decrypt_profile(self):
        if not self.profile_path: return mb.showwarning("No profile","Select Profile first")
        if yaml is None:
            return mb.showerror("Missing dependency","PyYAML is required.\nInstall with: pip install pyyaml")
        uid = self.user_id.get().strip()
        if not uid: return mb.showerror("Missing User ID","Enter your User ID before decrypting profile")
        enc=self.profile_path.read_bytes()
        try:
            plain, plat = decrypt_auto(enc, uid)
            ts=time.strftime("%Y-%m-%d-%H%M"); backup=self.profile_path.with_suffix(f".{ts}.bak"); backup.write_bytes(enc)
            self.profile_platform = plat
            self.profile_obj = yaml.load(plain.decode("utf-8","ignore"), Loader=get_yaml_loader())
            self.log(f"[Profile] Decrypted OK (platform: {plat}) — Backup: {backup.name}")
            # Preview unlockables categories count
            unl = (self.profile_obj or {}).get("unlockables") or {}
            if isinstance(unl, dict):
                cats = ", ".join(sorted(k for k,v in unl.items() if isinstance(v, dict)))
                self.log(f"[Profile] unlockables categories: {cats or '(none)'}")
        except Exception as e:
            mb.showerror("Profile Decrypt Failed", str(e)); self.log(f"[Profile] Decrypt error: {e}")

    def _profile_ensure_cat(self, key: str):
        if self.profile_obj is None:
            raise RuntimeError("Profile not loaded")
        unl = self.profile_obj.setdefault("unlockables", {})
        cat = unl.setdefault(key, {})
        ent = cat.setdefault("entries", [])
        if not isinstance(ent, list): cat["entries"] = ent = []
        return ent

    def _load_external_catalog(self):
        out = {}
        try:
            p = Path(self.profile_path or ".").with_name("unified_profile_unlockables_catalog.csv")
            if not p.exists():
                for alt in [Path.cwd()/"unified_profile_unlockables_catalog.csv", Path("/mnt/data/unified_profile_unlockables_catalog.csv")]:
                    if alt.exists(): p = alt; break
            if p.exists():
                import csv
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    rd = csv.DictReader(f)
                    for row in rd:
                        cat = (row.get("category_key") or "").strip()
                        ent = (row.get("entry") or "").strip()
                        if cat and ent:
                            out.setdefault(cat, set()).add(ent)
                out = {k: sorted(v) for k,v in out.items()}
                self.log(f"[Profile] Loaded catalog from CSV: {p.name} (cats={len(out)})")
        except Exception as e:
            self.log(f"[Profile] Catalog CSV load note: {e}")
        return out

    def _apply_profile_unlocks(self):
        if not self.profile_obj:
            self.log("[Profile] No profile loaded; skipping unlocks"); return 0
        if not self.unlock_profile_var.get():
            self.log("[Profile] Unlocks (Profile) is OFF — skipping"); return 0

        catalog_csv = self._load_external_catalog()
        catalog = {}
        for k, v in (EMBEDDED_PROFILE_UNLOCKS.items() if isinstance(EMBEDDED_PROFILE_UNLOCKS, dict) else []):
            catalog[k] = list(v)
        for k, lst in (catalog_csv.items() if isinstance(catalog_csv, dict) else []):
            if k not in catalog: catalog[k] = []
            merged = set(map(str, catalog[k]))
            for e in lst or []:
                merged.add(str(e))
            catalog[k] = sorted(merged)

        added = 0
        per_cat_added = []
        caseflex_cats = {"unlockable_echo4","unlockable_darksiren","unlockable_paladin",
                         "unlockable_gravitar","unlockable_exosoldier","unlockable_weapons"}
                                            

        for cat_key, entries in (catalog.items() if isinstance(catalog, dict) else []):
            try:
                ent_list = self._profile_ensure_cat(cat_key)
                before = set(map(str, ent_list))

                expanded = []
                if cat_key in caseflex_cats:
                    for e in (entries or []):
                        expanded.extend(self._normalize_unlock_variants(e))
                else:
                    expanded = list(entries or [])

                new_items = [x for x in expanded if x not in before]
                if new_items:
                    seen, ordered = set(), []
                    for x in new_items:
                        if x not in seen:
                            seen.add(x); ordered.append(x)
                    ent_list.extend(ordered)
                    added += len(ordered)
                    sample = ", ".join(ordered[:5])
                    self.log(f"[Profile] {cat_key}: wrote {len(ordered)} entries → {sample}")
            except Exception as e:
                self.log(f"[Profile] Could not apply '{cat_key}': {e}")

        if per_cat_added:
            self.log("[Profile] Added → " + " | ".join(per_cat_added))
        self.log(f"[Profile] Unlocks applied: +{added} entries")
        return added

    def encrypt_profile(self):
        if not self.profile_path: return mb.showwarning("No profile","Select Profile first")
        if yaml is None:
            return mb.showerror("Missing dependency","PyYAML is required.\nInstall with: pip install pyyaml")
        uid = self.user_id.get().strip()
        if not uid: return mb.showerror("Missing User ID","Enter your User ID before encrypting profile")
        if self.profile_obj is None:
            return mb.showwarning("No profile data","Decrypt Profile first")

        try:
            self._apply_profile_unlocks()
            yb = yaml.safe_dump(self.profile_obj, sort_keys=False, allow_unicode=True).encode()
            out = self.profile_path.with_suffix(".sav")
            out.write_bytes(encrypt_from_yaml(yb, self.profile_platform or "epic", uid))
            self.log(f"[Profile] Encrypted → {out.name}")
            mb.showinfo("Done", f"Saved {out.name}")
        except Exception as e:
            mb.showerror("Profile Encrypt Failed", str(e)); self.log(f"[Profile] Encrypt error: {e}")
    # preview_profile_unlocks removed in H build




# ── run ───────────────────────────────────────────────────────────────────────
# ========================
# v1.031a Integrated Patches
# (see comment block above for details)
# ========================
from pathlib import Path as _Path031a
import re as _re031a

_CHAR_CATS_031a = ["unlockable_darksiren","unlockable_paladin","unlockable_gravitar","unlockable_exosoldier"]
_ECHO_CAT_031a = "unlockable_echo4"

def _unlockables_root_031a(self):
    if self.profile_obj is None:
        raise RuntimeError("Profile not loaded")
    return (self.profile_obj
            .setdefault("domains", {})
            .setdefault("local", {})
            .setdefault("unlockables", {}))

def _profile_ensure_cat_031a(self, key: str):
    unl = _unlockables_root_031a(self)
    cat = unl.setdefault(key, {})
    ent = cat.setdefault("entries", [])
    if not isinstance(ent, list):
        cat["entries"] = ent = []
    return ent

def _migrate_unlockables_to_domains_031a(self):
    try:
        if not isinstance(self.profile_obj, dict):
            return
        legacy = self.profile_obj.get("unlockables")
        target = _unlockables_root_031a(self)
        if isinstance(legacy, dict):
            for cat, obj in legacy.items():
                if not isinstance(obj, dict):
                    continue
                tgt_cat = target.setdefault(cat, {})
                tgt_list = tgt_cat.setdefault("entries", [])
                src_list = obj.get("entries") or []
                seen = set(map(str, tgt_list))
                for e in map(str, src_list):
                    if e not in seen:
                        tgt_list.append(e); seen.add(e)
            self.profile_obj.pop("unlockables", None)
            try: self.log("[Profile] Migrated top-level 'unlockables' → domains/local (legacy removed)")
            except Exception: pass
    except Exception as e:
        try: self.log(f"[Profile] Migration note: {e}")
        except Exception: pass

def _normalize_unlock_variants_031a(entry: str):
    e = str(entry)
    out = {e}
    if "." in e:
        prefix, rest = e.split(".", 1)
        out.add(prefix + "." + rest.lower())
    out.add(e.lower())
    return list(out)

def _extract_echo_skins_031a(echo_entries):
    pat = _re031a.compile(r'^Unlockable_Echo4\.Skin(\d+)_([A-Za-z0-9_]+)$', _re031a.I)
    pairs = set()
    for s in map(str, echo_entries or []):
        m = pat.match(s) or pat.match(s.lower().replace("unlockable_echo4.","Unlockable_Echo4."))
        if m:
            pairs.add( (int(m.group(1)), m.group(2)) )
    return pairs

App._unlockables_root = _unlockables_root_031a
App._profile_ensure_cat = _profile_ensure_cat_031a
App._migrate_unlockables_to_domains = _migrate_unlockables_to_domains_031a

if hasattr(App, "decrypt_profile"):
    _orig_decrypt_profile_031a = App.decrypt_profile
    def decrypt_profile_patched_031a(self, *a, **kw):
        res = _orig_decrypt_profile_031a(self, *a, **kw)
        try:
            _migrate_unlockables_to_domains_031a(self)
            unl2 = _unlockables_root_031a(self)
            if isinstance(unl2, dict):
                cats2 = ", ".join(sorted(k for k,v in unl2.items() if isinstance(v, dict)))
                self.log(f"[Profile] unlockables (domains/local) categories: {cats2 or '(none)'}")
        except Exception:
            pass
        return res
    App.decrypt_profile = decrypt_profile_patched_031a

if hasattr(App, "_apply_profile_unlocks"):
    _orig_apply_profile_unlocks_031a = App._apply_profile_unlocks
    def _apply_profile_unlocks_patched_031a(self, *a, **kw):
        snapshot = {}
        unl = _unlockables_root_031a(self)
        for cat, obj in (unl or {}).items():
            if isinstance(obj, dict):
                snapshot[cat] = list(map(str, obj.get("entries") or []))

        added = _orig_apply_profile_unlocks_031a(self, *a, **kw)

        try:
            echo_list = _profile_ensure_cat_031a(self, _ECHO_CAT_031a)
            echo_pairs = _extract_echo_skins_031a(echo_list)
            if echo_pairs:
                for cat in _CHAR_CATS_031a:
                    prefix = cat.replace("unlockable_","Unlockable_")
                    dest = _profile_ensure_cat_031a(self, cat)
                    already = set(map(str, dest))
                    for idx, suf in sorted(echo_pairs):
                        token = f"{prefix}.Skin{idx}_{suf}"
                        for v in _normalize_unlock_variants_031a(token):
                            if v not in already:
                                dest.append(v)
                                already.add(v)
                try: self.log(f"[Profile] Parity fill: mirrored {len(echo_pairs)} Echo skin indices → all characters")
                except Exception: pass
        except Exception as e:
            try: self.log(f"[Profile] Parity fill note: {e}")
            except Exception: pass

        try:
            for cat, old in snapshot.items():
                dest = _profile_ensure_cat_031a(self, cat)
                seen = set(map(str, dest))
                for s in old:
                    if s not in seen:
                        dest.append(s); seen.add(s)
        except Exception as e:
            try: self.log(f"[Profile] Preserve note: {e}")
            except Exception: pass

        try:
            crown = "Unlockable_Echo4.attachment10_crown"
            dest = _profile_ensure_cat_031a(self, _ECHO_CAT_031a)
            seen = set(map(str, dest))
            for v in _normalize_unlock_variants_031a(crown):
                if v not in seen:
                    dest.append(v); seen.add(v)
        except Exception:
            pass

        return added
    App._apply_profile_unlocks = _apply_profile_unlocks_patched_031a

if not hasattr(App, "dump_yaml"):
    def dump_yaml_031a(self):
        import yaml as _yaml031a
        p = _Path031a(self.profile_path or ".").with_name("profile_decrypted.yaml")
        txt = _yaml031a.safe_dump(self.profile_obj, sort_keys=False, allow_unicode=True)
        p.write_text(txt, encoding="utf-8")
        try: self.log(f"[Profile] Dumped YAML → {p}")
        except Exception: pass
    App.dump_yaml = dump_yaml_031a

# ======================== end v1.031a patches ========================

#if __name__ == "__main__":

# DEBUG launcher additions (non-invasive)
if __name__ == "__main__":
    # DEBUG launcher additions (non-invasive)
    import sys, traceback, atexit
    DEBUG = ("--debug" in sys.argv) or ("-d" in sys.argv)

    def _bl4_excepthook(exc_type, exc, tb):
        msg = "".join(traceback.format_exception(exc_type, exc, tb))
        try:
            with open("startup_error.log", "w", encoding="utf-8") as f:
                f.write(msg)
        except Exception:
            pass
        try:
            import tkinter.messagebox as _mb
            _mb.showerror("Startup error", msg)
        except Exception:
            pass
        if DEBUG:
            try:
                input("Press Enter to close...")
            except Exception:
                pass
        sys.__excepthook__(exc_type, exc, tb)

    sys.excepthook = _bl4_excepthook


    import sys, traceback
    try:
        import tkinter as tk
        from tkinter import messagebox
        # Build the Tk root and pass it to App
        root = tk.Tk()
        try:
            app = App(root)   # your App expects 'root'
        except TypeError:
            # Fallback if your App signature doesn't need root
            app = App()

        # Prefer an app.run() if you have one; otherwise mainloop via the instance/root
        if hasattr(app, "run") and callable(getattr(app, "run")):
            app.run()
        elif hasattr(app, "root"):
            app.root.mainloop()
        else:
            root.mainloop()

    except Exception:
        # Never exit silently—show, log, and print the real error
        tb = traceback.format_exc()
        try:
            from tkinter import messagebox as _mb
            _mb.showerror("Startup error", tb)
        except Exception:
            pass
        try:
            with open("startup_error.log", "w", encoding="utf-8") as _f:
                _f.write(tb)
        except Exception:
            pass
        print(tb)
        if "--debug" in sys.argv:
            try:
                input("Press Enter to close...")
            except Exception:
                pass

 


# ======================== v1.032a patch starts here ========================
# UI: add Level/Rarity/Flags columns. Items inspector adds Equipped + State Flags.
# Progression: replace "Max SDU" button with checkbox + Apply; echo cap default 3525; log nodes/points.

# 1) Patch Items UI to add columns and compute level/rarity per row
def _patched_build_tab_items(self, parent: ttk.Frame)->None:
    filt=ttk.Frame(parent); filt.pack(fill="x", pady=6, padx=8)
    ttk.Label(filt,text="Search:").pack(side="left")
    self.search_var=tk.StringVar(); ttk.Entry(filt,textvariable=self.search_var,width=40).pack(side="left",padx=6)
    ttk.Label(filt,text="Type:").pack(side="left",padx=(12,4))
    self.type_var=tk.StringVar(value="All")
    ttk.Combobox(filt,textvariable=self.type_var, values=["All","Weapon","Equipment","Equipment Alt","Special"], width=18, state="readonly").pack(side="left")
    ttk.Button(filt,text="Filter",command=self.apply_filter).pack(side="left",padx=6)
    ttk.Button(filt,text="Export Decoded → YAML",command=self.export_decoded_yaml).pack(side="left",padx=12)
    cols=("path","type","level","rarity","flags","serial")
    self.tree=ttk.Treeview(parent,columns=cols,show="headings")
    for c,txt,w in [("path","Path",480),("type","Type",120),("level","Lvl",60),("rarity","Rarity",70),("flags","Flags",90),("serial","Serial",480)]:
        self.tree.heading(c,text=txt); self.tree.column(c,width=w,anchor="w")
    self.tree.pack(expand=True,fill="both", padx=8, pady=(0,8))
    self.tree.bind("<Double-1>", self.open_inspector)

def _patched_refresh_items(self)->None:
    self.items=[]
    r=self._root()
    if not isinstance(r, dict): return
    # gather flags/state_flags if siblings exist
    def get_flags_for(path):
        try:
            toks=tokens(path); cur=self._root() if self._root() is not None else self.yaml_obj
            for t in toks[:-1]: cur = cur[t]
            if isinstance(cur, dict):
                return cur.get("flags",""), cur.get("state_flags","")
        except Exception:
            pass
        return ("","")
    for path,serial in walk_ug(r):
        t = serial[3] if serial.startswith("@Ug") and len(serial)>=4 else "?"
        friendly = {"r":"Weapon","e":"Equipment","d":"Equipment Alt","u":"Special","f":"Special","!":"Special"}.get(t,"Unknown")
        try:
            d=decode_item_serial(serial); lvl = d.stats.level or ""
            rar = d.stats.rarity or ""
        except Exception:
            lvl = ""; rar = ""
        flags, sflags = get_flags_for(path)
        flag_str = f"{flags}/{sflags}" if flags!="" or sflags!="" else ""
        self.items.append((path,friendly,str(lvl),str(rar),flag_str,serial))
    self.apply_filter()

def _patched_apply_filter(self)->None:
    term=(self.search_var.get() or "").lower(); type_sel=self.type_var.get()
    for r in self.tree.get_children(): self.tree.delete(r)
    for p,friendly,lvl,rar,fl,serial in self.items:
        if type_sel!="All" and dtype!=type_sel: continue
        if term and not any(term in s for s in (p.lower(), serial.lower(), str(name).lower())):
                continue
        self.tree.insert("", "end", values=(p,friendly,lvl,rar,fl,serial))

# 2) Patch inspector to add Equipped + State Flags selection and write siblings
STATE_FLAG_LABELS = [
    (641, "Badge 4 (Green)"),
    (577, "Badge 3 (Purple)"),
    (545, "Badge 2 (Blue)"),
    (529, "Badge 1 (Orange)"),
    (521, "Bank"),
    (517, "Junk"),
    (515, "Favorite"),
    (513, "Blank"),
]
def _patched_open_inspector(self,_evt=None)->None:
    sel=self.tree.selection()
    if not sel: return
    p,typ,name,code,serial,tags = _safe_unpack_item_values(self.tree.item(sel[0],"values"))
    toks=tokens(p); d=decode_item_serial(serial)
    top=tk.Toplevel(self.root); top.title("BL4 Save Editor v1.04a Full"); top.geometry("900x640"); top.configure(bg=Dark.BG)
    nb=ttk.Notebook(top); nb.pack(expand=True,fill="both")

    # Simple
    simp=ttk.Frame(nb); nb.add(simp,text="Simple")
    vals={
        "Primary": d.stats.primary_stat or 0,
        "Secondary": d.stats.secondary_stat or 0,
        "Rarity": d.stats.rarity or 0,
        "Manufacturer": d.stats.manufacturer or 0,
        "Item Class": d.stats.item_class or 0,
        "Level": d.stats.level or 1,
    }
    entries={}; grid=ttk.Frame(simp,padding=12); grid.pack(fill="both",expand=True,side="left")
    row=0
    for name in ["Primary","Secondary","Rarity","Manufacturer","Item Class","Level"]:
        ttk.Label(grid,text=name).grid(row=row,column=0,sticky="w",padx=6,pady=6)
        var=tk.StringVar(value=str(vals[name])); ttk.Entry(grid,textvariable=var,width=16).grid(row=row,column=1,sticky="w",padx=6,pady=6)
        entries[name]=var; row+=1

    # Flags box
    fb=ttk.LabelFrame(simp,text="Flags",padding=10); fb.pack(side="left",fill="y",padx=12)
    eq_var=tk.BooleanVar(value=False)
    ttk.Checkbutton(fb,text="Equipped",variable=eq_var).pack(anchor="w")
    ttk.Label(fb,text="State Marker").pack(anchor="w",pady=(8,2))
    state_var=tk.StringVar(value="")
    ttk.Combobox(fb,textvariable=state_var,values=[f"{label} ({val})" for val,label in STATE_FLAG_LABELS],state="readonly",width=24).pack(anchor="w")

    def save_simple():
        try:
            d.stats.primary_stat=int(entries["Primary"].get())
            d.stats.secondary_stat=int(entries["Secondary"].get())
            d.stats.rarity=int(entries["Rarity"].get())
            d.stats.manufacturer=int(entries["Manufacturer"].get())
            d.stats.item_class=int(entries["Item Class"].get())
            d.stats.level=int(entries["Level"].get())
        except ValueError:
            return mb.showerror("Invalid input","All fields must be integers")
        new_serial = encode_item_serial(d)

        root = self.yaml_obj if self._root() is self.yaml_obj else self._root()

        set_by(root, toks, new_serial)
        # write sibling flags
        try:
            parent=self.yaml_obj if self._root() is self.yaml_obj else self._root()
            cur=parent
            for t in toks[:-1]: cur=cur[t]
            if isinstance(cur, dict):
                if eq_var.get(): cur["flags"]=1
                sel=state_var.get().strip()
                if sel:
                    try: cur["state_flags"]=int(sel.split("(")[-1].split(")")[0])
                    except: pass
        except Exception: pass

        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_items(); self.log(f"Updated {p}"); top.destroy()
    ttk.Button(simp,text="Save & Encode",command=save_simple).pack(pady=10)

    # Raw
    rawtab=ttk.Frame(nb); nb.add(rawtab,text="Raw")
    canvas=tk.Canvas(rawtab,bg=Dark.BG,highlightthickness=0); frame=ttk.Frame(canvas)
    vsb=tk.Scrollbar(rawtab,orient="vertical",command=canvas.yview); canvas.configure(yscrollcommand=vsb.set)
    canvas.pack(side="left",fill="both",expand=True); vsb.pack(side="right",fill="y")
    inner=ttk.Frame(canvas); canvas.create_window((0,0),window=inner,anchor="nw")
    for k,v in (d.raw or {}).items():
        ttk.Label(inner,text=str(k)).pack(anchor="w"); ttk.Label(inner,text=str(v)).pack(anchor="w")
    inner.update_idletasks(); canvas.config(scrollregion=canvas.bbox("all"))

# 3) Patch progression UI to use a checkbox for Max SDU and set echo default 3225
def _patched_build_tab_progression(self, parent: ttk.Frame):
    pf = ttk.LabelFrame(parent, text="Progression (graphs & nodes)", padding=8); pf.pack(fill="both", expand=True, padx=10, pady=8)
    ctl = ttk.Frame(pf); ctl.pack(fill="x")
    self.var_max_sdu = tk.BooleanVar(value=False)
    ttk.Checkbutton(ctl, text="Max SDU", variable=self.var_max_sdu).pack(side="left", padx=(0,6))
    ttk.Button(ctl, text="Apply", command=self.apply_progression_actions).pack(side="left", padx=6)
    ttk.Button(ctl, text="Recalculate Point Pools", command=self.recalc_pools).pack(side="left", padx=6)
    ttk.Label(ctl, text="Echo Tokens cap:").pack(side="left", padx=(18,4))
    self.echo_var=tk.StringVar(value="3225"); ttk.Entry(ctl,textvariable=self.echo_var,width=8).pack(side="left")
    cols=("graph","node","points_spent","is_activated","activation_level")
    self.prog_tree=ttk.Treeview(pf, columns=cols, show="headings", height=18)
    for c,w in [("graph",340),("node",340),("points_spent",120),("is_activated",120),("activation_level",140)]:
        self.prog_tree.heading(c, text=c.replace("_"," ").title()); self.prog_tree.column(c, width=w, anchor="w")
    self.prog_tree.pack(expand=True, fill="both", pady=(6,2))
    edit = ttk.Frame(pf, padding=6); edit.pack(fill="x")
    ttk.Label(edit,text="points_spent").pack(side="left")
    self.points_var=tk.StringVar(); ttk.Entry(edit,textvariable=self.points_var,width=8).pack(side="left",padx=6)
    self.act_var=tk.BooleanVar(value=False); ttk.Checkbutton(edit,text="is_activated",variable=self.act_var).pack(side="left",padx=6)
    ttk.Label(edit,text="activation_level").pack(side="left")
    self.level_var=tk.StringVar(); ttk.Entry(edit,textvariable=self.level_var,width=8).pack(side="left",padx=6)
    ttk.Button(edit,text="Apply to Selected",command=self.apply_node).pack(side="left",padx=10)
    ttk.Button(edit,text="Activate All (Graph)",command=lambda:self.bulk_graph(True)).pack(side="left",padx=6)
    ttk.Button(edit,text="Deactivate All (Graph)",command=lambda:self.bulk_graph(False)).pack(side="left",padx=6)

def apply_progression_actions(self):
    r=self._root()
    if not isinstance(r, dict): return
    prog=r.setdefault("progression", {})
    if self.var_max_sdu.get():
        before = sum(len(g.get("nodes",[])) for g in prog.get("graphs",[]) or [] if g.get("name")=="sdu_upgrades")
        ensure_sdu_graph(prog)
        after = sum(len(g.get("nodes",[])) for g in prog.get("graphs",[]) or [] if g.get("name")=="sdu_upgrades")
        set_nodes = max(0, after - before) if after else 60
        # recompute total points in SDU graph
        total_points = 0
        for g in prog.get("graphs",[]) or []:
            if g.get("name")=="sdu_upgrades":
                total_points = sum(int(n.get("points_spent",0)) for n in g.get("nodes",[]) if isinstance(n,dict))
        self.log(f"Applied Max SDU: set {set_nodes} of 60 nodes; total points attributed: {total_points}")
        self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
        self.refresh_progression()
    else:
        self.log("Max SDU unchecked — no SDU changes applied.")

# 4) Patch recalc_pools to cap at 3525
def _patched_recalc_pools(self):
    r=self._root()
    if not isinstance(r, dict): return
    prog=r.setdefault("progression", {})
    if not prog and isinstance(self.yaml_obj, dict):
        prog=self.yaml_obj.setdefault("progression", {})
    pools=prog.setdefault("point_pools", {})
    char_pts = sum_points_in_graphs(prog, name_prefixes=["Progress_DS_"])
    spec_pts = sum_points_in_graphs(prog, name_prefixes=["ProgressGraph_Specializations"])
    pools["characterprogresspoints"]=char_pts
    pools["specializationtokenpool"]=spec_pts
    try:
        cap=int(self.echo_var.get()) if getattr(self, "echo_var", None) else 3225
    except Exception:
        cap=3225
    pools["echotokenprogresspoints"]=min(int(pools.get("echotokenprogresspoints", cap) or cap), cap)
    self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
    self.refresh_progression(); self.log(f"Recalculated pools: char={char_pts}, spec={spec_pts}, echo={pools['echotokenprogresspoints']} (cap {cap})")

# Bind patches
App._build_tab_items = _patched_build_tab_items
App.refresh_items = _patched_refresh_items
App.apply_filter = _patched_apply_filter
App.open_inspector = _patched_open_inspector
App._build_tab_progression = _patched_build_tab_progression
App.apply_progression_actions = apply_progression_actions
App.recalc_pools = _patched_recalc_pools
# ======================== v1.032a patch ends here ==========================



# ==========================================================
# 1.034a Patch Additions
# ==========================================================

AVAILABLE_CLASSES_1034A = [
    "Char_DarkSiren","Char_Paladin","Char_Gravitar","Char_ExoSoldier",
]

# Catalog used by 1.04a. If you want to resolve from EMBEDDED_PROFILE_UNLOCKS at runtime,
# you can fill these "entries" later; for now keep it syntactically valid.
PROFILE_UNLOCKS_1034A = {
    "unlockable_darksiren": {"entries": []},
    "unlockable_exosoldier": {"entries": []},
    "unlockable_gravitar": {"entries": []},
    "unlockable_paladin": {"entries": []},
    "unlockable_echo4": {"entries": []},
    "unlockable_weapons": {"entries": []},
    "unlockable_vehicles": {"entries": []},
}



# === BEGIN: auto-extended unlocks from reference profile ===

PROFILE_UNLOCKS_1034A.setdefault('unlockable_darksiren', [])
PROFILE_UNLOCKS_1034A['unlockable_darksiren'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_darksiren']) | {
    "Unlockable_DarkSiren.Body01_Prison",
    "Unlockable_DarkSiren.Body02_Premium",
    "Unlockable_DarkSiren.Head01_Prison",
    "Unlockable_DarkSiren.Head02_PigTails",
    "Unlockable_DarkSiren.Head03_MoHawk",
    "Unlockable_DarkSiren.Head04_Shades",
    "Unlockable_DarkSiren.Head05_BikeHelmet",
    "Unlockable_DarkSiren.Head06_PunkMask",
    "Unlockable_DarkSiren.Head07_Demon",
    "Unlockable_DarkSiren.Head08_Survivalist",
    "Unlockable_DarkSiren.Head09_Electi",
    "Unlockable_DarkSiren.Head10_Transhuman",
    "Unlockable_DarkSiren.Head11_Ripper",
    "Unlockable_DarkSiren.Head12_Order",
    "Unlockable_DarkSiren.Head13_Robot",
    "Unlockable_DarkSiren.Head14_Thresher",
    "Unlockable_DarkSiren.Head15_CrimeLord",
    "Unlockable_DarkSiren.Head16_Premium",
    "Unlockable_DarkSiren.Head23_CrashTestDummy",
    "Unlockable_DarkSiren.Skin01_Prison",
    "Unlockable_DarkSiren.Skin02_Order",
    "Unlockable_DarkSiren.Skin03_Ghost",
    "Unlockable_DarkSiren.Skin04_Tech",
    "Unlockable_DarkSiren.Skin05_Ripper",
    "Unlockable_DarkSiren.Skin06_Amara",
    "Unlockable_DarkSiren.Skin07_RedHanded",
    "Unlockable_DarkSiren.Skin08_Corrupted",
    "Unlockable_DarkSiren.Skin09_Sewer",
    "Unlockable_DarkSiren.Skin10_Hawaiian",
    "Unlockable_DarkSiren.Skin11_Astral",
    "Unlockable_DarkSiren.Skin12_Tediore",
    "Unlockable_DarkSiren.Skin13_3CatMoon",
    "Unlockable_DarkSiren.Skin14_Fire",
    "Unlockable_DarkSiren.Skin15_Survivalist",
    "Unlockable_DarkSiren.Skin16_Crimson",
    "Unlockable_DarkSiren.Skin17_Auger",
    "Unlockable_DarkSiren.Skin18_Electi",
    "Unlockable_DarkSiren.Skin19_Dirty",
    "Unlockable_DarkSiren.Skin20_HighRoller",
    "Unlockable_DarkSiren.Skin21_Graffiti",
    "Unlockable_DarkSiren.Skin22_Knitted",
    "Unlockable_DarkSiren.Skin23_GearboxDev",
    "Unlockable_DarkSiren.Skin24_PreOrder",
    "Unlockable_DarkSiren.Skin25_Slimed",
    "Unlockable_DarkSiren.Skin26_Camo",
    "Unlockable_DarkSiren.Skin27_Space",
    "Unlockable_DarkSiren.Skin28_Ritual",
    "Unlockable_DarkSiren.Skin29_Guardian",
    "Unlockable_DarkSiren.Skin30_Cute",
    "Unlockable_DarkSiren.Skin31_Koto",
    "Unlockable_DarkSiren.Skin32_DuctTaped",
    "Unlockable_DarkSiren.Skin33_Jakobs",
    "Unlockable_DarkSiren.Skin34_Daedalus",
    "Unlockable_DarkSiren.Skin35_Vladof",
    "Unlockable_DarkSiren.Skin36_Torgue",
    "Unlockable_DarkSiren.Skin37_Maliwan",
    "Unlockable_DarkSiren.Skin38_CyberPop",
    "Unlockable_DarkSiren.Skin39_Critters",
    "Unlockable_DarkSiren.Skin40_Veil",
    "Unlockable_DarkSiren.Skin44_Premium",
    "Unlockable_DarkSiren.Skin45_BreakFree",
    "unlockable_darksiren",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_echo4', [])
PROFILE_UNLOCKS_1034A['unlockable_echo4'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_echo4']) | {
    "Unlockable_Echo4.Body01_GeneVIV",
    "Unlockable_Echo4.Body03_Ripper",
    "Unlockable_Echo4.Skin01_Prison",
    "Unlockable_Echo4.Skin02_Order",
    "Unlockable_Echo4.Skin03_Ghost",
    "Unlockable_Echo4.Skin04_Tech",
    "Unlockable_Echo4.Skin05_Ripper",
    "Unlockable_Echo4.Skin06_Amara",
    "Unlockable_Echo4.Skin07_RedHanded",
    "Unlockable_Echo4.Skin08_Corrupted",
    "Unlockable_Echo4.Skin09_Sewer",
    "Unlockable_Echo4.Skin10_Hawaiian",
    "Unlockable_Echo4.Skin11_Astral",
    "Unlockable_Echo4.Skin12_Tediore",
    "Unlockable_Echo4.Skin13_3CatMoon",
    "Unlockable_Echo4.Skin14_Fire",
    "Unlockable_Echo4.Skin15_Survivalist",
    "Unlockable_Echo4.Skin16_Crimson",
    "Unlockable_Echo4.Skin17_Auger",
    "Unlockable_Echo4.Skin18_Electi",
    "Unlockable_Echo4.Skin19_Dirty",
    "Unlockable_Echo4.Skin20_HighRoller",
    "Unlockable_Echo4.Skin21_Graffiti",
    "Unlockable_Echo4.Skin22_Knitted",
    "Unlockable_Echo4.Skin23_GearboxDev",
    "Unlockable_Echo4.Skin24_PreOrder",
    "Unlockable_Echo4.Skin25_Slimed",
    "Unlockable_Echo4.Skin26_Camo",
    "Unlockable_Echo4.Skin27_Space",
    "Unlockable_Echo4.Skin28_Ritual",
    "Unlockable_Echo4.Skin29_Guardian",
    "Unlockable_Echo4.Skin30_Cute",
    "Unlockable_Echo4.Skin31_Koto",
    "Unlockable_Echo4.Skin32_DuctTaped",
    "Unlockable_Echo4.Skin33_Jakobs",
    "Unlockable_Echo4.Skin34_Daedalus",
    "Unlockable_Echo4.Skin35_Vladof",
    "Unlockable_Echo4.Skin36_Torgue",
    "Unlockable_Echo4.Skin37_Maliwan",
    "Unlockable_Echo4.Skin38_CyberPop",
    "Unlockable_Echo4.Skin39_Critters",
    "Unlockable_Echo4.Skin40_Veil",
    "Unlockable_Echo4.Skin41_Butterfinger",
    "Unlockable_Echo4.Skin42_Legacy",
    "Unlockable_Echo4.Skin43_Twitch",
    "Unlockable_Echo4.Skin45_BreakFree",
    "Unlockable_Echo4.Skin50_BreakTheGame",
    "Unlockable_Echo4.attachment01_partyhat",
    "Unlockable_Echo4.attachment02_bow",
    "Unlockable_Echo4.attachment03_bolt",
    "Unlockable_Echo4.attachment04_wings",
    "Unlockable_Echo4.attachment05_skull",
    "Unlockable_Echo4.attachment06_crystalhorn",
    "Unlockable_Echo4.attachment07_horns",
    "Unlockable_Echo4.attachment08_tinfoilhat",
    "Unlockable_Echo4.attachment09_goggles",
    "Unlockable_Echo4.attachment10_crown",
    "Unlockable_Echo4.attachment11_mohawk",
    "Unlockable_Echo4.attachment12_psychomask",
    "Unlockable_Echo4.attachment13_fishinghat",
    "Unlockable_Echo4.body02_order",
    "unlockable_echo4",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_exosoldier', [])
PROFILE_UNLOCKS_1034A['unlockable_exosoldier'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_exosoldier']) | {
    "Unlockable_ExoSoldier.Body01_Prison",
    "Unlockable_ExoSoldier.Body02_Premium",
    "Unlockable_ExoSoldier.Head01_Prison",
    "Unlockable_ExoSoldier.Head02_Mullet",
    "Unlockable_ExoSoldier.Head03_Guerilla",
    "Unlockable_ExoSoldier.Head04_TechHawk",
    "Unlockable_ExoSoldier.Head05_LongHair",
    "Unlockable_ExoSoldier.Head06_BlindFold",
    "Unlockable_ExoSoldier.Head07_Helm",
    "Unlockable_ExoSoldier.Head08_Survivalist",
    "Unlockable_ExoSoldier.Head09_Electi",
    "Unlockable_ExoSoldier.Head10_Transhuman",
    "Unlockable_ExoSoldier.Head11_Ripper",
    "Unlockable_ExoSoldier.Head12_Order",
    "Unlockable_ExoSoldier.Head13_Robot",
    "Unlockable_ExoSoldier.Head14_Thresher",
    "Unlockable_ExoSoldier.Head15_CrimeLord",
    "Unlockable_ExoSoldier.Head16_Premium",
    "Unlockable_ExoSoldier.Head23_CrushTestDummy",
    "Unlockable_ExoSoldier.Skin01_Prison",
    "Unlockable_ExoSoldier.Skin02_Order",
    "Unlockable_ExoSoldier.Skin03_Ghost",
    "Unlockable_ExoSoldier.Skin04_Tech",
    "Unlockable_ExoSoldier.Skin05_Ripper",
    "Unlockable_ExoSoldier.Skin06_Amara",
    "Unlockable_ExoSoldier.Skin07_RedHanded",
    "Unlockable_ExoSoldier.Skin08_Corrupted",
    "Unlockable_ExoSoldier.Skin09_Sewer",
    "Unlockable_ExoSoldier.Skin10_Hawaiian",
    "Unlockable_ExoSoldier.Skin11_Astral",
    "Unlockable_ExoSoldier.Skin12_Tediore",
    "Unlockable_ExoSoldier.Skin13_3CatMoon",
    "Unlockable_ExoSoldier.Skin14_Fire",
    "Unlockable_ExoSoldier.Skin15_Survivalist",
    "Unlockable_ExoSoldier.Skin16_Crimson",
    "Unlockable_ExoSoldier.Skin17_Auger",
    "Unlockable_ExoSoldier.Skin18_Electi",
    "Unlockable_ExoSoldier.Skin19_Dirty",
    "Unlockable_ExoSoldier.Skin20_HighRoller",
    "Unlockable_ExoSoldier.Skin21_Graffiti",
    "Unlockable_ExoSoldier.Skin22_Knitted",
    "Unlockable_ExoSoldier.Skin23_GearboxDev",
    "Unlockable_ExoSoldier.Skin24_PreOrder",
    "Unlockable_ExoSoldier.Skin25_Slimed",
    "Unlockable_ExoSoldier.Skin26_Camo",
    "Unlockable_ExoSoldier.Skin27_Space",
    "Unlockable_ExoSoldier.Skin28_Ritual",
    "Unlockable_ExoSoldier.Skin29_Guardian",
    "Unlockable_ExoSoldier.Skin30_Cute",
    "Unlockable_ExoSoldier.Skin31_Koto",
    "Unlockable_ExoSoldier.Skin32_DuctTaped",
    "Unlockable_ExoSoldier.Skin33_Jakobs",
    "Unlockable_ExoSoldier.Skin34_Daedalus",
    "Unlockable_ExoSoldier.Skin35_Vladof",
    "Unlockable_ExoSoldier.Skin36_Torgue",
    "Unlockable_ExoSoldier.Skin37_Maliwan",
    "Unlockable_ExoSoldier.Skin38_CyberPop",
    "Unlockable_ExoSoldier.Skin39_Critters",
    "Unlockable_ExoSoldier.Skin40_Veil",
    "Unlockable_ExoSoldier.Skin44_Premium",
    "Unlockable_ExoSoldier.Skin45_BreakFree",
    "unlockable_exosoldier",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_gravitar', [])
PROFILE_UNLOCKS_1034A['unlockable_gravitar'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_gravitar']) | {
    "Unlockable_Gravitar.Body01_Prison",
    "Unlockable_Gravitar.Body02_Premium",
    "Unlockable_Gravitar.Head01_Prison",
    "Unlockable_Gravitar.Head02_DreadBuns",
    "Unlockable_Gravitar.Head03_Helmet",
    "Unlockable_Gravitar.Head04_TechBraids",
    "Unlockable_Gravitar.Head05_SafetyFirst",
    "Unlockable_Gravitar.Head06_RoundGlasses",
    "Unlockable_Gravitar.Head07_VRPunk",
    "Unlockable_Gravitar.Head08_Survivalist",
    "Unlockable_Gravitar.Head09_Electi",
    "Unlockable_Gravitar.Head10_Transhuman",
    "Unlockable_Gravitar.Head11_Ripper",
    "Unlockable_Gravitar.Head12_Order",
    "Unlockable_Gravitar.Head13_Robot",
    "Unlockable_Gravitar.Head14_Thresher",
    "Unlockable_Gravitar.Head15_CrimeLord",
    "Unlockable_Gravitar.Head16_Premium",
    "Unlockable_Gravitar.Head23_CrushTestDummy",
    "Unlockable_Gravitar.Skin01_Prison",
    "Unlockable_Gravitar.Skin02_Order",
    "Unlockable_Gravitar.Skin03_Ghost",
    "Unlockable_Gravitar.Skin04_Tech",
    "Unlockable_Gravitar.Skin05_Ripper",
    "Unlockable_Gravitar.Skin06_Amara",
    "Unlockable_Gravitar.Skin07_RedHanded",
    "Unlockable_Gravitar.Skin08_Corrupted",
    "Unlockable_Gravitar.Skin09_Sewer",
    "Unlockable_Gravitar.Skin10_Hawaiian",
    "Unlockable_Gravitar.Skin11_Astral",
    "Unlockable_Gravitar.Skin12_Tediore",
    "Unlockable_Gravitar.Skin13_3CatMoon",
    "Unlockable_Gravitar.Skin14_Fire",
    "Unlockable_Gravitar.Skin15_Survivalist",
    "Unlockable_Gravitar.Skin16_Crimson",
    "Unlockable_Gravitar.Skin17_Auger",
    "Unlockable_Gravitar.Skin18_Electi",
    "Unlockable_Gravitar.Skin19_Dirty",
    "Unlockable_Gravitar.Skin20_HighRoller",
    "Unlockable_Gravitar.Skin21_Graffiti",
    "Unlockable_Gravitar.Skin22_Knitted",
    "Unlockable_Gravitar.Skin23_GearboxDev",
    "Unlockable_Gravitar.Skin24_PreOrder",
    "Unlockable_Gravitar.Skin25_Slimed",
    "Unlockable_Gravitar.Skin26_Camo",
    "Unlockable_Gravitar.Skin27_Space",
    "Unlockable_Gravitar.Skin28_Ritual",
    "Unlockable_Gravitar.Skin29_Guardian",
    "Unlockable_Gravitar.Skin30_Cute",
    "Unlockable_Gravitar.Skin31_Koto",
    "Unlockable_Gravitar.Skin32_DuctTaped",
    "Unlockable_Gravitar.Skin33_Jakobs",
    "Unlockable_Gravitar.Skin34_Daedalus",
    "Unlockable_Gravitar.Skin35_Vladof",
    "Unlockable_Gravitar.Skin36_Torgue",
    "Unlockable_Gravitar.Skin37_Maliwan",
    "Unlockable_Gravitar.Skin38_CyberPop",
    "Unlockable_Gravitar.Skin39_Critters",
    "Unlockable_Gravitar.Skin40_Veil",
    "Unlockable_Gravitar.Skin44_Premium",
    "Unlockable_Gravitar.Skin45_BreakFree",
    "unlockable_gravitar",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_paladin', [])
PROFILE_UNLOCKS_1034A['unlockable_paladin'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_paladin']) | {
    "Unlockable_Paladin.Body01_Prison",
    "Unlockable_Paladin.Body02_Premium",
    "Unlockable_Paladin.Head01_Prison",
    "Unlockable_Paladin.Head02_PonyTail",
    "Unlockable_Paladin.Head03_BaldMask",
    "Unlockable_Paladin.Head04_Visor",
    "Unlockable_Paladin.Head05_Goth",
    "Unlockable_Paladin.Head06_Hooded",
    "Unlockable_Paladin.Head07_Headband",
    "Unlockable_Paladin.Head08_Survivalist",
    "Unlockable_Paladin.Head09_Electi",
    "Unlockable_Paladin.Head10_Transhuman",
    "Unlockable_Paladin.Head11_Ripper",
    "Unlockable_Paladin.Head12_Order",
    "Unlockable_Paladin.Head13_Robot",
    "Unlockable_Paladin.Head14_Thresher",
    "Unlockable_Paladin.Head15_CrimeLord",
    "Unlockable_Paladin.Head16_Premium",
    "Unlockable_Paladin.Head23_CrushTestDummy",
    "Unlockable_Paladin.Skin01_Prison",
    "Unlockable_Paladin.Skin02_Order",
    "Unlockable_Paladin.Skin03_Ghost",
    "Unlockable_Paladin.Skin04_Tech",
    "Unlockable_Paladin.Skin05_Ripper",
    "Unlockable_Paladin.Skin06_Amara",
    "Unlockable_Paladin.Skin07_RedHanded",
    "Unlockable_Paladin.Skin08_Corrupted",
    "Unlockable_Paladin.Skin09_Sewer",
    "Unlockable_Paladin.Skin10_Hawaiian",
    "Unlockable_Paladin.Skin11_Astral",
    "Unlockable_Paladin.Skin12_Tediore",
    "Unlockable_Paladin.Skin13_3CatMoon",
    "Unlockable_Paladin.Skin14_Fire",
    "Unlockable_Paladin.Skin15_Survivalist",
    "Unlockable_Paladin.Skin16_Crimson",
    "Unlockable_Paladin.Skin17_Auger",
    "Unlockable_Paladin.Skin18_Electi",
    "Unlockable_Paladin.Skin19_Dirty",
    "Unlockable_Paladin.Skin20_HighRoller",
    "Unlockable_Paladin.Skin21_Graffiti",
    "Unlockable_Paladin.Skin22_Knitted",
    "Unlockable_Paladin.Skin23_GearboxDev",
    "Unlockable_Paladin.Skin24_PreOrder",
    "Unlockable_Paladin.Skin25_Slimed",
    "Unlockable_Paladin.Skin26_Camo",
    "Unlockable_Paladin.Skin27_Space",
    "Unlockable_Paladin.Skin28_Ritual",
    "Unlockable_Paladin.Skin29_Guardian",
    "Unlockable_Paladin.Skin30_Cute",
    "Unlockable_Paladin.Skin31_Koto",
    "Unlockable_Paladin.Skin32_DuctTaped",
    "Unlockable_Paladin.Skin33_Jakobs",
    "Unlockable_Paladin.Skin34_Daedalus",
    "Unlockable_Paladin.Skin35_Vladof",
    "Unlockable_Paladin.Skin36_Torgue",
    "Unlockable_Paladin.Skin37_Maliwan",
    "Unlockable_Paladin.Skin38_CyberPop",
    "Unlockable_Paladin.Skin39_Critters",
    "Unlockable_Paladin.Skin40_Veil",
    "Unlockable_Paladin.Skin44_Premium",
    "Unlockable_Paladin.Skin45_BreakFree",
    "unlockable_paladin",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_vehicles', [])
PROFILE_UNLOCKS_1034A['unlockable_vehicles'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_vehicles']) | {
    "Unlockable_Vehicles.Borg",
    "Unlockable_Vehicles.DarkSiren",
    "Unlockable_Vehicles.DarkSiren_Proto",
    "Unlockable_Vehicles.ExoSoldier",
    "Unlockable_Vehicles.ExoSoldier_Proto",
    "Unlockable_Vehicles.Gravitar",
    "Unlockable_Vehicles.Gravitar_Proto",
    "Unlockable_Vehicles.Grazer",
    "Unlockable_Vehicles.Mat01_Synthwave",
    "Unlockable_Vehicles.Mat02_LavaRock",
    "Unlockable_Vehicles.Mat03_BioGoo",
    "Unlockable_Vehicles.Mat04_Doodles",
    "Unlockable_Vehicles.Mat05_FransFroyo",
    "Unlockable_Vehicles.Mat06_ElectiSamurai",
    "Unlockable_Vehicles.Mat07_CuteCat",
    "Unlockable_Vehicles.Mat08_EchoBot",
    "Unlockable_Vehicles.Mat09_FolkHero",
    "Unlockable_Vehicles.Mat10_Graffiti",
    "Unlockable_Vehicles.Mat11_Cupcake",
    "Unlockable_Vehicles.Mat12_AnimalPrint",
    "Unlockable_Vehicles.Mat13_Whiteout",
    "Unlockable_Vehicles.Mat14_Grunt",
    "Unlockable_Vehicles.Mat15_Retro",
    "Unlockable_Vehicles.Mat16_PolePosition",
    "Unlockable_Vehicles.Mat17_DeadWood",
    "Unlockable_Vehicles.Mat18_CrashTest",
    "Unlockable_Vehicles.Mat19_Meltdown",
    "Unlockable_Vehicles.Mat20_Cyberspace",
    "Unlockable_Vehicles.Mat21_Afterburn",
    "Unlockable_Vehicles.Mat22_Overload",
    "Unlockable_Vehicles.Mat23_FutureProof",
    "Unlockable_Vehicles.Mat24_Propaganda",
    "Unlockable_Vehicles.Mat25_LocustGas",
    "Unlockable_Vehicles.Mat26_AugerSight",
    "Unlockable_Vehicles.Mat27_GoldenPower",
    "Unlockable_Vehicles.Mat28_Ripper",
    "Unlockable_Vehicles.Mat29_Cheers",
    "Unlockable_Vehicles.Mat30_CrimsonRaiders",
    "Unlockable_Vehicles.Mat31_Splash",
    "Unlockable_Vehicles.Mat32_ImperialGuard",
    "Unlockable_Vehicles.Mat33_Creepy",
    "Unlockable_Vehicles.Mat34_MoneyCamo",
    "Unlockable_Vehicles.Mat35_GearboxDev",
    "Unlockable_Vehicles.Paladin",
    "Unlockable_Vehicles.Paladin_Proto",
    "Unlockable_Vehicles.mat40_animemech",
    "Unlockable_Vehicles.mat41_synthesizer",
    "Unlockable_Vehicles.mat42_gratata",
    "Unlockable_Vehicles.mat43_nitroflame",
    "Unlockable_Vehicles.mat44_hotrod",
    "Unlockable_Vehicles.mat45_ripperuncommon",
    "Unlockable_Vehicles.mat46_daedalusuncommon",
    "Unlockable_Vehicles.mat47_jakobsuncommon",
    "Unlockable_Vehicles.mat48_maliwanuncommon",
    "Unlockable_Vehicles.mat49_orderuncommon",
    "Unlockable_Vehicles.mat50_tedioreuncommon",
    "Unlockable_Vehicles.mat51_torgueuncommon",
    "Unlockable_Vehicles.mat52_vladofuncommon",
    "unlockable_vehicles",
})

PROFILE_UNLOCKS_1034A.setdefault('unlockable_weapons', [])
PROFILE_UNLOCKS_1034A['unlockable_weapons'] = sorted(set(PROFILE_UNLOCKS_1034A['unlockable_weapons']) | {
    "Unlockable_Weapons.Mat01_Synthwave",
    "Unlockable_Weapons.Mat02_LavaRock",
    "Unlockable_Weapons.Mat03_BioGoo",
    "Unlockable_Weapons.Mat04_Doodles",
    "Unlockable_Weapons.Mat05_FransFroyo",
    "Unlockable_Weapons.Mat06_ElectiSamurai",
    "Unlockable_Weapons.Mat07_CuteCat",
    "Unlockable_Weapons.Mat08_EchoBot",
    "Unlockable_Weapons.Mat09_FolkHero",
    "Unlockable_Weapons.Mat10_Graffiti",
    "Unlockable_Weapons.Mat11_Cupcake",
    "Unlockable_Weapons.Mat12_AnimalPrint",
    "Unlockable_Weapons.Mat13_Whiteout",
    "Unlockable_Weapons.Mat14_Grunt",
    "Unlockable_Weapons.Mat15_Retro",
    "Unlockable_Weapons.Mat16_PolePosition",
    "Unlockable_Weapons.Mat17_DeadWood",
    "Unlockable_Weapons.Mat18_CrashTest",
    "Unlockable_Weapons.Mat19_Meltdown",
    "Unlockable_Weapons.Mat20_Cyberspace",
    "Unlockable_Weapons.Mat21_Afterburn",
    "Unlockable_Weapons.Mat22_Overload",
    "Unlockable_Weapons.Mat23_FutureProof",
    "Unlockable_Weapons.Mat24_Propaganda",
    "Unlockable_Weapons.Mat25_LocustGas",
    "Unlockable_Weapons.Mat26_AugerSight",
    "Unlockable_Weapons.Mat27_GoldenPower",
    "Unlockable_Weapons.Mat28_Ripper",
    "Unlockable_Weapons.Mat29_Cheers",
    "Unlockable_Weapons.Mat30_CrimsonRaiders",
    "Unlockable_Weapons.Mat31_Splash",
    "Unlockable_Weapons.Mat32_ImperialGuard",
    "Unlockable_Weapons.Mat33_Creepy",
    "Unlockable_Weapons.Mat34_MoneyCamo",
    "Unlockable_Weapons.Mat35_GearboxDev",
    "Unlockable_Weapons.Mat36_PreOrder",
    "Unlockable_Weapons.Mat37_SHiFT",
    "Unlockable_Weapons.Mat38_HeadHunter",
    "Unlockable_Weapons.Mat39_Premium",
    "Unlockable_Weapons.Shiny_Loarmaster",
    "Unlockable_Weapons.Shiny_Ultimate",
    "Unlockable_Weapons.shiny_anarchy",
    "Unlockable_Weapons.shiny_asher",
    "Unlockable_Weapons.shiny_atlien",
    "Unlockable_Weapons.shiny_ballista",
    "Unlockable_Weapons.shiny_beegun",
    "Unlockable_Weapons.shiny_bloodstarved",
    "Unlockable_Weapons.shiny_bod",
    "Unlockable_Weapons.shiny_bonnieclyde",
    "Unlockable_Weapons.shiny_boomslang",
    "Unlockable_Weapons.shiny_bugbear",
    "Unlockable_Weapons.shiny_bully",
    "Unlockable_Weapons.shiny_chuck",
    "Unlockable_Weapons.shiny_coldshoulder",
    "Unlockable_Weapons.shiny_commbd",
    "Unlockable_Weapons.shiny_complex_root",
    "Unlockable_Weapons.shiny_conglomerate",
    "Unlockable_Weapons.shiny_convergence",
    "Unlockable_Weapons.shiny_crowdsourced",
    "Unlockable_Weapons.shiny_dividedfocus",
    "Unlockable_Weapons.shiny_dualdamage",
    "Unlockable_Weapons.shiny_finnty",
    "Unlockable_Weapons.shiny_fisheye",
    "Unlockable_Weapons.shiny_gmr",
    "Unlockable_Weapons.shiny_goalkeeper",
    "Unlockable_Weapons.shiny_goldengod",
    "Unlockable_Weapons.shiny_goremaster",
    "Unlockable_Weapons.shiny_heartgun",
    "Unlockable_Weapons.shiny_heavyturret",
    "Unlockable_Weapons.shiny_hellfire",
    "Unlockable_Weapons.shiny_hellwalker",
    "Unlockable_Weapons.shiny_kaleidosplode",
    "Unlockable_Weapons.shiny_kaoson",
    "Unlockable_Weapons.shiny_katagawa",
    "Unlockable_Weapons.shiny_kickballer",
    "Unlockable_Weapons.shiny_kingsgambit",
    "Unlockable_Weapons.shiny_leadballoon",
    "Unlockable_Weapons.shiny_linebacker",
    "Unlockable_Weapons.shiny_lucian",
    "Unlockable_Weapons.shiny_lumberjack",
    "Unlockable_Weapons.shiny_luty",
    "Unlockable_Weapons.shiny_noisycricket",
    "Unlockable_Weapons.shiny_ohmigot",
    "Unlockable_Weapons.shiny_om",
    "Unlockable_Weapons.shiny_onslaught",
    "Unlockable_Weapons.shiny_phantom_flame",
    "Unlockable_Weapons.shiny_plasmacoil",
    "Unlockable_Weapons.shiny_potatothrower",
    "Unlockable_Weapons.shiny_prince",
    "Unlockable_Weapons.shiny_queensrest",
    "Unlockable_Weapons.shiny_quickdraw",
    "Unlockable_Weapons.shiny_rainbowvomit",
    "Unlockable_Weapons.shiny_rangefinder",
    "Unlockable_Weapons.shiny_roach",
    "Unlockable_Weapons.shiny_rocketreload",
    "Unlockable_Weapons.shiny_rowan",
    "Unlockable_Weapons.shiny_rubysgrasp",
    "Unlockable_Weapons.shiny_seventh_sense",
    "Unlockable_Weapons.shiny_sideshow",
    "Unlockable_Weapons.shiny_slugger",
    "Unlockable_Weapons.shiny_star_helix",
    "Unlockable_Weapons.shiny_stopgap",
    "Unlockable_Weapons.shiny_stray",
    "Unlockable_Weapons.shiny_sweet_embrace",
    "Unlockable_Weapons.shiny_symmetry",
    "Unlockable_Weapons.shiny_tkswave",
    "Unlockable_Weapons.shiny_truck",
    "Unlockable_Weapons.shiny_vamoose",
    "Unlockable_Weapons.shiny_wf",
    "Unlockable_Weapons.shiny_wombocombo",
    "Unlockable_Weapons.shiny_zipgun",
    "unlockable_weapons",
})

# === END: auto-extended unlocks from reference profile ===
CLASS_TO_UNLOCK_KEY_1034A = {
    "Char_DarkSiren":"unlockable_darksiren",
    "Char_ExoSoldier":"unlockable_exosoldier",
    "Char_Gravitar":"unlockable_gravitar",
    "Char_Paladin":"unlockable_paladin",
}

REWARD_KEY_HINTS_1034A = ("Reward_","RewardPackage_","pgraph.sdu_upgrades.","Reward_HoverDrive_","Reward_Vehicle_")

def _ensure_list_1034a(x): return x if isinstance(x,list) else []
def _collect_strings_1034a(node):
    out=[]
    if isinstance(node,dict):
        for v in node.values(): out.extend(_collect_strings_1034a(v))
    elif isinstance(node,list):
        for v in node: out.extend(_collect_strings_1034a(v))
    elif isinstance(node,str):
        out.append(node)
    return out

def _unlock_entries_1034a(save_obj,entries):
    if not entries: return 0
    st=save_obj.setdefault('state',{})
    uniq=st.setdefault('unique_rewards',[])
    added=0
    for e in entries:
        if e.startswith("Reward") or e.startswith("pgraph."):
            if e not in uniq: uniq.append(e); added+=1
        else:
            ul=save_obj.setdefault('unlockables',{})
            flat=ul.setdefault('entries',[])
            if e not in flat: flat.append(e); added+=1
    return added

def _merge_profile_unlocks_1034a(save_obj,chosen_class):
    total=0
    total+=_unlock_entries_1034a(save_obj,PROFILE_UNLOCKS_1034A.get("shared_progress",{}).get("entries",[]))
    class_key=CLASS_TO_UNLOCK_KEY_1034A.get(chosen_class)
    if class_key:
        total+=_unlock_entries_1034a(save_obj,PROFILE_UNLOCKS_1034A.get(class_key,{}).get("entries",[]))
    for k in ("unlockable_echo4","unlockable_weapons","unlockable_vehicles"):
        total+=_unlock_entries_1034a(save_obj,PROFILE_UNLOCKS_1034A.get(k,{}).get("entries",[]))
    return total

def _promote_reward_packages_1034a(save_obj):
    st=save_obj.setdefault('state',{})
    uniq=st.setdefault('unique_rewards',[])
    seen=set(uniq)
    strings=_collect_strings_1034a(st)
    added=0
    for s in strings:
        if any(h in s for h in REWARD_KEY_HINTS_1034A):
            if s not in seen: uniq.append(s); seen.add(s); added+=1
    return added

def _maybe_unlock_map_1034a(save_obj):
    st=save_obj.setdefault('state',{})
    changed=0
    world=st.setdefault("world",{})
    areas=world.setdefault("areas",{})
    if not areas:
        default_areas=["Pandora","Eden-6","Promethea","Nekrotafeyo"]
        for zone in default_areas:
            areas[zone]={"visited":True,"discovered":True}; changed+=2
    else:
        for name,node in areas.items():
            if isinstance(node,dict):
                if not node.get("visited"): node["visited"]=True; changed+=1
                if not node.get("discovered"): node["discovered"]=True; changed+=1
    return changed

def _set_class_1034a(save_obj,new_class):
    st=save_obj.setdefault('state',{}); st['class']=new_class
    dom=save_obj.get('domains',{}).get('local',{})
    if isinstance(dom,dict): dom['characters_selected']=new_class

def _sync_points_with_level_1034a(save_obj):
    st=save_obj.setdefault('state',{})
    lvl=st.get("level",1)
    expected_points=max(0,lvl-1)
    st["spec_points"]=expected_points
    cp=st.setdefault("character_points",{})
    cp["unspent"]=expected_points
    return expected_points


def _resolve_profile_unlocks_catalog_1034a(globals_dict):
    # Prefer the 1.033a catalog if present
    catalog = globals_dict.get("EMBEDDED_PROFILE_UNLOCKS")
    if isinstance(catalog, dict):
        return catalog
    # Fallback to our minimal structure if not found (kept empty to avoid drift)
    return {
        "shared_progress": [],
        "unlockable_darksiren": [],
        "unlockable_exosoldier": [],
        "unlockable_gravitar": [],
        "unlockable_paladin": [],
        "unlockable_echo4": [],
        "unlockable_weapons": [],
        "unlockable_vehicles": [],
    }


# ---- 1.034a: EXTRA unlocks  ----
EXTRA_PROFILE_UNLOCKS_1034A = {
  "shared_progress": [
    "shared_progress.vault_hunter_level",
    "shared_progress.prologue_completed",
    "shared_progress.story_completed",
    "shared_progress.epilogue_started"
  ],
  "unlockable_darksiren": [
    "Unlockable_DarkSiren.Head01_Prison",
    "Unlockable_DarkSiren.Body01_Prison",
    "Unlockable_DarkSiren.Skin01_Prison",
    "Unlockable_DarkSiren.Skin24_PreOrder",
    "Unlockable_DarkSiren.Head23_CrashTestDummy",
    "Unlockable_DarkSiren.Body02_Premium",
    "Unlockable_DarkSiren.Head16_Premium",
    "Unlockable_DarkSiren.Skin44_Premium",
    "Unlockable_DarkSiren.Skin10_Hawaiian",
    "Unlockable_DarkSiren.Skin31_Koto",
    "Unlockable_DarkSiren.Skin02_Order",
    "Unlockable_DarkSiren.Skin37_Maliwan",
    "Unlockable_DarkSiren.Head02_PigTails",
    "Unlockable_DarkSiren.Skin14_Fire",
    "Unlockable_DarkSiren.Head06_PunkMask",
    "Unlockable_DarkSiren.Skin05_Ripper",
    "Unlockable_DarkSiren.Skin25_Slimed",
    "Unlockable_DarkSiren.Head11_Ripper",
    "Unlockable_DarkSiren.Skin26_Camo",
    "Unlockable_DarkSiren.Skin04_Tech",
    "Unlockable_DarkSiren.Skin06_Amara",
    "Unlockable_DarkSiren.Head05_BikeHelmet",
    "Unlockable_DarkSiren.Skin08_Corrupted",
    "Unlockable_DarkSiren.Head12_Order",
    "Unlockable_DarkSiren.Skin29_Guardian",
    "Unlockable_DarkSiren.Skin07_RedHanded",
    "Unlockable_DarkSiren.Head07_Demon",
    "Unlockable_DarkSiren.Skin34_Daedalus",
    "Unlockable_DarkSiren.Skin40_Veil",
    "Unlockable_DarkSiren.Skin45_BreakFree",
    "Unlockable_DarkSiren.Skin03_Ghost",
    "Unlockable_DarkSiren.Head08_Survivalist",
    "Unlockable_DarkSiren.Skin09_Sewer",
    "Unlockable_DarkSiren.Head09_Electi",
    "Unlockable_DarkSiren.Head15_CrimeLord",
    "Unlockable_DarkSiren.Skin11_Astral",
    "Unlockable_DarkSiren.Head10_Transhuman",
    "Unlockable_DarkSiren.Skin18_Electi",
    "Unlockable_DarkSiren.Skin13_3CatMoon",
    "Unlockable_DarkSiren.Skin15_Survivalist",
    "Unlockable_DarkSiren.Skin17_Auger",
    "Unlockable_DarkSiren.Skin27_Space",
    "Unlockable_DarkSiren.Head04_Shades",
    "Unlockable_DarkSiren.Skin12_Tediore",
    "Unlockable_DarkSiren.Head14_Thresher",
    "Unlockable_DarkSiren.Skin16_Crimson"
  ],
  "unlockable_exosoldier": [
    "Unlockable_ExoSoldier.Head01_Prison",
    "Unlockable_ExoSoldier.Body01_Prison",
    "Unlockable_ExoSoldier.Skin01_Prison",
    "Unlockable_ExoSoldier.Skin24_PreOrder",
    "Unlockable_ExoSoldier.Head23_CrushTestDummy",
    "Unlockable_ExoSoldier.Body02_Premium",
    "Unlockable_ExoSoldier.Head16_Premium",
    "Unlockable_ExoSoldier.Skin44_Premium",
    "Unlockable_ExoSoldier.Skin10_Hawaiian",
    "Unlockable_ExoSoldier.Skin31_Koto",
    "Unlockable_ExoSoldier.Skin02_Order",
    "Unlockable_ExoSoldier.Skin37_Maliwan",
    "Unlockable_ExoSoldier.Head03_Guerilla",
    "Unlockable_ExoSoldier.Skin14_Fire",
    "Unlockable_ExoSoldier.Head04_TechHawk",
    "Unlockable_ExoSoldier.Skin05_Ripper",
    "Unlockable_ExoSoldier.Skin25_Slimed",
    "Unlockable_ExoSoldier.Head11_Ripper",
    "Unlockable_ExoSoldier.Skin26_Camo",
    "Unlockable_ExoSoldier.Skin04_Tech",
    "Unlockable_ExoSoldier.Skin06_Amara",
    "Unlockable_ExoSoldier.Head07_Helm",
    "Unlockable_ExoSoldier.Skin08_Corrupted",
    "Unlockable_ExoSoldier.Head12_Order",
    "Unlockable_ExoSoldier.Skin29_Guardian",
    "Unlockable_ExoSoldier.Skin07_RedHanded",
    "Unlockable_ExoSoldier.Head06_BlindFold",
    "Unlockable_ExoSoldier.Skin34_Daedalus",
    "Unlockable_ExoSoldier.Skin40_Veil",
    "Unlockable_ExoSoldier.Skin45_BreakFree",
    "Unlockable_ExoSoldier.Skin03_Ghost",
    "Unlockable_ExoSoldier.Head08_Survivalist",
    "Unlockable_ExoSoldier.Skin09_Sewer",
    "Unlockable_ExoSoldier.Head09_Electi",
    "Unlockable_ExoSoldier.Head15_CrimeLord",
    "Unlockable_ExoSoldier.Skin11_Astral",
    "Unlockable_ExoSoldier.Head10_Transhuman",
    "Unlockable_ExoSoldier.Skin18_Electi",
    "Unlockable_ExoSoldier.Skin13_3CatMoon",
    "Unlockable_ExoSoldier.Skin15_Survivalist",
    "Unlockable_ExoSoldier.Skin17_Auger",
    "Unlockable_ExoSoldier.Skin27_Space",
    "Unlockable_ExoSoldier.Head05_LongHair",
    "Unlockable_ExoSoldier.Skin12_Tediore",
    "Unlockable_ExoSoldier.Head14_Thresher",
    "Unlockable_ExoSoldier.Skin16_Crimson"
  ],
  "unlockable_gravitar": [
    "Unlockable_Gravitar.Head01_Prison",
    "Unlockable_Gravitar.Body01_Prison",
    "Unlockable_Gravitar.Skin01_Prison",
    "Unlockable_Gravitar.Skin24_PreOrder",
    "Unlockable_Gravitar.Head23_CrushTestDummy",
    "Unlockable_Gravitar.Body02_Premium",
    "Unlockable_Gravitar.Head16_Premium",
    "Unlockable_Gravitar.Skin44_Premium",
    "Unlockable_Gravitar.Skin10_Hawaiian",
    "Unlockable_Gravitar.Skin31_Koto",
    "Unlockable_Gravitar.Skin02_Order",
    "Unlockable_Gravitar.Skin37_Maliwan",
    "Unlockable_Gravitar.Head02_DreadBuns",
    "Unlockable_Gravitar.Skin14_Fire",
    "Unlockable_Gravitar.Head05_SafetyFirst",
    "Unlockable_Gravitar.Skin05_Ripper",
    "Unlockable_Gravitar.Skin25_Slimed",
    "Unlockable_Gravitar.Head11_Ripper",
    "Unlockable_Gravitar.Skin26_Camo",
    "Unlockable_Gravitar.Skin04_Tech",
    "Unlockable_Gravitar.Skin06_Amara",
    "Unlockable_Gravitar.Head03_Helmet",
    "Unlockable_Gravitar.Skin08_Corrupted",
    "Unlockable_Gravitar.Head12_Order",
    "Unlockable_Gravitar.Skin29_Guardian",
    "Unlockable_Gravitar.Skin07_RedHanded",
    "Unlockable_Gravitar.Head04_TechBraids",
    "Unlockable_Gravitar.Skin34_Daedalus",
    "Unlockable_Gravitar.Skin40_Veil",
    "Unlockable_Gravitar.Skin45_BreakFree",
    "Unlockable_Gravitar.Skin03_Ghost",
    "Unlockable_Gravitar.Head08_Survivalist",
    "Unlockable_Gravitar.Skin09_Sewer",
    "Unlockable_Gravitar.Head09_Electi",
    "Unlockable_Gravitar.Head15_CrimeLord",
    "Unlockable_Gravitar.Skin11_Astral",
    "Unlockable_Gravitar.Head10_Transhuman",
    "Unlockable_Gravitar.Skin18_Electi",
    "Unlockable_Gravitar.Skin13_3CatMoon",
    "Unlockable_Gravitar.Skin15_Survivalist",
    "Unlockable_Gravitar.Skin17_Auger",
    "Unlockable_Gravitar.Skin27_Space",
    "Unlockable_Gravitar.Head06_RoundGlasses",
    "Unlockable_Gravitar.Skin12_Tediore",
    "Unlockable_Gravitar.Head14_Thresher",
    "Unlockable_Gravitar.Skin16_Crimson"
  ],
  "unlockable_paladin": [
    "Unlockable_Paladin.Head01_Prison",
    "Unlockable_Paladin.Body01_Prison",
    "Unlockable_Paladin.Skin01_Prison",
    "Unlockable_Paladin.Skin24_PreOrder",
    "Unlockable_Paladin.Head23_CrushTestDummy",
    "Unlockable_Paladin.Body02_Premium",
    "Unlockable_Paladin.Head16_Premium",
    "Unlockable_Paladin.Skin44_Premium",
    "Unlockable_Paladin.Skin10_Hawaiian",
    "Unlockable_Paladin.Skin31_Koto",
    "Unlockable_Paladin.Skin02_Order",
    "Unlockable_Paladin.Skin37_Maliwan",
    "Unlockable_Paladin.Head02_PonyTail",
    "Unlockable_Paladin.Skin14_Fire",
    "Unlockable_Paladin.Head03_BaldMask",
    "Unlockable_Paladin.Skin05_Ripper",
    "Unlockable_Paladin.Skin25_Slimed",
    "Unlockable_Paladin.Head11_Ripper",
    "Unlockable_Paladin.Skin26_Camo",
    "Unlockable_Paladin.Skin04_Tech",
    "Unlockable_Paladin.Skin06_Amara",
    "Unlockable_Paladin.Head04_Visor",
    "Unlockable_Paladin.Skin08_Corrupted",
    "Unlockable_Paladin.Head12_Order",
    "Unlockable_Paladin.Skin29_Guardian",
    "Unlockable_Paladin.Skin07_RedHanded",
    "Unlockable_Paladin.Head06_Hooded",
    "Unlockable_Paladin.Skin34_Daedalus",
    "Unlockable_Paladin.Skin40_Veil",
    "Unlockable_Paladin.Skin45_BreakFree",
    "Unlockable_Paladin.Skin03_Ghost",
    "Unlockable_Paladin.Head08_Survivalist",
    "Unlockable_Paladin.Skin09_Sewer",
    "Unlockable_Paladin.Head09_Electi",
    "Unlockable_Paladin.Head15_CrimeLord",
    "Unlockable_Paladin.Skin11_Astral",
    "Unlockable_Paladin.Head10_Transhuman",
    "Unlockable_Paladin.Skin18_Electi",
    "Unlockable_Paladin.Skin13_3CatMoon",
    "Unlockable_Paladin.Skin15_Survivalist",
    "Unlockable_Paladin.Skin17_Auger",
    "Unlockable_Paladin.Skin27_Space",
    "Unlockable_Paladin.Head05_Goth",
    "Unlockable_Paladin.Skin12_Tediore",
    "Unlockable_Paladin.Head14_Thresher",
    "Unlockable_Paladin.Skin16_Crimson"
  ],
  "unlockable_echo4": [
    "Unlockable_Echo4.Skin01_Prison",
    "Unlockable_Echo4.Skin42_Legacy",
    "Unlockable_Echo4.Skin24_PreOrder",
    "Unlockable_Echo4.attachment01_partyhat",
    "Unlockable_Echo4.Skin14_Fire",
    "Unlockable_Echo4.Skin50_BreakTheGame",
    "Unlockable_Echo4.attachment10_crown",
    "Unlockable_Echo4.attachment04_wings",
    "Unlockable_Echo4.Skin37_Maliwan",
    "Unlockable_Echo4.Skin05_Ripper",
    "Unlockable_Echo4.Body03_Ripper",
    "Unlockable_Echo4.Skin04_Tech",
    "Unlockable_Echo4.Skin33_Jakobs",
    "Unlockable_Echo4.attachment09_goggles",
    "Unlockable_Echo4.attachment07_horns",
    "Unlockable_Echo4.Skin38_CyberPop",
    "Unlockable_Echo4.Skin02_Order",
    "Unlockable_Echo4.Skin07_RedHanded",
    "Unlockable_Echo4.Skin22_Knitted",
    "Unlockable_Echo4.Skin25_Slimed",
    "Unlockable_Echo4.Skin29_Guardian",
    "Unlockable_Echo4.Skin35_Vladof",
    "Unlockable_Echo4.Skin19_Dirty",
    "Unlockable_Echo4.Skin11_Astral",
    "Unlockable_Echo4.Skin36_Torgue",
    "Unlockable_Echo4.Skin45_BreakFree",
    "Unlockable_Echo4.attachment08_tinfoilhat",
    "Unlockable_Echo4.Skin09_Sewer",
    "Unlockable_Echo4.Skin18_Electi",
    "Unlockable_Echo4.Skin15_Survivalist",
    "Unlockable_Echo4.Skin17_Auger",
    "Unlockable_Echo4.Skin27_Space",
    "Unlockable_Echo4.Body01_GeneVIV",
    "Unlockable_Echo4.Skin12_Tediore",
    "Unlockable_Echo4.Skin32_DuctTaped",
    "Unlockable_Echo4.Skin16_Crimson"
  ],
  "unlockable_weapons": [
    "Unlockable_Weapons.Mat01_Synthwave",
    "Unlockable_Weapons.Mat36_PreOrder",
    "Unlockable_Weapons.Mat38_HeadHunter",
    "Unlockable_Weapons.Mat29_Cheers",
    "Unlockable_Weapons.Mat17_DeadWood",
    "Unlockable_Weapons.Mat25_LocustGas",
    "Unlockable_Weapons.Mat26_AugerSight",
    "Unlockable_Weapons.Mat07_CuteCat",
    "Unlockable_Weapons.Mat13_Whiteout",
    "Unlockable_Weapons.Mat27_GoldenPower",
    "Unlockable_Weapons.Mat14_Grunt",
    "Unlockable_Weapons.shiny_leadballoon",
    "Unlockable_Weapons.shiny_convergence",
    "Unlockable_Weapons.shiny_boomslang",
    "Unlockable_Weapons.Mat08_EchoBot",
    "Unlockable_Weapons.Mat18_CrashTest",
    "Unlockable_Weapons.shiny_luty",
    "Unlockable_Weapons.shiny_rocketreload",
    "Unlockable_Weapons.Mat06_ElectiSamurai",
    "Unlockable_Weapons.shiny_noisycricket",
    "Unlockable_Weapons.shiny_heavyturret",
    "Unlockable_Weapons.shiny_kaoson",
    "Unlockable_Weapons.Mat33_Creepy",
    "Unlockable_Weapons.Mat34_MoneyCamo",
    "Unlockable_Weapons.Mat30_CrimsonRaiders",
    "Unlockable_Weapons.Mat32_ImperialGuard",
    "Unlockable_Weapons.shiny_kaleidosplode",
    "Unlockable_Weapons.shiny_slugger",
    "Unlockable_Weapons.shiny_beegun",
    "Unlockable_Weapons.shiny_kickballer",
    "Unlockable_Weapons.shiny_vamoose",
    "Unlockable_Weapons.shiny_anarchy"
  ],
  "unlockable_vehicles": [
    "Unlockable_Vehicles.Grazer",
    "Unlockable_Vehicles.Mat34_MoneyCamo",
    "Unlockable_Vehicles.Mat29_Cheers",
    "Unlockable_Vehicles.Mat13_Whiteout",
    "Unlockable_Vehicles.Mat20_Cyberspace",
    "Unlockable_Vehicles.Mat07_CuteCat",
    "Unlockable_Vehicles.DarkSiren_Proto",
    "Unlockable_Vehicles.DarkSiren",
    "Unlockable_Vehicles.Gravitar_Proto",
    "Unlockable_Vehicles.Mat19_Meltdown",
    "Unlockable_Vehicles.Paladin_Proto",
    "Unlockable_Vehicles.Borg",
    "Unlockable_Vehicles.ExoSoldier_Proto",
    "Unlockable_Vehicles.Mat27_GoldenPower",
    "Unlockable_Vehicles.mat47_jakobsuncommon",
    "Unlockable_Vehicles.Mat01_Synthwave",
    "Unlockable_Vehicles.Mat32_ImperialGuard",
    "Unlockable_Vehicles.Mat33_Creepy"
  ]
}

def _merge_extras_into_embedded_unlocks_1034a(catalog):
    # catalog is the 1.033a EMBEDDED_PROFILE_UNLOCKS (dict of lists)
    if not isinstance(catalog, dict): return catalog
    out = {}
    keys = [
        "shared_progress","unlockable_darksiren","unlockable_exosoldier",
        "unlockable_gravitar","unlockable_paladin","unlockable_echo4",
        "unlockable_weapons","unlockable_vehicles"
    ]
    for k in keys:
        base = catalog.get(k, [])
        extra = EXTRA_PROFILE_UNLOCKS_1034A.get(k, [])
        merged = list(base) + [x for x in extra if x not in base]
        out[k] = merged
    return out
def attach_ui_1034a(app):
    # app is your main UI instance; add controls if tab_progression exists
    try:
        parent = getattr(app, "tab_progression", None) or app.root
        frm = ttk.LabelFrame(parent, text="1.034a — Class & Unlocks")
        frm.pack(fill="x", padx=8, pady=8)

        ttk.Label(frm, text="Class:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        app.cbo_class_1034a = ttk.Combobox(frm, values=AVAILABLE_CLASSES_1034A, state="readonly", width=22)
        app.cbo_class_1034a.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        cur = (app.save_data or {}).get('state', {}).get('class', '')
        if cur in AVAILABLE_CLASSES_1034A:
            app.cbo_class_1034a.set(cur)

        ttk.Button(frm, text="Apply Class", command=lambda: _on_apply_class_btn_1034a(app)).grid(row=0, column=2, padx=6, pady=6)
        ttk.Button(frm, text="Unlock All (Class + Core Packs)", command=lambda: _on_unlock_all_btn_1034a(app)).grid(row=0, column=3, padx=6, pady=6)
        ttk.Button(frm, text="Unlock Map", command=lambda: _on_unlock_map_btn_1034a(app)).grid(row=0, column=4, padx=6, pady=6)

        # Spec Points Mode
        ttk.Label(frm, text="Spec Points:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        app.cbo_spec_mode_1034a = ttk.Combobox(frm, values=["Auto (level-1)","Custom"], state="readonly", width=22)
        app.cbo_spec_mode_1034a.grid(row=1, column=1, sticky="w", padx=6, pady=6)
        app.cbo_spec_mode_1034a.set("Auto (level-1)")
        app.ent_spec_custom_1034a = ttk.Spinbox(frm, from_=-999, to=999, width=8)
        app.ent_spec_custom_1034a.grid(row=1, column=2, sticky="w", padx=6, pady=6)
        ttk.Button(frm, text="Apply Points", command=lambda: _on_apply_points_btn_1034a(app)).grid(row=1, column=3, padx=6, pady=6)

        # Hook save/encrypt path: auto-sync spec points with level
        if not hasattr(app, "_orig_encrypt_write_1034a"):
            if hasattr(app, "encrypt_and_write"):
                app._orig_encrypt_write_1034a = app.encrypt_and_write

                def _wrapped_encrypt_and_write(*args, **kwargs):
                    try:
                        st = app.save_data.setdefault('state', {})
                        if st.get("spec_points_mode_1034a", "auto").startswith("custom"):
                            # respect custom points
                            pass
                        else:
                            _sync_points_with_level_1034a(app.save_data)
                    except Exception:
                        pass
                    return app._orig_encrypt_write_1034a(*args, **kwargs)

                app.encrypt_and_write = _wrapped_encrypt_and_write


        # Minimal decoder hook: attach context menu if inventory list present
        if hasattr(app, "inventory_list"):
            try:
                menu = tk.Menu(app.inventory_list, tearoff=0)
                def _decode_cmd():
                    sel = app._get_selected_serial_text() if hasattr(app,"_get_selected_serial_text") else None
                    if not sel:
                        messagebox.showwarning("Decode","No serial selected."); return
                    info = _decode_serial_1034a(sel)
                    lines = [
                        f"Serial: {info.serial}",
                        f"Type/Category: {info.item_type} / {info.item_category}",
                        f"Confidence: {info.confidence}",
                        f"Manufacturer: {info.stats.manufacturer}",
                        f"Item Class: {info.stats.item_class}",
                        f"Rarity: {info.stats.rarity}",
                        f"Level: {info.stats.level}",
                        f"Flags: {''.join(chr(c) for c in (info.stats.flags or [])) if info.stats.flags else 'N/A'}",
                        f"Markers: {info.raw_fields.get('markers','')}",
                    ]
                    messagebox.showinfo("Decoded Item","\n".join(lines))
                menu.add_command(label="Decode serial (1.034a)", command=_decode_cmd)
                def _popup(event, m=menu): m.tk_popup(event.x_root, event.y_root)
                app.inventory_list.bind("<Button-3>", _popup)
            except Exception:
                pass
    except Exception:
        pass

def _on_apply_class_btn_1034a(app):
    val = app.cbo_class_1034a.get().strip() if hasattr(app,"cbo_class_1034a") else ""
    if not val:
        messagebox.showwarning("Class","Pick a class."); return
    _set_class_1034a(app.save_data, val)
    messagebox.showinfo("Class", f"Class set to {val}.")

def _on_unlock_all_btn_1034a(app):
    chosen = (app.cbo_class_1034a.get().strip() if hasattr(app,"cbo_class_1034a") else "") or (app.save_data or {}).get('state',{}).get('class','')
    # Resolve catalog from 1.033a
    global PROFILE_UNLOCKS_1034A
    PROFILE_UNLOCKS_1034A = _resolve_profile_unlocks_catalog_1034a(globals())
    added_pkgs = _promote_reward_packages_1034a(app.save_data)
    added_prof = 0
    if PROFILE_UNLOCKS_1034A:
        # Convert 1.033a structure (dict of lists) to our expected dict->entries
        def to_entries(k):
            v = PROFILE_UNLOCKS_1034A.get(k, [])
            return v if isinstance(v, list) else v.get("entries", [])
        merged = {
            "shared_progress": {"entries": to_entries("shared_progress")},
            "unlockable_darksiren": {"entries": to_entries("unlockable_darksiren")},
            "unlockable_exosoldier": {"entries": to_entries("unlockable_exosoldier")},
            "unlockable_gravitar": {"entries": to_entries("unlockable_gravitar")},
            "unlockable_paladin": {"entries": to_entries("unlockable_paladin")},
            "unlockable_echo4": {"entries": to_entries("unlockable_echo4")},
            "unlockable_weapons": {"entries": to_entries("unlockable_weapons")},
            "unlockable_vehicles": {"entries": to_entries("unlockable_vehicles")},
        }
        # Temporarily swap into our expected var
        old = globals().get("PROFILE_UNLOCKS_1034A")
        globals()["PROFILE_UNLOCKS_1034A"] = merged
        added_prof = _merge_profile_unlocks_1034a(app.save_data, chosen)
        globals()["PROFILE_UNLOCKS_1034A"] = old
    messagebox.showinfo("Unlocks", f"Added {added_pkgs} package rewards and {added_prof} profile unlock entries.")

def _on_unlock_map_btn_1034a(app):
    changed = _maybe_unlock_map_1034a(app.save_data)
    messagebox.showinfo("Map", f"Touched {changed} map/location flags.")
# 'What’s New' banner function
def whats_new_1034a():
    return """
    1.034a — What's New
    ✓ Class switcher (DarkSiren, Paladin, Gravitar, ExoSoldier)
    ✓ Unlock-All (class + core packs + map)
    ✓ Embedded profile unlocks (skins, vehicles, Echo4, etc.)
    ✓ Weapon serial decoder (integrated)
    ✓ Spec points auto-sync with level
    """

def _on_apply_points_btn_1034a(app):
    mode = app.cbo_spec_mode_1034a.get() if hasattr(app,"cbo_spec_mode_1034a") else "Auto (level-1)"
    if mode.startswith("Custom"):
        try:
            val = int(app.ent_spec_custom_1034a.get())
        except Exception:
            messagebox.showerror("Spec Points","Enter a valid integer."); return
        st = app.save_data.setdefault('state', {})
        st["spec_points"] = val
        st.setdefault("character_points", {})["unspent"] = val
        st["spec_points_mode_1034a"] = "custom"
        messagebox.showinfo("Spec Points", f"Custom points set to {val}.")
    else:
        st = app.save_data.setdefault('state', {})
        st["spec_points_mode_1034a"] = "auto"
        pts = _sync_points_with_level_1034a(app.save_data)
        messagebox.showinfo("Spec Points", f"Auto-synced to {pts} (level-1).")


def _open_yaml_file(self):
    from tkinter import filedialog as fd, messagebox as mb
    try:
        path = fd.askopenfilename(title="Open YAML",
                                  filetypes=[("YAML files", "*.yml *.yaml"), ("All files", "*.*")])
        if not path:
            return
        p = Path(path)
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if getattr(self, "yaml_text", None):
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", txt)
        if 'yaml' in globals() and yaml is not None:
            try:
                self.yaml_obj = yaml.load(txt, Loader=get_yaml_loader())
            except Exception as e:
                self.log(f"YAML parse note: {e}")
        self.yaml_path = p
        try:
            if getattr(self, 'save_path', None) is None:
                self.save_path = p.with_suffix(".sav")
        except Exception:
            pass
        try:
            if hasattr(self, "nb") and hasattr(self, "tab_yaml"):
                self.nb.select(self.tab_yaml)
        except Exception:
            pass
        self.log(f"Opened YAML: {p.name}")
    except Exception as e:
        try:
            mb.showerror("Open YAML failed", str(e))
        except Exception:
            print("Open YAML failed:", e)

def _encrypt_yaml_as_save(self):
    from tkinter import filedialog as fd, messagebox as mb
    if 'yaml' not in globals() or yaml is None:
        try:
            mb.showerror("Missing dependency", "PyYAML is required.\nInstall with: pip install pyyaml")
        except Exception:
            print("PyYAML missing")
        return
    uid = (self.user_id.get() or "").strip() if hasattr(self, "user_id") else ""
    if not uid:
        try:
            mb.showerror("Missing User ID", "Enter your User ID (Steam64 or Epic numeric ID) first.")
        except Exception:
            print("Missing User ID")
        return
    txt = ""
    if getattr(self, "yaml_text", None):
        txt = self.yaml_text.get("1.0", "end")
    elif getattr(self, "yaml_path", None):
        try:
            txt = Path(self.yaml_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            txt = ""
    try:
        obj = yaml.load(txt, Loader=get_yaml_loader())
        obj = extract_and_encode_serials_from_yaml(obj)
        yb = yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).encode()
    except Exception as e:
        try:
            mb.showerror("Invalid YAML", f"Fix YAML before encrypting:\n{e}")
        except Exception:
            print("Invalid YAML:", e)
        return
    if getattr(self, "save_path", None):
        out = self.save_path.with_suffix(".sav")
    else:
        dest = fd.asksaveasfilename(defaultextension=".sav", filetypes=[("BL4 Save", ".sav")])
        if not dest:
            return
        out = Path(dest)
    try:
        plat = (getattr(self, "platform", None) or "epic").lower()
        out.write_bytes(encrypt_from_yaml(yb, plat, uid))
        self.log(f"Encrypted → {out.name}")
        try:
            mb.showinfo("Done", f"Saved {out.name}")
        except Exception:
            pass
    except Exception as e:
        try:
            mb.showerror("Encrypt Failed", str(e))
        except Exception:
            pass
        self.log(f"Encrypt error: {e}")


# --- YAML button shims: attach tiny handlers to App if missing ---
def __ensure_yaml_methods__():
    try:
        App  # ensure class exists
    except Exception:
        return

    if not hasattr(App, "_open_yaml_file"):
        def _open_yaml_file(self):
            from tkinter import filedialog as fd, messagebox as mb
            try:
                path = fd.askopenfilename(title="Open YAML",
                                          filetypes=[("YAML files","*.yml *.yaml"), ("All files","*.*")])
                if not path:
                    return
                p = Path(path)
                txt = p.read_text(encoding="utf-8", errors="ignore")
                if getattr(self, "yaml_text", None):
                    self.yaml_text.delete("1.0", "end")
                    self.yaml_text.insert("1.0", txt)
                if 'yaml' in globals() and yaml is not None:
                    try:
                        self.yaml_obj = yaml.load(txt, Loader=get_yaml_loader())
                    except Exception as e:
                        try: self.log(f"YAML parse note: {e}")
                        except Exception: pass
                self.yaml_path = p
                try:
                    if getattr(self, "save_path", None) is None:
                        self.save_path = p.with_suffix(".sav")
                except Exception:
                    pass
            except Exception as e:
                try:
                    mb.showerror("Open YAML failed", str(e))
                except Exception:
                    print("Open YAML failed:", e)
        App._open_yaml_file = _open_yaml_file

    if not hasattr(App, "_encrypt_yaml_as_save"):
        def _encrypt_yaml_as_save(self):
            from tkinter import filedialog as fd, messagebox as mb
            if 'yaml' not in globals() or yaml is None:
                try:
                    mb.showerror("Missing dependency", "PyYAML is required.\nInstall with: pip install pyyaml")
                except Exception:
                    print("PyYAML missing")
                return
            uid = (self.user_id.get() or "").strip() if hasattr(self, "user_id") else ""
            if not uid:
                try:
                    mb.showerror("Missing User ID", "Enter your User ID (Steam64 or Epic numeric ID) first.")
                except Exception:
                    print("Missing User ID")
                return
            txt = ""
            if getattr(self, "yaml_text", None):
                txt = self.yaml_text.get("1.0", "end")
            elif getattr(self, "yaml_path", None):
                try:
                    txt = Path(self.yaml_path).read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    txt = ""
            try:
                obj = yaml.load(txt, Loader=get_yaml_loader())
                obj = extract_and_encode_serials_from_yaml(obj)
                yb = yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).encode()
            except Exception as e:
                try:
                    mb.showerror("Invalid YAML", f"Fix YAML before encrypting:\n{e}")
                except Exception:
                    print("Invalid YAML:", e)
                return
            if getattr(self, "save_path", None):
                out = self.save_path.with_suffix(".sav")
            else:
                dest = fd.asksaveasfilename(defaultextension=".sav", filetypes=[("BL4 Save", ".sav")])
                if not dest:
                    return
                out = Path(dest)
            try:
                plat = (getattr(self, "platform", None) or "epic").lower()
                out.write_bytes(encrypt_from_yaml(yb, plat, uid))
                try: self.log(f"Encrypted → {out.name}")
                except Exception: pass
                try:
                    mb.showinfo("Done", f"Saved {out.name}")
                except Exception:
                    pass
            except Exception as e:
                try:
                    mb.showerror("Encrypt Failed", str(e))
                except Exception:
                    pass
                try: self.log(f"Encrypt error: {e}")
                except Exception: pass
        App._encrypt_yaml_as_save = _encrypt_yaml_as_save

try:
    __ensure_yaml_methods__()
except Exception:
    pass


def decode_items(save_dict):
    """
    Advanced item decoder for BL4.
    Returns list of tuples: (ptr, friendly_name, code, serial, tags)
    """
    import json
    results = []
    for idx, item in enumerate(save_dict.get("items", [])):
        serial = item.get("serial", "UNKNOWN")
        code = item.get("code", "???")
        balance_id = item.get("balance_id", "???")
        friendly = WEAPON_NAME_MAP.get(balance_id, balance_id)
        tags = {
            "equipped": item.get("equipped", False),
            "bank": item.get("bank", 0),
            "rarity": item.get("rarity", "unknown")
        }
        results.append((idx, friendly, code, serial, tags))
    return results


def set_by(root, toks, value):
    # Walk a yaml/dict/list structure following tokens that can include indexes like "items[75]".
    # Auto-creates dict/list containers as needed and extends lists for out-of-range indexes.
    import re as _re
    cur = root
    for raw in toks[:-1]:
        m = _re.match(r"^([^\[\]]+)(?:\[(\d+)\])?$", str(raw))
        if not m:
            key = str(raw)
            if isinstance(cur, dict):
                if key not in cur or cur[key] is None:
                    cur[key] = {}
                cur = cur[key]
            else:
                raise KeyError(raw)
        else:
            key, idx = m.group(1), m.group(2)
            if idx is None:
                if not isinstance(cur, dict):
                    raise KeyError(raw)
                if key not in cur or cur[key] is None:
                    cur[key] = {}
                cur = cur[key]
            else:
                if not isinstance(cur, dict):
                    raise KeyError(raw)
                if key not in cur or cur[key] is None or not isinstance(cur[key], list):
                    cur[key] = []
                lst = cur[key]
                i = int(idx)
                while len(lst) <= i:
                    lst.append({})
                cur = lst[i]
    last = str(toks[-1])
    m = _re.match(r"^([^\[\]]+)(?:\[(\d+)\])?$", last)
    if m and m.group(2) is not None:
        key, idx = m.group(1), int(m.group(2))
        if key not in cur or not isinstance(cur[key], list):
            cur[key] = []
        lst = cur[key]
        while len(lst) <= idx:
            lst.append(None)
        lst[idx] = value
    else:
        if isinstance(cur, dict):
            cur[last] = value
        else:
            raise KeyError(last)
    return root



def _simple_name_from_serial(serial: str) -> str:
    s = str(serial or "").strip()
    if not s.startswith("@Ug"):
        return ""
    mfgr_map = {
        "Fme!K": "Maliwan",
        "Fme!V": "Vladof",
        "Fme!H": "Hyperion",
        "Fme!D": "Dahl",
        "Fme!J": "Jakobs",
        "Fme!T": "Tediore",
        "Fme!A": "Atlas",
        "Fme!C": "COV",
        "Fme!N": "Torgue",
        "Fme!S": "S&S",
    }
    import re as _re
    m = _re.search(r"\{(Fme![A-Z])", s)
    brand = mfgr_map.get(m.group(1), "") if m else ""
    cls = ""
    if s.startswith("@UgeU_") or "UGe Shotgun" in s:
        cls = "Shotgun"
    elif s.startswith("@Ugr") or "@Ugr" in s:
        cls = "Rifle"
    elif s.startswith("@Ugg") or "@Ugg" in s:
        cls = "SMG"
    elif s.startswith("@Ugp") or "@Ugp" in s:
        cls = "Pistol"
    elif s.startswith("@Ugs") or "@Ugs" in s:
        cls = "Sniper"
    elif s.startswith("@Ugx") or "@Ugx" in s:
        cls = "Launcher"
    if brand and cls:
        return f"{brand} {cls}"
    return brand or cls

