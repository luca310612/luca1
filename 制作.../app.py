import os, uvicorn, csv, uvicorn
import pandas as pd
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
templates = Jinja2Templates(directory="templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    raise FileNotFoundError(f"Static directory not found: {static_dir}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

base_dir = os.path.dirname(__file__)

csv_paths = [
    os.path.join(base_dir, 'csv/fukushima_hos.csv'),    
    os.path.join(base_dir, 'csv/hokkaidou_dent.csv'),
    os.path.join(base_dir, 'csv/yamagata_hos.csv'),
    os.path.join(base_dir, 'csv/yamagata_dent.csv'),
    os.path.join(base_dir, 'csv/miyagi_hos.csv'),
    os.path.join(base_dir, 'csv/miyagi_dent.csv'),
    os.path.join(base_dir, 'csv/iwate_hos.csv'),
    os.path.join(base_dir, 'csv/iwate_dent.csv'),
    os.path.join(base_dir, 'csv/fukushima_hos.csv'),
    os.path.join(base_dir, 'csv/fukushima_dent.csv'),
    os.path.join(base_dir, 'csv/aomori_hos.csv'),
    os.path.join(base_dir, 'csv/aomori_dent.csv'),
]

# ブロックする都道府県のリスト（設定可能）
blocked_prefectures = set()

dfs = []
for path in csv_paths:
    if os.path.exists(path):
        dfs.append(pd.read_csv(path, header=0, skip_blank_lines=True, low_memory=False, dtype=str, on_bad_lines='skip'))
    else:
        print(f"ファイルが見つかりません: {path}")
df = pd.concat(dfs, ignore_index=True)

class Hospital(BaseModel):
    id: int
    name: str
    address: str
    departments: str
    reviews: int

class HospitalCreate(BaseModel):
    name: str
    address: str
    departments: str

def is_prefecture_blocked(address: str, prefecture: str = None) -> bool:
    """都道府県がブロックされているかチェック"""
    if prefecture and prefecture in blocked_prefectures:
        return True
    
    # 住所から都道府県を抽出してチェック
    if address:
        for blocked_pref in blocked_prefectures:
            if blocked_pref in address:
                return True
    
    return False

def filter_by_prefecture(data: List[dict], exclude_blocked: bool = True) -> List[dict]:
    """都道府県フィルタリング"""
    if not exclude_blocked or not blocked_prefectures:
        return data
    
    filtered_data = []
    for item in data:
        prefecture = item.get("prefecture", "")
        address = item.get("address", "")
        
        if not is_prefecture_blocked(address, prefecture):
            filtered_data.append(item)
    
    return filtered_data

def load_hospital_cards(csv_paths, exclude_blocked: bool = True):
    cards = []
    for csv_path in csv_paths:
        if not os.path.exists(csv_path):
            print(f"ファイルが見つかりません: {csv_path}")
            continue 
        df = pd.read_csv(csv_path, dtype=str, on_bad_lines='skip') 

        if list(df.columns)[0].startswith("col"):
            df.columns = ["name", "address", "tel"]  

        df.rename(columns={
            "病院名": "name",
            "住所": "address",
            "診療科": "departments",
            "都道府県": "prefecture",
        }, inplace=True)

        for _, row in df.iterrows():
            if pd.notna(row.get("name")):
                card = {
                    "name": row.get("name", ""),
                    "address": row.get("address", ""),
                    "departments": row.get("established", ""),
                    "prefecture": row.get("prefecture", "")
                }
                
                # 都道府県ブロックチェック
                if exclude_blocked and is_prefecture_blocked(card["address"], card["prefecture"]):
                    continue
                
                cards.append(card)
    return cards

def extract_hospital_info(csv_path, exclude_blocked: bool = True):
    df = pd.read_csv(csv_path, header=0, skip_blank_lines=True, dtype=str)
    hospital_info = []
    for _, row in df.iterrows():
        if pd.notna(row.get("name")):
            hospital = {
                "name": str(row.get("name", "")).strip(),
                "address": str(row.get("address", "")).strip(),
                "departments": [],
                "prefecture": str(row.get("prefecture", "")).strip(),
            }
            
            # 都道府県ブロックチェック
            if exclude_blocked and is_prefecture_blocked(hospital["address"], hospital["prefecture"]):
                continue
            
            for item in row:
                if pd.notna(item) and any(k in str(item) for k in [
                    "内", "外", "整", "小", "呼", "リハ", "精神", "糖尿病", "循環器", "消化器",
                    "脳外", "心外", "皮", "ひ", "産婦", "眼", "耳い", "放", "麻", "歯", "形", "病理"
]):
                    hospital["departments"].append(str(item).strip())
            hospital_info.append(hospital)
    return hospital_info

def create_hospital_cards(csv_path, exclude_blocked: bool = True):
    df = pd.read_csv(csv_path, header=None)

    cards = []
    card_id = 1

    for _, row in df.iterrows():
        if pd.notna(row[2]):
            current_card = {
                "id": card_id,
                "name": str(row[2]).strip(),
                "address": str(row[3]).strip() if pd.notna(row[3]) else "",
                "reviews": 0,
                "departments": "",
                "prefecture": str(row[4]).strip() if len(row) > 4 and pd.notna(row[4]) else "",
            }
            
            # 都道府県ブロックチェック
            if exclude_blocked and is_prefecture_blocked(current_card["address"], current_card["prefecture"]):
                continue
            
            card_id += 1

            for item in row:
                if pd.notna(item) and any(k in str(item) for k in ["内", "外", "整", "小", "呼", "リハ", "精神", "糖尿病", "循環器", "消化器",
        "脳外", "心外", "皮", "ひ", "産婦", "眼", "耳い", "放", "麻", "歯", "形", "病理"
]):
                    current_card["departments"] += " " + str(item).strip()

            cards.append(current_card)

    return cards

def extract_hospital_data(csv_paths, exclude_blocked: bool = True):
    hospital_data = []
    for csv_path in csv_paths:
        df = pd.read_csv(
    csv_path, 
    header=0, 
    skip_blank_lines=True, 
    low_memory=False, 
    dtype=str, 
    on_bad_lines='skip'
)
        df.rename(columns={
            "病院名": "name",
            "住所": "address",
            "診療科": "established",
            "レビューの数": "review",
            "都道府県": "prefecture",
        }, inplace=True)
        
        for _, row in df.iterrows():
            if pd.isna(row.get("name")) or pd.isna(row.get("address")) or pd.isna(row.get("established")):
                continue
            
            hospital = {
                "name": str(row.get("name", "")).strip(),
                "address": str(row.get("address", "")).strip(),
                "departments": str(row.get("established", "")).split(",") if pd.notna(row.get("established")) else [],
                "reviews": int(row.get("review", 0)) if pd.notna(row.get("review")) else 0,
                "prefecture": str(row.get("prefecture", "")).strip(),
            }
            
            # 都道府県ブロックチェック
            if exclude_blocked and is_prefecture_blocked(hospital["address"], hospital["prefecture"]):
                continue
            
            hospital_data.append(hospital)
    return hospital_data

def add_hospital_to_csv(csv_path, name, address, departments):
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        row = [None, None, name, address] + departments
        writer.writerow(row)

# 都道府県ブロック管理のエンドポイント
@app.get("/blocked-prefectures", response_class=JSONResponse)
async def get_blocked_prefectures():
    """ブロックされている都道府県のリストを取得"""
    return {"blocked_prefectures": list(blocked_prefectures)}

@app.post("/block-prefecture")
async def block_prefecture(prefecture: str):
    """都道府県をブロックリストに追加"""
    blocked_prefectures.add(prefecture)
    return {"message": f"都道府県 '{prefecture}' がブロックされました", "blocked_prefectures": list(blocked_prefectures)}

@app.post("/unblock-prefecture")
async def unblock_prefecture(prefecture: str):
    """都道府県をブロックリストから削除"""
    blocked_prefectures.discard(prefecture)
    return {"message": f"都道府県 '{prefecture}' のブロックが解除されました", "blocked_prefectures": list(blocked_prefectures)}

@app.post("/set-blocked-prefectures")
async def set_blocked_prefectures(prefectures: List[str]):
    """ブロックする都道府県のリストを設定"""
    global blocked_prefectures
    blocked_prefectures = set(prefectures)
    return {"message": "ブロックする都道府県が設定されました", "blocked_prefectures": list(blocked_prefectures)}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, exclude_blocked: bool = Query(True, description="ブロックされた都道府県を除外するかどうか")):
    cards = load_hospital_cards(csv_paths, exclude_blocked)
    return templates.TemplateResponse("index.html", {"request": request, "cards": cards})

@app.get("/hospital_cards", response_class=JSONResponse)
async def get_hospital_cards(exclude_blocked: bool = Query(True, description="ブロックされた都道府県を除外するかどうか")):
    cards = load_hospital_cards(csv_paths, exclude_blocked)
    return cards

@app.get("/hospital-info", response_class=JSONResponse)
async def get_hospital_info(exclude_blocked: bool = Query(True, description="ブロックされた都道府県を除外するかどうか")):
    csv_path = [] 
    hospital_info = extract_hospital_info(csv_path, exclude_blocked)
    return hospital_info

@app.get("/hospital-cards", response_class=JSONResponse)
async def get_hospital_cards_alt(exclude_blocked: bool = Query(True, description="ブロックされた都道府県を除外するかどうか")):
    csv_path = []
    hospital_cards = create_hospital_cards(csv_path, exclude_blocked)
    return hospital_cards

@app.post("/add-hospital")
async def add_hospital(name: str, address: str, departments: list):
    csv_path = []
    add_hospital_to_csv(csv_path, name, address, departments)
    return {"message": "病院が追加されました", "name": name, "address": address, "departments": departments}

@app.get("/hospital-data", response_class=JSONResponse)
async def get_hospital_data(exclude_blocked: bool = Query(True, description="ブロックされた都道府県を除外するかどうか")):
    hospital_data = extract_hospital_data(csv_paths, exclude_blocked)
    return hospital_data

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5001, reload=True)