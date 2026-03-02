from dataclasses import dataclass, field
from typing import Optional
from utils.display import (
    box_top, box_bottom, box_row, box_separator,
    print_message, prompt_choice, press_enter, clr, Color
)


@dataclass
class Quest:
    key: str
    name: str
    description: str
    flavor: str
    condition_type: str
    condition_target: int
    condition_tag: str
    reward_gold: int
    reward_xp: int
    reward_item: Optional[str] = None


ALL_QUESTS: dict[str, Quest] = {}

def _q(quest: Quest):
    ALL_QUESTS[quest.key] = quest


_q(Quest(
    key="kill_5_goblins",
    name="La Plaga Verde",
    description="Eliminá 5 goblins.",
    flavor="Son chiquitos pero insoportables. Como las notificaciones del celu.",
    condition_type="kills_type", condition_target=5, condition_tag="goblin",
    reward_gold=40, reward_xp=100,
))

_q(Quest(
    key="kill_10_undead",
    name="Que Descansen en Paz",
    description="Eliminá 10 no-muertos (esqueletos, zombies o vampiros).",
    flavor="Una vez, dos veces. Los muertos son testarudos pero vos más.",
    condition_type="kills_type", condition_target=10, condition_tag="undead",
    reward_gold=80, reward_xp=200, reward_item="health_potion",
))

_q(Quest(
    key="kill_3_bosses",
    name="Cazador de Jefes",
    description="Derrotá 3 jefes de piso.",
    flavor="Tres bestias enormes. Vos solo. Nivel de locura: máximo.",
    condition_type="kills_type", condition_target=3, condition_tag="boss",
    reward_gold=300, reward_xp=600, reward_item="elixir",
))

_q(Quest(
    key="kill_20_enemies",
    name="El Matador",
    description="Eliminá 20 enemigos en total.",
    flavor="Veinte. No veinte mil, veinte. Tranquilo que llegás.",
    condition_type="kills", condition_target=20, condition_tag="",
    reward_gold=100, reward_xp=250,
))

_q(Quest(
    key="kill_50_enemies",
    name="Carnicero de Aethoria",
    description="Eliminá 50 enemigos en total.",
    flavor="Cincuenta cuerpos después, la mazmorra te empieza a respetar.",
    condition_type="kills", condition_target=50, condition_tag="",
    reward_gold=250, reward_xp=500, reward_item="greater_health_potion",
))

_q(Quest(
    key="kill_orc",
    name="Problema de Vecindario",
    description="Eliminá 3 orcos.",
    flavor="Son enormes, huelen mal y no pagan alquiler. Fuera.",
    condition_type="kills_type", condition_target=3, condition_tag="orc",
    reward_gold=60, reward_xp=120,
))

_q(Quest(
    key="kill_demon",
    name="Exorcismo Express",
    description="Eliminá 2 demonios.",
    flavor="Sin sacerdote, sin ritual. Solo vos y muchas ganas.",
    condition_type="kills_type", condition_target=2, condition_tag="demon",
    reward_gold=120, reward_xp=280, reward_item="mana_potion",
))


_q(Quest(
    key="clear_3_floors",
    name="Turista de Mazmorras",
    description="Completá 3 pisos de la mazmorra.",
    flavor="Tres pisos. Ya sos más veterano que el 90% de los que entraron.",
    condition_type="floors", condition_target=3, condition_tag="",
    reward_gold=150, reward_xp=300,
))

_q(Quest(
    key="clear_7_floors",
    name="Habitué del Calabozo",
    description="Completá 7 pisos de la mazmorra.",
    flavor="Siete pisos. La mazmorra ya te conoce. No es buena señal pero tampoco mala.",
    condition_type="floors", condition_target=7, condition_tag="",
    reward_gold=400, reward_xp=700, reward_item="elixir",
))

_q(Quest(
    key="reach_level_5",
    name="Dejaste de Ser Novato",
    description="Llegá al nivel 5.",
    flavor="Nivel 5. Ya podés decir que sabés lo que hacés. Más o menos.",
    condition_type="level", condition_target=5, condition_tag="",
    reward_gold=100, reward_xp=0,
))

_q(Quest(
    key="reach_level_10",
    name="Veterano",
    description="Llegá al nivel 10.",
    flavor="Nivel 10. La mitad del camino. La parte fácil ya quedó atrás.",
    condition_type="level", condition_target=10, condition_tag="",
    reward_gold=250, reward_xp=0, reward_item="greater_health_potion",
))


_q(Quest(
    key="earn_500_gold",
    name="Capitalista de Mazmorra",
    description="Acumulá 500 monedas de oro.",
    flavor="Quinientas monedas. En una mazmorra. Emprendedor, digamos.",
    condition_type="gold_total", condition_target=500, condition_tag="",
    reward_gold=0, reward_xp=150, reward_item="mana_potion",
))

_q(Quest(
    key="earn_2000_gold",
    name="Magnate del Subsuelo",
    description="Acumulá 2000 monedas de oro.",
    flavor="Dos mil monedas. La economía de la mazmorra te pertenece.",
    condition_type="gold_total", condition_target=2000, condition_tag="",
    reward_gold=500, reward_xp=300, reward_item="ruby",
))

_q(Quest(
    key="collect_5_items",
    name="Acumulador",
    description="Recogé 10 objetos a lo largo del juego.",
    flavor="Diez objetos. No importa cuáles. Sos un coleccionista, básicamente.",
    condition_type="items_collected", condition_target=10, condition_tag="",
    reward_gold=80, reward_xp=120,
))


_q(Quest(
    key="survive_trap",
    name="Vivir Peligrosamente",
    description="Esquivá 3 trampas.",
    flavor="Tres veces casi te mató el piso. Ya sos más cuidadoso.",
    condition_type="traps_avoided", condition_target=3, condition_tag="",
    reward_gold=60, reward_xp=100,
))

_q(Quest(
    key="flee_combat",
    name="Discreción es Valor",
    description="Huí exitosamente de 3 combates.",
    flavor="Rajaste tres veces y seguís vivo. Eso no es cobardía, es estrategia.",
    condition_type="fled_combats", condition_target=3, condition_tag="",
    reward_gold=50, reward_xp=80,
))


class QuestManager:
    """
    Manages quest progress and completion for the player.
    Stored inside player.quest_data dict.
    """

    def __init__(self, quest_data: dict = None):
        """
        quest_data format:
        {
          "active":    ["quest_key", ...],
          "completed": ["quest_key", ...],
          "progress":  {"quest_key": current_value, ...},
          "gold_earned_total": int,
          "items_collected":   int,
          "traps_avoided":     int,
          "fled_combats":      int,
          "kills_by_tag":      {"goblin": 3, "undead": 1, "boss": 0, ...},
        }
        """
        if quest_data is None:
            quest_data = {}

        self.active:    list[str] = quest_data.get("active", [])
        self.completed: list[str] = quest_data.get("completed", [])
        self.progress:  dict      = quest_data.get("progress", {})

        self.gold_earned_total: int  = quest_data.get("gold_earned_total", 0)
        self.items_collected:   int  = quest_data.get("items_collected", 0)
        self.traps_avoided:     int  = quest_data.get("traps_avoided", 0)
        self.fled_combats:      int  = quest_data.get("fled_combats", 0)
        self.kills_by_tag:      dict = quest_data.get("kills_by_tag", {})

        for key in ALL_QUESTS:
            if key not in self.completed and key not in self.active:
                self.active.append(key)


    def on_enemy_killed(self, enemy) -> list[str]:
        """Call after every combat victory. Returns completion messages."""
        messages = []

        tags = set()
        name_lower = enemy.name.lower()
        for tag in ("goblin", "orc", "skeleton", "zombie", "vampire",
                    "demon", "dragon", "witch", "rat"):
            if tag in name_lower:
                tags.add(tag)
        if enemy.is_undead:
            tags.add("undead")
        if enemy.is_boss:
            tags.add("boss")

        for tag in tags:
            self.kills_by_tag[tag] = self.kills_by_tag.get(tag, 0) + 1

        messages += self._check_all()
        return messages

    def on_floor_cleared(self, floors_cleared: int) -> list[str]:
        return self._check_all()

    def on_gold_earned(self, amount: int) -> list[str]:
        self.gold_earned_total += amount
        return self._check_all()

    def on_item_collected(self) -> list[str]:
        self.items_collected += 1
        return self._check_all()

    def on_trap_avoided(self) -> list[str]:
        self.traps_avoided += 1
        return self._check_all()

    def on_fled_combat(self) -> list[str]:
        self.fled_combats += 1
        return self._check_all()

    def on_level_up(self, level: int) -> list[str]:
        return self._check_all()


    def _get_progress(self, quest: Quest, player_kills: int, player_floors: int,
                      player_level: int) -> int:
        """Return current progress value for a quest."""
        ct = quest.condition_type
        if ct == "kills":
            return player_kills
        elif ct == "kills_type":
            return self.kills_by_tag.get(quest.condition_tag, 0)
        elif ct == "floors":
            return player_floors
        elif ct == "level":
            return player_level
        elif ct == "gold_total":
            return self.gold_earned_total
        elif ct == "items_collected":
            return self.items_collected
        elif ct == "traps_avoided":
            return self.traps_avoided
        elif ct == "fled_combats":
            return self.fled_combats
        return 0

    def _check_all(self, player_kills: int = 0, player_floors: int = 0,
                   player_level: int = 0) -> list[str]:
        """Check all active quests for completion. Returns notification messages."""
        messages = []
        newly_completed = []

        for key in list(self.active):
            quest = ALL_QUESTS.get(key)
            if not quest:
                continue
            current = self._get_progress(quest, player_kills, player_floors, player_level)
            if current >= quest.condition_target:
                newly_completed.append(key)

        for key in newly_completed:
            self.active.remove(key)
            self.completed.append(key)
            quest = ALL_QUESTS[key]
            messages.append(f"")
            messages.append(f"  *** MISIÓN COMPLETADA: {quest.name} ***")
            messages.append(f"  {quest.flavor}")
            if quest.reward_gold > 0:
                messages.append(f"  Recompensa: {quest.reward_gold} oro + {quest.reward_xp} XP")
            if quest.reward_item:
                messages.append(f"  Objeto: {quest.reward_item}")

        return messages

    def complete_quest_and_reward(self, key: str, player) -> list[str]:
        """Apply rewards for a completed quest. Call after _check_all detects completion."""
        quest = ALL_QUESTS.get(key)
        if not quest:
            return []
        messages = []
        if quest.reward_gold > 0:
            player.earn_gold(quest.reward_gold)
        if quest.reward_xp > 0:
            msgs = player.gain_xp(quest.reward_xp)
            messages += msgs
        if quest.reward_item:
            from data.items import ALL_ITEMS
            item = ALL_ITEMS.get(quest.reward_item)
            if item:
                ok, msg = player.add_to_inventory(item)
                if ok:
                    messages.append(f"  Recibís: {item.name}")
        return messages

    def check_and_reward(self, player, player_kills=0, player_floors=0,
                         player_level=0) -> list[str]:
        """Full check + reward cycle. Returns all messages."""
        notifications = self._check_all(player_kills, player_floors, player_level)
        reward_msgs = []
        for key in list(self.completed):
            if key not in getattr(self, "_rewarded", set()):
                if not hasattr(self, "_rewarded"):
                    self._rewarded = set()
                self._rewarded.add(key)
                reward_msgs += self.complete_quest_and_reward(key, player)
        return notifications + reward_msgs


    def to_dict(self) -> dict:
        return {
            "active":            self.active,
            "completed":         self.completed,
            "progress":          self.progress,
            "gold_earned_total": self.gold_earned_total,
            "items_collected":   self.items_collected,
            "traps_avoided":     self.traps_avoided,
            "fled_combats":      self.fled_combats,
            "kills_by_tag":      self.kills_by_tag,
            "rewarded":          list(getattr(self, "_rewarded", set())),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "QuestManager":
        qm = cls(data)
        qm._rewarded = set(data.get("rewarded", []))
        return qm


def show_quests(player) -> None:
    """Display the quest log screen."""
    qm: QuestManager = player.quest_manager

    print()
    print(box_top())
    print(box_row(clr("REGISTRO DE MISIONES", Color.YELLOW), align="center"))
    print(box_separator())
    print(box_row(f"  Completadas: {clr(str(len(qm.completed)), Color.GREEN)}  |  "
                  f"Activas: {clr(str(len(qm.active)), Color.CYAN)}"))
    print(box_separator())

    print(box_row(clr("  EN CURSO:", Color.CYAN)))
    active_shown = 0
    for key in qm.active[:8]:
        quest = ALL_QUESTS.get(key)
        if not quest:
            continue
        current = qm._get_progress(
            quest,
            player_kills=player.kills,
            player_floors=player.floors_cleared,
            player_level=player.level,
        )
        pct = min(current, quest.condition_target)
        bar_len = 12
        filled = int((pct / quest.condition_target) * bar_len)
        bar = clr("█" * filled, Color.CYAN) + clr("░" * (bar_len - filled), Color.GREY)
        print(box_row(f"  * {quest.name}"))
        print(box_row(f"    {quest.description}"))
        print(box_row(f"    [{bar}] {pct}/{quest.condition_target}  "
                      f"Recomp: {clr(str(quest.reward_gold)+'g', Color.YELLOW)} "
                      f"+ {quest.reward_xp}XP"))
        active_shown += 1

    if active_shown == 0:
        print(box_row(clr("  No hay misiones activas. Bastante raro.", Color.GREY)))

    print(box_separator())

    print(box_row(clr("  COMPLETADAS:", Color.GREEN)))
    recent = qm.completed[-5:]
    if recent:
        for key in reversed(recent):
            quest = ALL_QUESTS.get(key)
            if quest:
                print(box_row(f"  {clr(chr(10003), Color.GREEN)} {quest.name}"))
    else:
        print(box_row(clr("  Ninguna todavía. A trabajar.", Color.GREY)))

    print(box_bottom())
    press_enter()
