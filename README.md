# 職涯助理 AI (Career Assistant AI)
![AGENT](https://github.com/user-attachments/assets/13759682-fa58-44a6-aa9d-de2e768211d9)

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
- Node.js 16+
- Ollama 本地模型服務
- 其他依賴請參考 requirements.txt 和 package.json

## 快速開始

1. 安裝後端依賴：
```bash
pip install -r requirements.txt
```

2. 安裝前端依賴：
```bash
cd frontend
npm install
```

3. 下載 Qwen 模型：
```bash
ollama pull qwen2.5:7b
```

4. 啟動 Ollama 服務：
```bash
ollama serve
```

5. 啟動後端服務：
```bash
python app.py
```

6. 啟動前端服務：
```bash
cd frontend
npm start
```

現在您可以通過瀏覽器訪問 http://localhost:3000 使用應用程式。

## API 端點

### 1. 整合分析（推薦使用）
- 端點：`POST /analyze-career`
- 功能：一次性獲取所有分析結果
- 輸入：
  - 履歷文件（PDF/文字）
  - 職缺標題
  - 職缺描述
  - 職缺要求列表
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

#### 2.3 職涯建議
- 端點：`POST /career-advice`
- 功能：提供職涯發展建議
- 輸入：
  - 履歷文件
  - 職缺資訊
