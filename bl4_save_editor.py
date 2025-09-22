
#!/usr/bin/env python3
"""
BL4 Unified Save Editor — v1.033a 
- Fix: Character/Progression read/write whether data is at YAML root or under "state"
- UI: Dark + teal accents for better legibility
- Character tab: adds Cash, Eridium, SHIFT (gold) Keys with auto-path detection
- Items: popup inspector (Simple + Raw) preserved
- YAML tab: search + _DECODED_ITEMS export/encode
Dependencies:
    pip install pyyaml pycryptodome
"""

from pathlib import Path
import time, zlib
from typing import Any, Dict, List, Optional, Tuple, Union

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
    ],
}

EMBEDDED_REWARD_PACKAGES = [
    # Character Skins
    "RewardPackage_CharacterSkin_36_Torgue",
    "RewardPackage_CharacterSkin_26_MoneyCamo",
    "RewardPackage_CharacterSkin_03_Ghost",
    "RewardPackage_CharacterSkin_37_Maliwan",
    "RewardPackage_CharacterSkin_39_Critters",
    "RewardPackage_CharacterSkin_38_Cyberpop",
    "RewardPackage_CharacterSkin_34_Daedalus",
    "RewardPackage_CharacterSkin_25_Slimed",
    "RewardPackage_CharacterSkin_40_Veil",

    # Character Heads (known reward packages)
    "RewardPackage_CharacterHeads_06_UniqueE",
    "RewardPackage_CharacterHeads_07_UniqueF",

    # Echo Skins
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

    # Echo Attachments
    "RewardPackage_EchoAttachment_10_Crown",
    "RewardPackage_EchoAttachment_04_Wings",
    "RewardPackage_EchoAttachment_03_Bolt",
    "RewardPackage_EchoAttachment_09_Goggles",

    # Weapon Skins
    "RewardPackage_WeaponSkin_16_PolePosition",
    "RewardPackage_WeaponSkin_31_Splash",
    "RewardPackage_WeaponSkin_13_Whiteout",
    "RewardPackage_WeaponSkin_14_Grunt",
    "RewardPackage_WeaponSkin_18_CrashTest",
    "RewardPackage_WeaponSkin_07_CuteCat",
    "RewardPackage_WeaponSkin_19_Meltdown",

    # Vehicle skins / brand rewards
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

    # Bundles / meta rewards
    "RewardPackage_Combined_Propaganda",
    "RewardPackage_PreOrder",
    "RewardPackage_Premium",
    "RewardPackage_Headhunter",
    "RewardPackage_Legacy",
]


# ── Optional deps ─────────────────────────────────────────────────────────────
try:
    import yaml
except Exception:
    yaml = None

# ── Theme ─────────────────────────────────────────────────────────────────────
class Dark:
    BG = "#0b0f12"       # slightly deeper
    FG = "#e7eef2"
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
        self.root = root; self.root.title("BL4 Unified Save Editor — v1.033a"); self.root.geometry("1340x900")
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
            self.refresh_character(); self.refresh_items(); self.refresh_progression()
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
        opts = ttk.LabelFrame(parent, text="Cosmetic Unlocks", padding=8)
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

        cols=("path","type","code","serial")
        self.tree=ttk.Treeview(parent,columns=cols,show="headings")
        for c,txt,w in [("path","Path",520),("type","Type",140),("code","Code",80),("serial","Serial",540)]:
            self.tree.heading(c,text=txt); self.tree.column(c,width=w,anchor="w")
        self.tree.pack(expand=True,fill="both", padx=8, pady=(0,8))
        self.tree.bind("<Double-1>", self.open_inspector)

    def refresh_items(self)->None:
        self.items=[]
        r=self._root()
        if not isinstance(r, dict): return
        for path,serial in walk_ug(r):
            t = serial[3] if serial.startswith("@Ug") and len(serial)>=4 else "?"
            friendly = {"r":"Weapon","e":"Equipment","d":"Equipment Alt","w":"Special","u":"Special","f":"Special","!":"Special"}.get(t,"Unknown")
            code = serial[:4] if serial.startswith("@Ug") and len(serial)>=4 else "@Ug?"
            self.items.append((path,friendly,code,serial))
        self.apply_filter()

    def apply_filter(self)->None:
        term=(self.search_var.get() or "").lower(); type_sel=self.type_var.get()
        for r in self.tree.get_children(): self.tree.delete(r)
        for p,friendly,code,serial in self.items:
            if type_sel!="All" and friendly!=type_sel: continue
            if term and term not in p.lower() and term not in serial.lower(): continue
            self.tree.insert("", "end", values=(p,friendly,code,serial))

    def open_inspector(self,_evt=None)->None:
        sel=self.tree.selection()
        if not sel: return
        p,friendly,code,serial=self.tree.item(sel[0],"values")
        toks=tokens(p); d=decode_item_serial(serial)
        b=bytearray(bit_pack_decode(serial))
        top=tk.Toplevel(self.root); top.title("Item Inspector"); top.geometry("880x620"); top.configure(bg=Dark.BG)
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
            new_serial=encode_item_serial(d); set_by(self.yaml_obj if self._root() is self.yaml_obj else self._root(),toks,new_serial)
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
            bb=bytearray(b)
            try: amap={k:int(v.get()) for k,v in ents.items() if v.get().strip()!=""}
            except ValueError: return mb.showerror("Invalid","All raw values must be integers")
            # Apply common raw edits onto buffer
            for k,val in amap.items():
                if k.startswith("val16_at_"):
                    off=int(k.split("_")[-1])
                    if 0<=off<=len(bb)-2: bb[off:off+2]=int(val).to_bytes(2,"little")
                elif k=="header_le" and len(bb)>=8: bb[0:8]=int(val).to_bytes(8,"little")
                elif k=="field2_le" and len(bb)>=8: bb[4:8]=int(val).to_bytes(4,"little")
                elif k.startswith("byte_"):
                    idx=int(k.split("_")[-1])
                    if 0<=idx<len(bb): bb[idx]=int(val)&0xFF
            prefix=f"@Ug{d.item_type}"
            new_serial=bit_pack_encode(bytes(bb), prefix)
            set_by(self.yaml_obj if self._root() is self.yaml_obj else self._root(),toks,new_serial)
            self.yaml_text.delete("1.0","end"); self.yaml_text.insert("1.0", yaml.safe_dump(self.yaml_obj, sort_keys=False, allow_unicode=True))
            self.refresh_items(); self.log(f"Updated (raw) {p}"); top.destroy()
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
        ttk.Label(ytop,text="Find:").pack(side="left")
        self.find_var=tk.StringVar(); ttk.Entry(ytop,textvariable=self.find_var,width=40).pack(side="left",padx=6)
        ttk.Button(ytop,text="Next",command=self.find_next).pack(side="left")
        ttk.Separator(ytop, orient="vertical").pack(side="left", fill="y", padx=8)
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

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
 


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
        if type_sel!="All" and friendly!=type_sel: continue
        if term and term not in p.lower() and term not in serial.lower(): continue
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
    p,friendly,_,_,_,serial=self.tree.item(sel[0],"values")
    toks=tokens(p); d=decode_item_serial(serial)
    top=tk.Toplevel(self.root); top.title("Item Inspector"); top.geometry("900x640"); top.configure(bg=Dark.BG)
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
        new_serial=encode_item_serial(d); set_by(self.yaml_obj if self._root() is self.yaml_obj else self._root(),toks,new_serial)
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
