from flask import Flask, request, jsonify
from flask_cors import CORS
from models.career_agent import CareerAgent, Resume, JobDescription
import logging
import json
import asyncio

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 初始化 AI 代理
agent = CareerAgent()

@app.route('/')
def index():
    return jsonify({"status": "API service is running"})

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "未提供履歷檔案"}), 400
        
        resume_file = request.files['resume']
        job_info = request.form.get('job_info', '{}')
        
        # 解析職缺資訊
        try:
            job_data = json.loads(job_info)
            # 確保 requirements 是列表
            if 'requirements' not in job_data:
                job_data['requirements'] = []
            elif isinstance(job_data['requirements'], str):
                try:
                    job_data['requirements'] = json.loads(job_data['requirements'])
                except json.JSONDecodeError:
                    job_data['requirements'] = []
            
            job_description = JobDescription(
                title=job_data.get('title', ''),
                description=job_data.get('description', ''),
                requirements=job_data['requirements']
            )
        except json.JSONDecodeError:
            return jsonify({"error": "無效的職缺資訊格式"}), 400

        # 創建履歷物件
        resume = Resume(
            content=resume_file.read(),
            format=resume_file.filename.split('.')[-1].lower()
        )

        # 分析履歷
        result = asyncio.run(agent.analyze_resume(resume, job_description))
        return jsonify(result.model_dump())

    except Exception as e:
        logger.error(f"分析履歷時發生錯誤: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-interview-questions', methods=['POST'])
def generate_interview_questions():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "未提供履歷檔案"}), 400
        
        resume_file = request.files['resume']
        job_info = request.form.get('job_info', '{}')
        
        try:
            job_data = json.loads(job_info)
            job_description = JobDescription(
                title=job_data.get('title', ''),
                description=job_data.get('description', ''),
                requirements=job_data.get('requirements', [])
            )
        except json.JSONDecodeError:
            return jsonify({"error": "無效的職缺資訊格式"}), 400

        resume = Resume(
            content=resume_file.read(),
            format=resume_file.filename.split('.')[-1].lower()
        )

        questions = asyncio.run(agent.generate_interview_questions(resume, job_description))
        return jsonify([q.model_dump() for q in questions])

    except Exception as e:
        logger.error(f"生成面試問題時發生錯誤: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/provide-career-advice', methods=['POST'])
def provide_career_advice():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "未提供履歷檔案"}), 400
        
        resume_file = request.files['resume']
        career_goals = request.form.get('career_goals', '')

        resume = Resume(
            content=resume_file.read(),
            format=resume_file.filename.split('.')[-1].lower()
        )

        # 創建一個簡單的職缺描述，用於提供職涯建議
        job_description = JobDescription(
            title="職涯發展",
            description=career_goals,
            requirements=[]
        )

        advice = asyncio.run(agent.provide_career_advice(resume, job_description))
        return jsonify({"advice": advice})

    except Exception as e:
        logger.error(f"提供職涯建議時發生錯誤: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 