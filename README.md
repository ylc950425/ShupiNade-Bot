# Discord Bot — su / kanade

為 VTuber 粉絲社群打造的 Discord Bot，同一份程式碼供兩個伺服器的 Bot 使用：

| Bot | VTuber |
|-----|--------|
| **su** | 水宮枢 (Mizumiya Su) |
| **kanade** | 音乃瀬奏 (Kanade Izuru) |

---

## 目錄

- [功能列表](#功能列表)
- [專案結構](#專案結構)
- [環境需求與安裝](#環境需求與安裝)
- [部署說明](#部署說明)
- [設定檔說明](#設定檔說明)
- [指令一覽](#指令一覽)

---

## 功能列表

### 🎭 反應身份組 (`reaction.py`)
- 用戶在指定訊息上加上 Emoji 反應，自動獲得對應身份組
- 移除反應則撤銷身份組（基本身份組除外）
- 可透過管理員斜線指令動態新增/刪除設定

### 📋 事件記錄 (`log.py`)
| 類別 | 記錄事件 |
|------|---------|
| 訊息 | 訊息編輯（含前後對比）、訊息刪除（含附檔備份） |
| 成員 | 伺服器暱稱、身份組、伺服器頭像、全域名稱、全域頭像更新 |
| 伺服器 | 表符新增/刪除/改名、貼圖新增/刪除/編輯、邀請連結建立、身份組建立/刪除 |

### 🎮 小遊戲 (`game.py`)
| 遊戲 | 說明 |
|------|------|
| 擲骰子 | 選擇 1~20 顆骰子，可查看最多 100 筆翻頁紀錄 |
| 骰子挑戰 | 擲出所有骰子同點才能升階，進度持久化存檔 |
| 擲硬幣 | 顯示正/反面圖片，統計各面次數 |
| 二選一遊戲 | 從紅/藍中猜對才能過關，記錄最佳關卡數 |

### 👋 成員進出管理 (`join.py`)
- 新成員加入：於歡迎頻道發送自訂歡迎訊息（含規則頻道 Mention）
- 成員退出：於 Log 頻道發送含加入時間、持有身份組的告別訊息
- 自動更新成員數量計數頻道名稱

### ⏰ 定時任務 (`task.py`)
| 任務 | 觸發時間 | 說明 |
|------|---------|------|
| 每日推薦歌曲 | 每天 08:00（台灣時間） | 從追蹤清單中隨機推薦一首歌至大廳頻道 |
| 星期一嘲諷 | 每週日 23:30 | 發送貼圖與表符（**kanade 專屬**） |
| 伺服器改名 | 每週一 00:00 | 改名為「奏の月曜工坊」（**kanade 專屬**） |
| 伺服器復原 | 每週二 00:00 | 改回「奏の樂音工坊」（**kanade 專屬**） |

### 📺 YouTube 頻道監控 (`youtube.py`)
透過 YouTube Data API v3 監控指定頻道，每分鐘輪詢一次，開台前 30 分鐘改為每 5 秒輪詢：

| 事件 | 通知內容 |
|------|---------|
| 新影片上傳 | 影片標題、縮圖、連結 |
| 直播待機室建立 | 預定開台時間 |
| 直播開始 | @直播通知身份組 ping + 實際開台時間 |
| 直播結束 | 結束時間 + 直播時長 |
| 標題/開台時間/封面圖變更 | 前後對比 |
| 訂閱數/影片數/總觀看數里程碑 | 到達里程碑時通知 |
| 影片觀看數追蹤 | 每超過 10 萬次通知一次 |
| 直播聊天室監控 | 偵測 Hololive 成員或版主留言，轉發至 Discord |

### 💬 訊息功能 (`message.py`)
- **防洗頻**：10 秒內偵測到 3 則以上相同訊息 → 刪除 30 秒內所有相同訊息、移除基本身份組、發送違規記錄
- **Bot 對話**（限指定頻道）：回應是/否、可以/不可以、機率查詢、求籤、多選一等問題
- **私訊轉發**：將用戶私訊內容轉發至後台頻道，並自動回覆設定的訊息

### ⚙️ 斜線指令 (`slash.py`)
詳細說明見[指令一覽](#指令一覽)。

---

## 專案結構

```
/
├── app.py                    # Bot 入口點，處理 load/unload/reload 指令
├── .env                      # Bot Token
├── Define/
│   ├── Classes.py            # 基礎類別 MyBot, MyCog, MyView, MyModal
│   ├── Functions.py          # 工具函式（讀寫 JSON、時間、URL 解析等）
│   └── CommandsGroup.py      # 斜線指令群組定義
├── Cogs/
│   ├── game.py               # 小遊戲
│   ├── join.py               # 成員進出處理
│   ├── log.py                # 事件記錄
│   ├── message.py            # 訊息處理
│   ├── reaction.py           # 反應身份組
│   ├── slash.py              # 各類斜線指令
│   ├── task.py               # 定時任務
│   └── youtube.py            # YouTube 頻道監控
└── jsonfile/
    ├── settings.json         # 伺服器設定（ID、功能開關等）
    ├── youtube_data.json     # YouTube 監控資料
    └── game_data.json        # 遊戲玩家存檔
```

> **注意**：`jsonfile/` 資料夾在不同伺服器的部署環境中內容不同，請勿混用。

---

## 環境需求與安裝

- Python 3.10+

### 安裝相依套件

```bash
pip install discord.py python-dotenv requests pytchat emoji PyNaCl davey
```

| 套件 | 用途 |
|------|------|
| `discord.py` | Discord Bot 框架 |
| `python-dotenv` | 從 `.env` 讀取 Token |
| `requests` | 呼叫 YouTube Data API |
| `pytchat` | 讀取 YouTube 直播聊天室 |
| `emoji` | 驗證 Unicode Emoji 格式 |
| `PyNaCl` | 語音功能相依套件（程式碼中未直接 import，但 discord.py 語音需要） |
| `davey` | 語音功能相依套件（程式碼中未直接 import，但 discord.py 語音需要） |

---

## 部署說明

### 1. 設定 Token

在專案根目錄（與 `app.py` 同層）建立 `.env` 檔：

```env
TOKEN=你的_Bot_Token
```

### 2. 準備 `jsonfile/` 資料夾

根據要部署的 Bot（su 或 kanade），將對應的設定檔放入 `jsonfile/` 資料夾：

```
jsonfile/
├── settings.json
├── youtube_data.json
└── game_data.json
```

> ⚠️ 部署時資料夾名稱固定為 `jsonfile`，不加 `-su` 或 `-kanade` 後綴。兩個 Bot 各自部署在不同伺服器上，每個環境只有一份 `jsonfile/`。

### 3. 啟動 Bot

```bash
python app.py
```

Bot 啟動後會自動載入 `Cogs/` 下所有 `.py` 模組，並同步斜線指令至 Discord。

---

## 設定檔說明

### `jsonfile/settings.json`

```jsonc
{
    "id": {
        "guild": 伺服器ID,
        "role": {
            "basic": 基本身份組ID,          // 加入伺服器後透過反應領取
            "admin": 管理員身份組ID,
            "sub_admin": 副管理員身份組ID,   // 可設為 null
            "stream_notice": 直播通知身份組ID
        },
        "channel": {
            "welcome": 歡迎頻道ID,
            "rule": 規則頻道ID,
            "member_count": 成員計數頻道ID,
            "report": 服務台討論串父頻道ID,
            "penalty": 違規記錄頻道ID,
            "log": {
                "message": 訊息Log頻道ID,
                "member": 成員Log頻道ID,
                "guild": 伺服器Log頻道ID
            },
            "bot": {
                "chat": Bot對話頻道ID,
                "game": 遊戲指令頻道ID,
                "panel": Bot後台頻道ID
            },
            "chat": {
                "lobby": 大廳頻道ID,        // 每日推薦歌曲發送至此
                "stream": 直播討論頻道ID,
                "oshi": 推文頻道ID
            },
            "youtube": {
                "video_upload": 影片通知頻道ID,
                "video_views": 觀看數里程碑頻道ID
            }
        }
    },
    "reaction_role": [
        {
            "role_id": 身份組ID,
            "reaction": "表符（支援自訂表符格式 <:name:id>）",
            "message_url": "Discord 訊息完整 URL"
        }
    ],
    "image": {
        "omikuji": [ { "name": "籤名", "url": "圖片URL（不含副檔名）" } ],
        "coin":    [ { "name": "裏/表", "url": "圖片URL（不含副檔名）" } ]
    },
    "welcome_message": "歡迎訊息，可用 {member} {guild} {rule_channel} 作為變數",
    "function": {
        "first_person": "Bot 的第一人稱稱呼",
        "member_counter": {
            "enable": true,
            "name": "頻道名稱格式，可用 {member_count} 作為變數"
        },
        "message_react": {
            "觸發關鍵字（支援 Regex，{mention_self} 代表 @Bot）": {
                "reaction": ["要加的 Emoji"],
                "reply": [],
                "send": ["要傳送的訊息"]
            }
        },
        "spam_check": { "enable": true },
        "dm_reply": {
            "enable": true,
            "message": "收到私訊時自動回覆的內容"
        }
    },
    "guild": {
        "kanade": false,  // true 則啟用 kanade 專屬功能（星期一任務等）
        "su": true
    }
}
```

### `jsonfile/youtube_data.json`

```jsonc
{
    "key": "YouTube Data API v3 金鑰",
    "channel_id": "要監控的 YouTube 頻道 ID",
    "playlist_id": "對應頻道的上傳播放清單 ID（通常將頻道 ID 的 UC 換成 UU）",
    "statistics": {
        "viewCount": 上次記錄的總觀看數,
        "subscriberCount": 上次記錄的訂閱數,
        "videoCount": 上次記錄的影片數,
        "milestone": { "viewCount": 0, "videoCount": 0 }
    },
    "channel_chat_live_title": {
        "live": "直播中時的討論頻道名稱",
        "nolive": "無直播時的討論頻道名稱"
    },
    "freechat_video_id": ["不追蹤的影片 ID（如 Free Chat 台）"],
    "playlist_video_id": [],  // 最近 20 筆已處理過的影片 ID，由程式自動維護
    "streams": [],            // 正在追蹤的直播/待機室，由程式自動維護
    "views_check": [          // 觀看數追蹤清單，可透過 /youtube video-views 管理
        { "name": "影片名稱", "id": "影片ID", "views": 上次記錄觀看數 }
    ],
    "emoji": [                // YouTube 表符與 Discord 表符的對應表
        { "yt": "YouTube 表符 Regex", "dc": "Discord 表符" }
    ]
}
```

### `jsonfile/game_data.json`

由程式自動維護，記錄所有玩家的遊戲進度，無需手動編輯。初始內容如下：

```json
{
    "red_or_blue": { "ranking": [] },
    "dice": { "emoji": [] },
    "player": {}
}
```

---

## 指令一覽

### 前綴指令（`!`）

| 指令 | 說明 |
|------|------|
| `!load <模組名>` | 載入指定 Cog |
| `!unload <模組名>` | 卸載指定 Cog |
| `!reload <模組名>` | 重新載入指定 Cog |
| `!set_report` | 在當前頻道發送服務台按鈕訊息 |

### 斜線指令（`/`）

#### `/game` — 遊戲（限遊戲頻道）

| 指令 | 說明 |
|------|------|
| `/game dice` | 擲骰子（選擇骰子數量，可查看紀錄） |
| `/game dice-challenge` | 骰子挑戰（擲出同點才能升階） |
| `/game coin-toss` | 擲硬幣 |
| `/game red-or-blue` | 二選一闖關遊戲 |

#### `/youtube` — YouTube 設定（管理員限定）

| 指令 | 說明 |
|------|------|
| `/youtube add-video <url>` | 手動加入影片/直播至監控清單 |
| `/youtube show-streams` | 顯示目前所有追蹤中的直播台 |
| `/youtube video-views` | 開啟影片觀看數追蹤設定面板 |
| `/youtube get-thumbnail <url>` | 取得 YouTube 影片封面圖 |

#### `/settings` — 伺服器設定（管理員限定）

| 指令 | 說明 |
|------|------|
| `/settings reaction-role` | 開啟反應身份組設定面板（可新增/刪除） |

#### `/message` — 訊息管理（管理員限定）

| 指令 | 說明 |
|------|------|
| `/message send <頻道> <訊息內容>` | 以 Bot 身份發送訊息至指定頻道 |
| `/message edit <訊息連結> <訊息內容>` | 編輯 Bot 發送過的訊息 |
| `/message credit <圖片> <作者> <來源> [備註]` | 發送表符出處 Embed |

#### `/voice-channel` — 語音頻道

| 指令 | 說明 |
|------|------|
| `/voice-channel connect <頻道>` | 將 Bot 加入語音頻道 |
| `/voice-channel disconnect` | 將 Bot 退出語音頻道 |

#### `/func convert` — 換算工具

| 指令 | 說明 |
|------|------|
| `/func convert temperature` | 溫度單位互換（°C / °F / K，輸入其中一個即可） |
