# 職涯助理 AI (Career Assistant AI)

這是一個使用 AI 技術來協助求職者準備面試和優化履歷的專案。本專案使用 pydantic-ai 框架開發，可以：

- 分析履歷內容（支援 PDF 和純文字格式）
- 比對職缺描述，找出履歷中的缺漏
- 生成個人化的面試問題
- 提供職涯發展建議

## 功能特點

- 使用本地 Ollama 模型進行推理，確保資料隱私
- 支援 PDF 和純文字履歷解析
- 智能分析職缺要求與履歷匹配度
- 生成客製化的面試準備建議
- 提供職涯發展方向建議
- RESTful API 介面

## 安裝需求

- Python 3.9+
- Ollama 本地模型服務
- 其他依賴請參考 requirements.txt

## 快速開始

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 下載 Qwen 模型：
```bash
ollama pull qwen2.5:7b
```

3. 啟動 Ollama 服務：
```bash
ollama serve
```

4. 運行應用：
```bash
uvicorn app.main:app --reload
```

## API 端點

### 1. 整合分析（推薦使用）
- 端點：`POST /analyze-career`
- 功能：一次性獲取所有分析結果
- 輸入：
  - 履歷文件（PDF/文字）
  - 職缺標題
  - 職缺描述
  - 職缺要求列表
  - 問題數量（可選，預設 5 題）
- 輸出：
  - 履歷分析結果
  - 面試問題列表
  - 職涯發展建議

### 2. 個別功能端點

#### 2.1 履歷分析
- 端點：`POST /analyze-resume`
- 功能：分析履歷與職缺的匹配度
- 輸入：
  - 履歷文件（PDF/文字）
  - 職缺標題
  - 職缺描述
  - 職缺要求列表

#### 2.2 面試問題生成
- 端點：`POST /generate-interview-questions`
- 功能：生成個人化的面試問題
- 輸入：
  - 履歷文件
  - 職缺資訊
  - 問題數量（可選，預設 5 題）

#### 2.3 職涯建議
- 端點：`POST /career-advice`
- 功能：提供職涯發展建議
- 輸入：
  - 履歷文件
  - 職缺資訊

## 專案結構

```
career_assistant/
├── app/
│   ├── main.py              # FastAPI 應用程式入口
│   ├── models/
│   │   └── career_agent.py  # AI Agent 模型定義
│   ├── services/            # 業務邏輯層
│   └── utils/              # 工具函數
├── tests/                  # 測試檔案
├── requirements.txt        # 專案依賴
└── README.md              # 專案說明
```

## 使用範例

1. 使用 Swagger UI 測試 API：
   - 訪問 `http://localhost:8000/docs`
   - 選擇 `/analyze-career` 端點（推薦）
   - 上傳履歷文件並填寫相關資訊

2. 使用 curl 測試整合分析 API：
```bash
curl -X POST "http://localhost:8000/analyze-career" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "resume=@your_resume.pdf" \
     -F "job_title=資深工程師" \
     -F "job_description=職缺描述" \
     -F "job_requirements=要求1,要求2,要求3" \
     -F "question_count=5"
```

## 注意事項

- 確保 Ollama 服務正在運行
- 建議使用 Qwen 2.5 7B 模型以獲得最佳效果
- 大型 PDF 文件可能需要較長處理時間
- 請確保上傳的履歷文件格式正確

## 未來規劃

- [ ] 添加更多模型支援
- [ ] 實現對話式介面
- [ ] 添加更多職涯分析工具
- [ ] 支援更多文件格式
- [ ] 添加使用者認證功能

## 授權

MIT License 