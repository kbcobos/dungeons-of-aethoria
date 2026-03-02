from dataclasses import dataclass, field
from typing import Optional
from utils.display import (
    box_top, box_bottom, box_row, box_separator,
    print_message, prompt_choice, press_enter, clr, Color
)


@dataclass
class SkillNode:
    key: str
    class_key: str
    name: str
    description: str
    narrative: str
    level_required: int
    prerequisite: Optional[str]
    mp_cost: int = 0
    damage_base: int = 0
    damage_scale: float = 1.0
    stat_used: str = "str"
    heal_amount: int = 0
    effect: str = ""
    cooldown: int = 0
    tier: int = 2


ALL_SKILLS: dict[str, SkillNode] = {}

def _s(skill: SkillNode):
    ALL_SKILLS[skill.key] = skill


_s(SkillNode("guerrero_grito", "guerrero",
    "Grito de Guerra", "Intimida al enemigo reduciendo su ataque por 2 turnos.",
    "{name} lets out a battle cry that shakes the very walls, rattling their foe's resolve!",
    level_required=4, prerequisite=None, mp_cost=6, effect="weaken", tier=2))

_s(SkillNode("guerrero_escudo", "guerrero",
    "Postura Defensiva", "Adopta una postura que reduce el daño recibido a la mitad por 1 turno.",
    "{name} plants their feet and raises their guard — an impenetrable wall of steel and will!",
    level_required=7, prerequisite="guerrero_grito", mp_cost=10, effect="shield", heal_amount=0, tier=2))

_s(SkillNode("guerrero_ejecucion", "guerrero",
    "Ejecución", "Golpe masivo que hace el doble de daño si el enemigo tiene menos del 30% de HP.",
    "{name} seizes the moment — a final, merciless strike aimed directly at the killing blow!",
    level_required=12, prerequisite="guerrero_escudo", mp_cost=15,
    damage_base=40, damage_scale=2.5, stat_used="str", effect="execute", tier=3))

_s(SkillNode("mago_tormenta", "mago",
    "Tormenta de Hielo", "Ralentiza al enemigo y hace daño continuo por 3 turnos.",
    "{name} summons a localized blizzard — freezing winds tear at their foe from all directions!",
    level_required=4, prerequisite=None, mp_cost=18,
    damage_base=15, damage_scale=1.4, stat_used="int", effect="freeze", tier=2))

_s(SkillNode("mago_mana", "mago",
    "Absorción de Maná", "Drena el MP del enemigo y lo convierte en daño.",
    "{name} reaches into the magical aether and tears the energy from their foe's very essence!",
    level_required=7, prerequisite="mago_tormenta", mp_cost=10,
    damage_base=20, damage_scale=1.6, stat_used="int", effect="drain", tier=2))

_s(SkillNode("mago_meteor", "mago",
    "Lluvia de Meteoros", "Invoca meteoros que caen sobre el enemigo. Daño masivo.",
    "{name} tears open the sky itself — burning rocks streak down in a cataclysmic barrage!",
    level_required=13, prerequisite="mago_mana", mp_cost=35,
    damage_base=55, damage_scale=3.0, stat_used="int", cooldown=3, tier=3))

_s(SkillNode("picaro_cegar", "picaro",
    "Arena en los Ojos", "Ciega al enemigo, haciéndole fallar su próximo ataque.",
    "{name} throws a fistful of grit directly into their foe's face. Not elegant, but effective.",
    level_required=4, prerequisite=None, mp_cost=5, effect="stun", tier=2))

_s(SkillNode("picaro_robo", "picaro",
    "Robo Rápido", "Roba entre 20 y 80 monedas de oro al enemigo durante el combate.",
    "{name}'s hand moves faster than thought — gold vanishes from the enemy's purse before they blink.",
    level_required=6, prerequisite="picaro_cegar", mp_cost=4, effect="steal", tier=2))

_s(SkillNode("picaro_muerte", "picaro",
    "Golpe Letal", "Si el enemigo está envenenado, este ataque hace x3 de daño.",
    "{name} waits for the poison to do its work — then drives home the blade with lethal precision!",
    level_required=11, prerequisite="picaro_robo", mp_cost=12,
    damage_base=30, damage_scale=2.0, stat_used="dex", effect="lethal", tier=3))

_s(SkillNode("paladin_resurreccion", "paladin",
    "Voluntad de Acero", "Cuando tu HP baja de 20, te recuperas automáticamente con 50 HP (1 vez por combate).",
    "{name} refuses to fall — divine light floods their wounds, defying death with sheer conviction!",
    level_required=5, prerequisite=None, mp_cost=0, effect="revive", tier=2))

_s(SkillNode("paladin_sagrado", "paladin",
    "Toque Sagrado", "Cura 60 HP y elimina todos los efectos negativos.",
    "{name} channels pure holy energy through their hands — wounds close, curses shatter, pain fades.",
    level_required=8, prerequisite="paladin_resurreccion", mp_cost=20, heal_amount=60, effect="cleanse", tier=2))

_s(SkillNode("paladin_juicio", "paladin",
    "Juicio Divino", "Daño masivo sagrado. Extra efectivo contra no-muertos y demonios.",
    "{name} calls down divine judgement — a column of blinding light obliterates the unholy!",
    level_required=14, prerequisite="paladin_sagrado", mp_cost=28,
    damage_base=45, damage_scale=2.2, stat_used="cha", effect="holy", cooldown=2, tier=3))

_s(SkillNode("arquero_lluvia", "arquero",
    "Lluvia de Flechas", "Lanza 5 flechas simultáneas con daño total masivo.",
    "{name} nocks five arrows at once — the air hisses as they arc toward their target in a deadly fan!",
    level_required=4, prerequisite=None, mp_cost=12,
    damage_base=8, damage_scale=1.2, stat_used="dex", effect="multi", tier=2))

_s(SkillNode("arquero_ojo", "arquero",
    "Ojo de Águila", "El próximo ataque es un crítico garantizado.",
    "{name} narrows their eyes, steadies their breath, and lines up the perfect shot...",
    level_required=7, prerequisite="arquero_lluvia", mp_cost=8, effect="guaranteed_crit", tier=2))

_s(SkillNode("arquero_flecha_muerte", "arquero",
    "Flecha de la Muerte", "Una flecha que ignora completamente la armadura del enemigo.",
    "{name} draws a pitch-black arrow — its tip glows briefly before punching through all resistance!",
    level_required=12, prerequisite="arquero_ojo", mp_cost=20,
    damage_base=50, damage_scale=2.0, stat_used="dex", effect="armor_pierce", tier=3))

_s(SkillNode("barbaro_berserker", "barbaro",
    "Modo Berserker", "Mientras HP < 50%, tus ataques hacen +80% de daño.",
    "{name}'s wounds only fuel the fire. Blood-rage transforms desperation into devastating power!",
    level_required=4, prerequisite=None, mp_cost=0, effect="berserker", tier=2))

_s(SkillNode("barbaro_salto", "barbaro",
    "Salto Aplastante", "Salta sobre el enemigo causando daño masivo y aturdimiento.",
    "{name} leaps into the air with impossible height and comes crashing down like a falling boulder!",
    level_required=7, prerequisite="barbaro_berserker", mp_cost=10,
    damage_base=35, damage_scale=2.2, stat_used="str", effect="stun", tier=2))

_s(SkillNode("barbaro_inmortal", "barbaro",
    "No Puedo Morir", "Durante 2 turnos, no podés morir. Tu HP no baja de 1.",
    "{name} roars at death itself — and death, for once, blinks first.",
    level_required=15, prerequisite="barbaro_salto", mp_cost=20, effect="immortal", cooldown=5, tier=3))

_s(SkillNode("monje_meditacion", "monje",
    "Meditación de Combate", "Recupera 20 HP y 20 MP por turno durante 2 turnos.",
    "{name} closes their eyes amid the chaos — a pocket of absolute stillness in the storm of battle.",
    level_required=4, prerequisite=None, mp_cost=8, heal_amount=20, effect="regen", tier=2))

_s(SkillNode("monje_chakra", "monje",
    "Golpe de Chakra", "Golpe de energía pura que ignora la mitad de la defensa enemiga.",
    "{name} channels chi directly into their strike — raw life energy detonates on impact!",
    level_required=7, prerequisite="monje_meditacion", mp_cost=14,
    damage_base=25, damage_scale=1.8, stat_used="wis", effect="armor_pierce", tier=2))

_s(SkillNode("monje_tormenta", "monje",
    "Tormenta de Golpes", "Ataca 8 veces seguidas. Cada golpe hace poco daño pero juntos devastan.",
    "{name} becomes a blur — eight perfectly timed strikes delivered in the span of a single breath!",
    level_required=13, prerequisite="monje_chakra", mp_cost=22,
    damage_base=6, damage_scale=1.0, stat_used="dex", effect="multi", cooldown=2, tier=3))

_s(SkillNode("explorador_sigilo", "explorador",
    "Ataque desde las Sombras", "Desaparece y ataca desde la oscuridad con daño doble.",
    "{name} steps into shadow and vanishes — reappearing an instant later in a devastating ambush!",
    level_required=4, prerequisite=None, mp_cost=10,
    damage_base=22, damage_scale=1.9, stat_used="dex", effect="ambush", tier=2))

_s(SkillNode("explorador_trampa_mortal", "explorador",
    "Trampa Mortal", "Coloca una trampa que hace daño masivo al primer ataque del enemigo.",
    "{name} sets a killing trap with practiced efficiency — the enemy won't see it until it's too late.",
    level_required=7, prerequisite="explorador_sigilo", mp_cost=12,
    damage_base=30, damage_scale=1.5, stat_used="wis", effect="counter_trap", tier=2))

_s(SkillNode("explorador_punto_debil", "explorador",
    "Punto Débil Crítico", "Analiza al enemigo para que todos tus ataques sean críticos por 3 turnos.",
    "{name} studies every twitch, every gap — and then exploits them all simultaneously.",
    level_required=11, prerequisite="explorador_trampa_mortal", mp_cost=18,
    effect="guaranteed_crit", cooldown=4, tier=3))

_s(SkillNode("hechicero_surje", "hechicero",
    "Oleada de Poder", "Gasta todo el MP restante para un ataque masivo.",
    "{name} opens the floodgates — every last drop of magical energy detonates outward in a nova!",
    level_required=5, prerequisite=None, mp_cost=0,
    damage_base=0, damage_scale=3.0, stat_used="int", effect="mana_burst", tier=2))

_s(SkillNode("hechicero_doble", "hechicero",
    "Hechizo Doble", "Lanza el mismo hechizo dos veces en un turno.",
    "{name}'s fingers trace two sigils simultaneously — the spell detonates twice in rapid succession!",
    level_required=8, prerequisite="hechicero_surje", mp_cost=15, effect="double_cast", tier=2))

_s(SkillNode("hechicero_singularidad", "hechicero",
    "Singularidad Arcana", "Crea un punto de colapso mágico. El mayor daño del juego.",
    "{name} tears a hole in reality — a point of infinite magical density implodes on their foe!",
    level_required=15, prerequisite="hechicero_doble", mp_cost=50,
    damage_base=80, damage_scale=4.0, stat_used="int", cooldown=4, tier=3))

_s(SkillNode("brujo_pacto", "brujo",
    "Pacto de Sangre", "Sacrifica 30 HP para que el próximo ataque haga daño doble.",
    "{name} cuts their palm with a ritual knife — dark power floods into the blade in exchange.",
    level_required=4, prerequisite=None, mp_cost=5, effect="blood_pact", tier=2))

_s(SkillNode("brujo_tentaculos", "brujo",
    "Tentáculos del Vacío", "Invoca tentáculos que paralizan y drenan vida del enemigo.",
    "{name} speaks a word that shouldn't exist — tendrils of void emerge to clutch and drain!",
    level_required=8, prerequisite="brujo_pacto", mp_cost=20,
    damage_base=18, damage_scale=1.8, stat_used="cha", effect="drain", cooldown=2, tier=2))

_s(SkillNode("brujo_apocalipsis", "brujo",
    "Maldición del Apocalipsis", "La maldición más poderosa: el enemigo pierde el 40% de su HP máximo.",
    "{name} speaks the final syllable of the most forbidden incantation — reality weeps.",
    level_required=16, prerequisite="brujo_tentaculos", mp_cost=40,
    damage_base=0, damage_scale=0, stat_used="cha", effect="apocalypse", cooldown=5, tier=3))


def get_class_skills(class_key: str) -> list[SkillNode]:
    """Return all skill nodes for a given class."""
    return [s for s in ALL_SKILLS.values() if s.class_key == class_key]


def get_available_to_unlock(class_key: str, unlocked: list[str], player_level: int) -> list[SkillNode]:
    """Return skills the player can unlock right now."""
    result = []
    for skill in get_class_skills(class_key):
        if skill.key in unlocked:
            continue
        if player_level < skill.level_required:
            continue
        if skill.prerequisite and skill.prerequisite not in unlocked:
            continue
        result.append(skill)
    return result


def skill_to_ability(skill: SkillNode):
    """Convert a SkillNode to an Ability object for use in combat."""
    from data.classes import Ability
    return Ability(
        name=skill.name,
        description=skill.description,
        narrative=skill.narrative,
        mp_cost=skill.mp_cost,
        damage_base=skill.damage_base,
        damage_scale=skill.damage_scale,
        stat_used=skill.stat_used,
        heal_amount=skill.heal_amount,
        effect=skill.effect,
        cooldown=skill.cooldown,
    )


def show_skill_tree(player) -> None:
    """Display and interact with the skill tree."""
    while True:
        class_key = player.char_class.key
        unlocked  = player.unlocked_skills
        all_class_skills = get_class_skills(class_key)
        available = get_available_to_unlock(class_key, unlocked, player.level)

        _draw_skill_tree(player, all_class_skills, unlocked, available)

        if not available:
            press_enter("  [ No hay habilidades para desbloquear ahora. Subí de nivel. ]")
            return

        options = [f"{s.name}  [Nivel {s.level_required}]" for s in available]
        options.append("-- Volver --")

        choice = prompt_choice(options, "¿Qué habilidad desbloqueás?")
        if choice == len(options) - 1:
            return

        skill = available[choice]
        _unlock_skill(player, skill)


def _draw_skill_tree(player, all_skills: list, unlocked: list, available: list):
    """Render the skill tree panel."""
    print()
    print(box_top())
    print(box_row(clr(f"ÁRBOL DE HABILIDADES — {player.char_class.name.upper()}", Color.YELLOW), align="center"))
    print(box_row(f"  Nivel: {player.level}  |  Habilidades desbloqueadas: {len(unlocked)}", ))
    print(box_separator())

    tier_colors = {1: Color.GREY, 2: Color.CYAN, 3: Color.MAGENTA}

    for skill in sorted(all_skills, key=lambda s: (s.tier, s.level_required)):
        if skill.key in unlocked:
            status = clr("[DESBLOQUEADA]", Color.GREEN)
        elif skill in available:
            status = clr("[DISPONIBLE]", Color.YELLOW)
        else:
            req_str = f"Req: Nivel {skill.level_required}"
            if skill.prerequisite:
                pre = ALL_SKILLS.get(skill.prerequisite)
                if pre:
                    req_str += f" + {pre.name}"
            status = clr(f"[BLOQUEADA — {req_str}]", Color.GREY)

        tier_label = {1: "BASE", 2: "AVANZADA", 3: "ÉLITE"}.get(skill.tier, "")
        tier_str   = clr(f"[{tier_label}]", tier_colors.get(skill.tier, Color.WHITE))

        print(box_row(f"  {clr(skill.name, Color.CYAN):30s}  {tier_str}  {status}"))
        print(box_row(f"    {skill.description}"))
        if skill.mp_cost > 0:
            print(box_row(f"    MP: {skill.mp_cost}  |  Nivel mínimo: {skill.level_required}"))
        print(box_row(""))

    print(box_bottom())


def _unlock_skill(player, skill: SkillNode):
    """Unlock a skill and add it to the player's available abilities."""
    player.unlocked_skills.append(skill.key)

    ability = skill_to_ability(skill)
    player.char_class.abilities.append(ability)

    print()
    print_message(f"¡Desbloqueaste: {clr(skill.name, Color.CYAN)}!", "good")
    print_message(f"  {skill.description}", "system")
    print_message("  La habilidad ya está disponible en combate.", "system")
    press_enter()
