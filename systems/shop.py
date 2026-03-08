import random
from data.items import ALL_ITEMS, Item, WEAPONS, ARMORS, POTIONS
from utils.lang import t, item_desc
from utils.display import (
    box_top, box_bottom, box_row, box_separator,
    print_message, prompt_choice, press_enter, clr, Color
)


def generate_shop_stock(floor: int) -> list[str]:
    """
    Generate a list of item keys for the shop based on current floor.
    Stock improves with floor progress.
    """
    stock = []

    potions = list(POTIONS.keys())
    stock += random.sample(potions, min(3, len(potions)))

    if floor <= 3:
        rarity_pool = ["common"]
    elif floor <= 6:
        rarity_pool = ["common", "common", "uncommon"]
    else:
        rarity_pool = ["uncommon", "rare"]

    weapon_pool = [k for k, v in WEAPONS.items() if v.rarity in rarity_pool]
    if weapon_pool:
        stock += random.sample(weapon_pool, min(2, len(weapon_pool)))

    armor_pool = [k for k, v in ARMORS.items() if v.rarity in rarity_pool]
    if armor_pool:
        stock += random.sample(armor_pool, min(2, len(armor_pool)))

    if floor >= 5 and random.random() < 0.4:
        rare_pool = [k for k, v in ALL_ITEMS.items() if v.rarity in ("rare", "legendary")]
        if rare_pool:
            stock.append(random.choice(rare_pool))

    return list(dict.fromkeys(stock))


def refresh_needed(player) -> bool:
    """Returns True if the shop stock should be refreshed (every 2 floors)."""
    return (player.dungeon_floor - 1) // 2 > player.shop_last_refresh // 2


def show_shop(player) -> None:
    """Display the permanent shop between floors."""

    if not player.shop_stock or refresh_needed(player):
        player.shop_stock = generate_shop_stock(player.dungeon_floor)
        player.shop_last_refresh = player.dungeon_floor
        print_message(t("shop_refreshed"), "system")

    while True:
        _draw_shop(player)
        options = ["Comprar", "Vender", "Salir de la tienda"]
        choice = prompt_choice(options, "¿Qué hacés?")

        if choice == 0:
            _buy(player)
        elif choice == 1:
            _sell(player)
        else:
            break


def _draw_shop(player) -> None:
    """Render the permanent shop UI."""
    print()
    print(box_top())
    print(box_row(clr(t("shop_title"), Color.YELLOW), align="center"))
    print(box_separator())
    print(box_row(clr(t("shop_tagline"), Color.GREY)))
    print(box_separator())
    print(box_row(f"  Tu oro: {clr(str(player.gold), Color.YELLOW)} gp  |  "
                  f"Piso actual: {player.dungeon_floor}"))
    print(box_separator())
    print(box_row(clr(f"  {t('shop_stock_label')}", Color.CYAN)))
    print()

    rarity_colors = {
        "common":    Color.WHITE,
        "uncommon":  Color.GREEN,
        "rare":      Color.CYAN,
        "legendary": Color.YELLOW,
    }

    if not player.shop_stock:
        print(box_row(clr(t("shop_no_stock"), Color.GREY)))
    else:
        for i, key in enumerate(player.shop_stock, 1):
            item = ALL_ITEMS.get(key)
            if not item:
                continue
            price = _buy_price(item)
            rarity_color = rarity_colors.get(item.rarity, Color.WHITE)
            name_str  = clr(f"{item.name}", rarity_color)
            price_str = clr(f"{price}gp", Color.YELLOW)
            type_str  = clr(f"[{item.item_type}]", Color.GREY)
            affordable = "" if player.gold >= price else clr(f"  {t('shop_no_afford')}", Color.RED)
            stats = []
            if item.attack_bonus:  stats.append(f"ATK+{item.attack_bonus}")
            if item.defense_bonus: stats.append(f"DEF+{item.defense_bonus}")
            if item.heal_hp:       stats.append(f"HP+{item.heal_hp}")
            if item.heal_mp:       stats.append(f"MP+{item.heal_mp}")
            if item.str_bonus:     stats.append(f"FUE+{item.str_bonus}")
            if item.dex_bonus:     stats.append(f"DES+{item.dex_bonus}")
            if item.int_bonus:     stats.append(f"INT+{item.int_bonus}")
            stat_str = clr("  " + "  ".join(stats), Color.GREEN) if stats else ""
            short_desc = clr(f"  {item_desc(item)[:40]}", Color.GREY)
            print(box_row(f"  {i:2}. {name_str}  {price_str}{affordable}  {type_str}"))
            print(box_row(f"      {short_desc}{stat_str}"))

    print()
    print(box_bottom())


def _buy(player) -> None:
    """Handle a purchase."""
    stock_items = [ALL_ITEMS.get(k) for k in player.shop_stock if ALL_ITEMS.get(k)]
    if not stock_items:
        print_message(t("shop_no_stock"), "warning")
        press_enter()
        return

    print()
    for i, item in enumerate(stock_items, 1):
        price = _buy_price(item)
        rarity_colors = {"common": Color.WHITE, "uncommon": Color.GREEN,
                         "rare": Color.CYAN, "legendary": Color.YELLOW}
        name_str  = clr(item.name, rarity_colors.get(item.rarity, Color.WHITE))
        price_str = clr(f"{price}gp", Color.YELLOW)
        affordable = "" if player.gold >= price else clr(f" {t('shop_no_afford')}", Color.RED)
        stats = []
        if item.attack_bonus:  stats.append(f"ATK+{item.attack_bonus}")
        if item.defense_bonus: stats.append(f"DEF+{item.defense_bonus}")
        if item.heal_hp:       stats.append(f"HP+{item.heal_hp}")
        if item.heal_mp:       stats.append(f"MP+{item.heal_mp}")
        if item.str_bonus:     stats.append(f"FUE+{item.str_bonus}")
        if item.dex_bonus:     stats.append(f"DES+{item.dex_bonus}")
        if item.int_bonus:     stats.append(f"INT+{item.int_bonus}")
        stat_str = clr("  " + "  ".join(stats), Color.GREEN) if stats else ""
        print(f"  {i}. {name_str}  {price_str}{affordable}")
        print(f"     {clr(item_desc(item)[:55], Color.GREY)}{stat_str}")
    print()

    options = [f"{item.name}  ({_buy_price(item)}gp)" for item in stock_items]
    options.append(t("shop_cancel"))
    choice = prompt_choice(options, t("shop_buy_prompt"))

    if choice == len(options) - 1:
        return

    item  = stock_items[choice]
    price = _buy_price(item)

    if not player.spend_gold(price):
        print_message(t("shop_no_gold"), "warning")
        press_enter()
        return

    ok, msg = player.add_to_inventory(item)
    if ok:
        if item.key in player.shop_stock:
            player.shop_stock.remove(item.key)
        print_message(t("shop_bought", item=clr(item.name, Color.CYAN)), "good")
    else:
        player.earn_gold(price)
        print_message(t("shop_inventory_full"), "warning")

    press_enter()


def _sell(player) -> None:
    """Handle a sale."""
    if not player.inventory:
        print_message(t("shop_nothing_sell"), "warning")
        press_enter()
        return

    options = [f"{item.name}  ({_sell_price(item)}gp)" for item in player.inventory]
    options.append(t("shop_cancel"))
    choice = prompt_choice(options, t("shop_sell_prompt"))

    if choice == len(options) - 1:
        return

    item  = player.inventory[choice]
    price = _sell_price(item)
    player.remove_from_inventory(item)
    player.earn_gold(price)
    print_message(t("shop_sold", item=item.name, price=clr(str(price), Color.YELLOW)), "good")
    press_enter()


def _buy_price(item: Item) -> int:
    """Shop buy price = item value * 1.5, rounded."""
    return max(1, int(item.value * 1.5))


def _sell_price(item: Item) -> int:
    """Sell price = item value * 0.6."""
    return max(1, int(item.value * 0.6))
