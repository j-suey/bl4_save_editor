# bl4_save_editor (Epic and Steam)
A lightweight, Python-based save editor for BL4. Export saves to YAML, edit values, and write them back safely. No EXEs included — run it your way.

# BL4 Save Editor (WIP)

Edit and inspect BL4 character saves via a simple, script-friendly workflow — no bundled EXEs. You control your environment, run it locally, and customize as you like.

> **Back up your saves first.** This tool directly reads/writes save files; always keep a manual backup before making changes.

---

## Features (initial scope)

- Read a BL4 save and export to human-readable YAML.
- Modify character props (levels, XP), skills, and progression nodes.
- Write changes back to a valid save file.
- Designed for CLI/automation; no GUI required.

**Example YAML (excerpt):**
```yaml
class: Char_DarkSiren
char_name: Vex
player_difficulty: Hard
experience:
  - type: Character
    level: 50
    points: 3430227
  - type: Specialization
    level: 57
    points: 6863836

progression:
  graphs:
  - name: Progress_DarkSiren_ActionSkills
    group_def_name: ProgressGroup_DarkSiren
    nodes:
    - name: Phase Echo
      is_activated: true

  - name: Progress_DarkSiren_ActionSkill_Modifiers_PhaseShard
    group_def_name: ProgressGroup_DarkSiren
    nodes:
    - name: Wither
      is_activated: true
      activation_level: 1
    - name: Banshee Wail
      is_activated: true
    - name: Wake the Dead
      is_activated: true

  - name: Progress_DS_Trunk_Domination
    group_def_name: ProgressGroup_DarkSiren
    nodes:
    - name: Phase Bullets
      points_spent: 2
