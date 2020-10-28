from get_data import *
from ml_utils import *
import sqlite3 as sql

buscas = {"12": "Etios+Hatch", "19": "HB20", "5": "Fiesta+Hatch", "5": "Ka", "15": "C3", "3": "Up!", "3": "Fox", "3": "Polo+Hatch"}
db_name = 'infos.db'

def update_db():
    with sql.connect(db_name) as conn:
        for key, value in buscas.items():
            for page in range(1,8):
                search_page = download_search_page(key, value, page)
                links_list = parse_search_page(search_page)

                for item in links_list:
                    ad_page = download_ad_page(item["link"])
                    ad_json_data = parse_ad_page(ad_page)
                    ad_json_data["modelo"] =  item['modelo']

                    p = compute_prediction(ad_json_data)

                    data_front = {"modelo": ad_json_data["form_modelo"], "score": float(p), "link": item["link"]}

                    c = conn.cursor()
                    c.execute("INSERT INTO infos VALUES ('{modelo}', '{link}', {score})".format(**data_front))
                    conn.commit()
    return True