from datetime import datetime, timedelta
import random

# --- Dados Fictícios em Memória ---
# Esses dados simulam o que antes vinha do banco PostgreSQL.

# Gerador de IDs simples
_next_id = {"categories": 6, "items": 13, "locations": 6, "movements": 16}

def _new_id(table):
    _next_id[table] += 1
    return _next_id[table] - 1

# Timestamps variados nos últimos 60 dias
_now = datetime.now()
def _days_ago(n):
    return _now - timedelta(days=n)

# --- Categorias ---
_categories = [
    {"id": 1, "nome": "Móveis",       "created_at": _days_ago(55), "updated_at": _days_ago(55)},
    {"id": 2, "nome": "Eletrônicos",   "created_at": _days_ago(50), "updated_at": _days_ago(50)},
    {"id": 3, "nome": "Limpeza",       "created_at": _days_ago(45), "updated_at": _days_ago(45)},
    {"id": 4, "nome": "Escritório",    "created_at": _days_ago(40), "updated_at": _days_ago(40)},
    {"id": 5, "nome": "Cozinha",       "created_at": _days_ago(35), "updated_at": _days_ago(35)},
]

# --- Itens ---
_items = [
    {"id": 1,  "nome": "Cadeira Escritório",    "categoria": "Móveis",       "category_id": 1, "quantidade_minima": 5,  "ativo": True, "created_at": _days_ago(50), "updated_at": _days_ago(10)},
    {"id": 2,  "nome": "Colchão Solteiro",      "categoria": "Móveis",       "category_id": 1, "quantidade_minima": 3,  "ativo": True, "created_at": _days_ago(50), "updated_at": _days_ago(8)},
    {"id": 3,  "nome": "Mesa de Jantar",         "categoria": "Móveis",       "category_id": 1, "quantidade_minima": 2,  "ativo": True, "created_at": _days_ago(48), "updated_at": _days_ago(15)},
    {"id": 4,  "nome": "Monitor 24\"",           "categoria": "Eletrônicos",  "category_id": 2, "quantidade_minima": 2,  "ativo": True, "created_at": _days_ago(45), "updated_at": _days_ago(5)},
    {"id": 5,  "nome": "Notebook Dell",          "categoria": "Eletrônicos",  "category_id": 2, "quantidade_minima": 3,  "ativo": True, "created_at": _days_ago(44), "updated_at": _days_ago(3)},
    {"id": 6,  "nome": "Televisor 50\"",         "categoria": "Eletrônicos",  "category_id": 2, "quantidade_minima": 1,  "ativo": True, "created_at": _days_ago(40), "updated_at": _days_ago(12)},
    {"id": 7,  "nome": "Detergente 5L",          "categoria": "Limpeza",      "category_id": 3, "quantidade_minima": 10, "ativo": True, "created_at": _days_ago(38), "updated_at": _days_ago(2)},
    {"id": 8,  "nome": "Vassoura",               "categoria": "Limpeza",      "category_id": 3, "quantidade_minima": 4,  "ativo": True, "created_at": _days_ago(37), "updated_at": _days_ago(7)},
    {"id": 9,  "nome": "Resma de Papel A4",      "categoria": "Escritório",   "category_id": 4, "quantidade_minima": 8,  "ativo": True, "created_at": _days_ago(35), "updated_at": _days_ago(1)},
    {"id": 10, "nome": "Caneta Esferográfica",   "categoria": "Escritório",   "category_id": 4, "quantidade_minima": 20, "ativo": True, "created_at": _days_ago(34), "updated_at": _days_ago(4)},
    {"id": 11, "nome": "Micro-ondas",            "categoria": "Cozinha",      "category_id": 5, "quantidade_minima": 2,  "ativo": True, "created_at": _days_ago(30), "updated_at": _days_ago(6)},
    {"id": 12, "nome": "Jogo de Talheres",       "categoria": "Cozinha",      "category_id": 5, "quantidade_minima": 5,  "ativo": True, "created_at": _days_ago(28), "updated_at": _days_ago(9)},
]

# --- Locais (1 Inventário Geral + 4 Apartamentos) ---
_locations = [
    {"id": 1, "nome": "Inventário Geral", "tipo": "GERAL",        "status_ocupacao": "DISPONIVEL", "ativo": True, "created_at": _days_ago(55), "updated_at": _days_ago(55)},
    {"id": 2, "nome": "Apartamento 101",  "tipo": "APARTAMENTO",  "status_ocupacao": "OCUPADO",    "ativo": True, "created_at": _days_ago(50), "updated_at": _days_ago(10)},
    {"id": 3, "nome": "Apartamento 202",  "tipo": "APARTAMENTO",  "status_ocupacao": "DISPONIVEL", "ativo": True, "created_at": _days_ago(50), "updated_at": _days_ago(20)},
    {"id": 4, "nome": "Apartamento 303",  "tipo": "APARTAMENTO",  "status_ocupacao": "OCUPADO",    "ativo": True, "created_at": _days_ago(45), "updated_at": _days_ago(5)},
    {"id": 5, "nome": "Apartamento 404",  "tipo": "APARTAMENTO",  "status_ocupacao": "DISPONIVEL", "ativo": False,"created_at": _days_ago(40), "updated_at": _days_ago(15)},
]

# --- Movimentações ---
_movements = [
    {"id": 1,  "item_id": 1,  "origem_id": None, "destino_id": 1, "quantidade": 10, "tipo": "Compra",        "observacao": "Lote inicial de cadeiras",      "created_at": _days_ago(45), "updated_at": _days_ago(45)},
    {"id": 2,  "item_id": 2,  "origem_id": None, "destino_id": 1, "quantidade": 8,  "tipo": "Compra",        "observacao": "Colchões novos",                "created_at": _days_ago(44), "updated_at": _days_ago(44)},
    {"id": 3,  "item_id": 4,  "origem_id": None, "destino_id": 1, "quantidade": 6,  "tipo": "Compra",        "observacao": "Monitores para escritório",      "created_at": _days_ago(40), "updated_at": _days_ago(40)},
    {"id": 4,  "item_id": 5,  "origem_id": None, "destino_id": 1, "quantidade": 5,  "tipo": "Compra",        "observacao": "Notebooks corporativos",        "created_at": _days_ago(38), "updated_at": _days_ago(38)},
    {"id": 5,  "item_id": 7,  "origem_id": None, "destino_id": 1, "quantidade": 15, "tipo": "Compra",        "observacao": "Estoque de limpeza",            "created_at": _days_ago(35), "updated_at": _days_ago(35)},
    {"id": 6,  "item_id": 9,  "origem_id": None, "destino_id": 1, "quantidade": 20, "tipo": "Compra",        "observacao": "Resmas de papel",               "created_at": _days_ago(33), "updated_at": _days_ago(33)},
    {"id": 7,  "item_id": 11, "origem_id": None, "destino_id": 1, "quantidade": 4,  "tipo": "Compra",        "observacao": "Micro-ondas para apts",         "created_at": _days_ago(30), "updated_at": _days_ago(30)},
    {"id": 8,  "item_id": 1,  "origem_id": 1,    "destino_id": 2, "quantidade": 3,  "tipo": "Transferência", "observacao": "Cadeiras para apt 101",         "created_at": _days_ago(25), "updated_at": _days_ago(25)},
    {"id": 9,  "item_id": 4,  "origem_id": 1,    "destino_id": 2, "quantidade": 2,  "tipo": "Transferência", "observacao": "Monitores para apt 101",        "created_at": _days_ago(20), "updated_at": _days_ago(20)},
    {"id": 10, "item_id": 5,  "origem_id": 1,    "destino_id": 4, "quantidade": 2,  "tipo": "Transferência", "observacao": "Notebooks para apt 303",        "created_at": _days_ago(15), "updated_at": _days_ago(15)},
    {"id": 11, "item_id": 7,  "origem_id": 1,    "destino_id": 3, "quantidade": 5,  "tipo": "Transferência", "observacao": "Limpeza para apt 202",          "created_at": _days_ago(12), "updated_at": _days_ago(12)},
    {"id": 12, "item_id": 11, "origem_id": 1,    "destino_id": 4, "quantidade": 1,  "tipo": "Transferência", "observacao": "Micro-ondas para apt 303",      "created_at": _days_ago(10), "updated_at": _days_ago(10)},
    {"id": 13, "item_id": 9,  "origem_id": 1,    "destino_id": 2, "quantidade": 5,  "tipo": "Transferência", "observacao": "Papel para apt 101",            "created_at": _days_ago(7),  "updated_at": _days_ago(7)},
    {"id": 14, "item_id": 1,  "origem_id": 2,    "destino_id": 1, "quantidade": 1,  "tipo": "Devolução",     "observacao": "Cadeira com defeito devolvida", "created_at": _days_ago(3),  "updated_at": _days_ago(3)},
    {"id": 15, "item_id": 7,  "origem_id": 1,    "destino_id": None,"quantidade": 2, "tipo": "Perda",        "observacao": "Detergente danificado",         "created_at": _days_ago(1),  "updated_at": _days_ago(1)},
]



connection_error = None  

def init_db():
    """Não faz nada - dados já estão carregados em memória."""
    pass

def reset_connection():
    """Não faz nada - sem conexão para resetar."""
    pass

# --- Leitura ---

def get_items(limit=None, offset=None, filters=None):
    results = [i for i in _items if i["ativo"]]

    if filters:
        if filters.get("search"):
            s = filters["search"].lower()
            results = [i for i in results if s in i["nome"].lower() or s in (i.get("categoria") or "").lower()]

        if filters.get("categoria") and filters["categoria"] != "Todas":
            results = [i for i in results if i.get("categoria") == filters["categoria"]]

    results.sort(key=lambda x: x["nome"].lower())

    if offset is not None:
        results = results[offset:]
    if limit is not None:
        results = results[:limit]

    return results

def get_critical_items(limit=10):
    """Retorna itens cujo saldo no Inventário Geral (id=1) está abaixo do mínimo."""
    critical = []
    for item in _items:
        if not item["ativo"]:
            continue
        balance = get_balance(item["id"], 1)
        if balance <= item["quantidade_minima"]:
            critical.append({
                "id": item["id"],
                "nome": item["nome"],
                "min": item["quantidade_minima"],
                "balance": balance,
            })
    # Ordena pela diferença (mais crítico primeiro)
    critical.sort(key=lambda x: x["min"] - x["balance"], reverse=True)
    return critical[:limit]

def get_total_critical_count():
    """Conta quantos itens estão abaixo do mínimo."""
    return len(get_critical_items(limit=9999))

def get_locations():
    return list(_locations)

def get_movements(limit=None, offset=None, filters=None):
    results = list(_movements)

    if filters:
        if filters.get("tipo") and filters["tipo"] != "Todos":
            results = [m for m in results if m["tipo"] == filters["tipo"]]

        if filters.get("item_id") and str(filters["item_id"]) != "0":
            item_id = int(filters["item_id"])
            results = [m for m in results if m["item_id"] == item_id]

        if filters.get("apt_id") and str(filters["apt_id"]) != "0":
            apt_id = int(filters["apt_id"])
            results = [m for m in results if m.get("origem_id") == apt_id or m.get("destino_id") == apt_id]

        if filters.get("date_start"):
            ds = filters["date_start"]
            if isinstance(ds, str):
                ds = datetime.fromisoformat(ds)
            results = [m for m in results if m["created_at"] >= ds]

        if filters.get("date_end"):
            de = filters["date_end"]
            if isinstance(de, str):
                de = datetime.fromisoformat(de)
            results = [m for m in results if m["created_at"] <= de]

    results.sort(key=lambda x: x["created_at"], reverse=True)

    if offset is not None:
        results = results[offset:]
    if limit is not None:
        results = results[:limit]

    return results

def get_categories():
    cats = sorted(_categories, key=lambda c: c["nome"])
    return list(cats)

# --- Escrita: Categorias ---

def add_category(nome):
    cat = {"id": _new_id("categories"), "nome": nome, "created_at": datetime.now(), "updated_at": datetime.now()}
    _categories.append(cat)

def update_category(cat_id, nome):
    for cat in _categories:
        if cat["id"] == cat_id:
            cat["nome"] = nome
            cat["updated_at"] = datetime.now()
            # Atualiza o texto da categoria nos itens também
            for item in _items:
                if item["category_id"] == cat_id:
                    item["categoria"] = nome
            break

def delete_category(cat_id):
    global _categories
    _categories = [c for c in _categories if c["id"] != cat_id]
    # Limpa referência nos itens
    for item in _items:
        if item["category_id"] == cat_id:
            item["category_id"] = None
            item["categoria"] = None

def get_item_category_name(item):
    if item.get("category_id"):
        for cat in _categories:
            if cat["id"] == item["category_id"]:
                return cat["nome"]
    return item.get("categoria") or "Geral"

# --- Escrita: Itens ---

def add_item(nome, category_id, quantidade_minima):
    cat_nome = None
    for c in _categories:
        if c["id"] == category_id:
            cat_nome = c["nome"]
            break
    item = {
        "id": _new_id("items"),
        "nome": nome,
        "categoria": cat_nome,
        "category_id": category_id,
        "quantidade_minima": quantidade_minima,
        "ativo": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    _items.append(item)

def update_item(item_id, nome, category_id, quantidade_minima):
    cat_nome = None
    for c in _categories:
        if c["id"] == category_id:
            cat_nome = c["nome"]
            break
    for item in _items:
        if item["id"] == item_id:
            item["nome"] = nome
            item["category_id"] = category_id
            item["categoria"] = cat_nome
            item["quantidade_minima"] = quantidade_minima
            item["updated_at"] = datetime.now()
            break

def toggle_item_active(item_id):
    for item in _items:
        if item["id"] == item_id:
            item["ativo"] = not item["ativo"]
            item["updated_at"] = datetime.now()
            break

def item_has_movements(item_id):
    return any(m["item_id"] == item_id for m in _movements)

def get_item_name(item_id):
    if not item_id:
        return "-"
    for item in _items:
        if item["id"] == item_id:
            return item["nome"]
    return "Desconhecido"

def get_location_name(location_id):
    if not location_id:
        return "-"
    for loc in _locations:
        if loc["id"] == location_id:
            return loc["nome"]
    return "Desconhecido"

# --- Escrita: Locais / Apartamentos ---

def add_apartment(nome, status="DISPONIVEL"):
    loc = {
        "id": _new_id("locations"),
        "nome": nome,
        "tipo": "APARTAMENTO",
        "status_ocupacao": status,
        "ativo": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    _locations.append(loc)

def toggle_apartment_status(apt_id):
    for loc in _locations:
        if loc["id"] == apt_id:
            loc["status_ocupacao"] = "OCUPADO" if loc["status_ocupacao"] == "DISPONIVEL" else "DISPONIVEL"
            loc["updated_at"] = datetime.now()
            break

def toggle_apartment_active(apt_id):
    for loc in _locations:
        if loc["id"] == apt_id:
            loc["ativo"] = not loc["ativo"]
            loc["updated_at"] = datetime.now()
            break

# --- Escrita: Movimentações ---

def add_movement(item_id, origem_id, destino_id, quantidade, tipo, observacao=""):
    mov = {
        "id": _new_id("movements"),
        "item_id": item_id,
        "origem_id": origem_id,
        "destino_id": destino_id,
        "quantidade": quantidade,
        "tipo": tipo,
        "observacao": observacao,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    _movements.append(mov)

def update_movement(movement_id, item_id, origem_id, destino_id, quantidade, tipo, observacao=""):
    for mov in _movements:
        if mov["id"] == movement_id:
            mov["item_id"] = item_id
            mov["origem_id"] = origem_id
            mov["destino_id"] = destino_id
            mov["quantidade"] = quantidade
            mov["tipo"] = tipo
            mov["observacao"] = observacao
            mov["updated_at"] = datetime.now()
            break

# --- Cálculos de Saldo ---

def get_balance(item_id, location_id):
    if location_id is None:
        return 0
    total_in = sum(m["quantidade"] for m in _movements if m["item_id"] == item_id and m.get("destino_id") == location_id)
    total_out = sum(m["quantidade"] for m in _movements if m["item_id"] == item_id and m.get("origem_id") == location_id)
    return total_in - total_out

def get_total_balances():
    """Retorna um dict {item_id: saldo_total} para todos os itens."""
    balances = {}
    for item in _items:
        total_in = sum(m["quantidade"] for m in _movements if m["item_id"] == item["id"] and m.get("destino_id") is not None)
        total_out = sum(m["quantidade"] for m in _movements if m["item_id"] == item["id"] and m.get("origem_id") is not None)
        balances[item["id"]] = total_in - total_out
    return balances

# --- Acesso via atributo (compatibilidade) ---

def __getattr__(name):
    if name == "items":
        return get_items()
    if name == "locations":
        return get_locations()
    if name == "movements":
        return get_movements()
    if name == "categories":
        return get_categories()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
