from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from pathlib import Path
import tempfile
import os
import logging
from .models.career_agent import CareerAgent, Resume, JobDescription, InterviewQuestion, AnalysisResult

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="職涯助理 AI", description="AI職涯輔助工具")

# 初始化 Agent
career_agent = CareerAgent()

class CareerAnalysisResponse(BaseModel):
    """整合所有分析結果的回應模型"""
    resume_analysis: AnalysisResult
    interview_questions: List[InterviewQuestion]
    career_advice: str

@app.post("/analyze-career", response_model=CareerAnalysisResponse)
async def analyze_career(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: List[str] = Form(...),
    question_count: int = Form(default=5)
):
    """
    整合分析履歷、生成面試問題和提供職涯建議
    """
    try:
        logger.info(f"開始處理整合分析請求: {resume.filename}")
        
        # 讀取文件內容
        resume_content = await resume.read()
        logger.info(f"成功讀取履歷文件，大小: {len(resume_content)} bytes")
        
        # 創建 Resume 和 JobDescription 對象
        resume_obj = Resume(
            content=resume_content,
            format='pdf' if resume.filename.endswith('.pdf') else 'text'
        )
        logger.info(f"履歷格式: {resume_obj.format}")
        
        job_desc = JobDescription(
            title=job_title,
            description=job_description,
            requirements=job_requirements
        )
        logger.info(f"職缺標題: {job_desc.title}")
        
        # 並行執行所有分析
        analysis_result = await career_agent.analyze_resume(resume_obj, job_desc)
        questions = await career_agent.generate_interview_questions(
            resume_obj, 
            job_desc,
            count=question_count
        )
        advice = await career_agent.provide_career_advice(resume_obj, job_desc)
        
        logger.info("整合分析完成")
        
        return CareerAnalysisResponse(
            resume_analysis=analysis_result,
            interview_questions=questions,
            career_advice=advice
        )
        
    except Exception as e:
        logger.error(f"處理整合分析時發生錯誤: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"處理整合分析時發生錯誤: {str(e)}"
        )

@app.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: List[str] = Form(...)
):
    """
    分析履歷並與職缺描述進行比對
    """
    try:
        logger.info(f"開始處理履歷分析請求: {resume.filename}")
        
        # 讀取文件內容
        resume_content = await resume.read()
        logger.info(f"成功讀取履歷文件，大小: {len(resume_content)} bytes")
        
        # 創建 Resume 和 JobDescription 對象
        resume_obj = Resume(
            content=resume_content,
            format='pdf' if resume.filename.endswith('.pdf') else 'text'
        )
        logger.info(f"履歷格式: {resume_obj.format}")
        
        job_desc = JobDescription(
            title=job_title,
            description=job_description,
            requirements=job_requirements
        )
        logger.info(f"職缺標題: {job_desc.title}")
        
        # 使用 Agent 分析履歷
        result = await career_agent.analyze_resume(resume_obj, job_desc)
        logger.info("履歷分析完成")
        
        return result
        
    except Exception as e:
        logger.error(f"處理履歷時發生錯誤: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"處理履歷時發生錯誤: {str(e)}"
        )

@app.post("/generate-interview-questions")
async def generate_interview_questions(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: List[str] = Form(...),
    question_count: int = Form(default=5)
) -> List[InterviewQuestion]:
    """
    生成個人化的面試問題
    """
    try:
        logger.info(f"開始生成面試問題: {resume.filename}")
        
        # 讀取文件內容
        resume_content = await resume.read()
        
        # 創建 Resume 和 JobDescription 對象
        resume_obj = Resume(
            content=resume_content,
            format='pdf' if resume.filename.endswith('.pdf') else 'text'
        )
        
        job_desc = JobDescription(
            title=job_title,
            description=job_description,
            requirements=job_requirements
        )
        
        # 使用 Agent 生成面試問題
        questions = await career_agent.generate_interview_questions(
            resume_obj, 
            job_desc,
            count=question_count
        )
        logger.info(f"成功生成 {len(questions)} 個面試問題")
        
        return questions
        
    except Exception as e:
        logger.error(f"生成面試問題時發生錯誤: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"生成面試問題時發生錯誤: {str(e)}"
        )

@app.post("/career-advice")
async def get_career_advice(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: List[str] = Form(...)
) -> str:
    """
    獲取職涯發展建議
    """
    try:
        logger.info(f"開始生成職涯建議: {resume.filename}")
        
        # 讀取文件內容
        resume_content = await resume.read()
        
        # 創建 Resume 和 JobDescription 對象
        resume_obj = Resume(
            content=resume_content,
            format='pdf' if resume.filename.endswith('.pdf') else 'text'
        )
        
        job_desc = JobDescription(
            title=job_title,
            description=job_description,
            requirements=job_requirements
        )
        
        # 使用 Agent 獲取職涯建議
        advice = await career_agent.provide_career_advice(resume_obj, job_desc)
        logger.info("成功生成職涯建議")
        
        return advice
        
    except Exception as e:
        logger.error(f"生成職涯建議時發生錯誤: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"生成職涯建議時發生錯誤: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 