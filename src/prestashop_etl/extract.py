from typing import Dict, Iterable, List

import requests


def _get_json(url: str, api_key: str) -> Dict:
    response = requests.get(url, auth=(api_key, ""), timeout=60)
    response.raise_for_status()
    return response.json()


def fetch_orders(base_url: str, api_key: str, start_date: str, end_date: str) -> List[Dict]:
    orders_url = (
        f"{base_url}/orders?filter[invoice_date]=[{start_date},{end_date}]"
        "&display=full&output_format=JSON"
    )
    data = _get_json(orders_url, api_key)
    return data.get("orders", [])


def fetch_entities_by_ids(base_url: str, api_key: str, entity: str, ids: Iterable[int], batch_size: int = 100) -> List[Dict]:
    id_list = sorted(set(int(x) for x in ids))
    if not id_list:
        return []

    rows: List[Dict] = []
    for i in range(0, len(id_list), batch_size):
        batch = id_list[i : i + batch_size]
        id_filter = "[" + "|".join(str(v) for v in batch) + "]"
        url = f"{base_url}/{entity}?filter[id]={id_filter}&display=full&output_format=JSON"
        data = _get_json(url, api_key)
        rows.extend(data.get(entity, []))

    return rows
