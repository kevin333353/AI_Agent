from typing import List, Dict
import ollama
from pydantic import BaseModel
import PyPDF2
import io

class AIService:
    def __init__(self, model_name: str = "qwen2.5:7b"):
        self.model_name = model_name

    def extract_text_from_pdf(self, pdf_file: bytes) -> str:
        """從 PDF 文件中提取文本"""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    async def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        """分析履歷內容"""
        prompt = f"""
        請分析以下履歷內容，並與職缺描述進行比對：
        
        履歷：
        {resume_text}
        
        職缺描述：
        {job_description}
        
        請提供：
        1. 技能匹配度
        2. 經驗匹配度
        3. 缺失的技能或經驗
        4. 整體匹配分數
        """
        
        response = await ollama.generate(
            model=self.model_name,
            prompt=prompt
        )
        
        return self._parse_analysis_response(response)

    async def generate_interview_questions(self, resume_text: str, job_description: str) -> List[str]:
        """生成面試問題"""
        prompt = f"""
        基於以下履歷和職缺描述，生成相關的面試問題：
        
        履歷：
        {resume_text}
        
        職缺描述：
        {job_description}
        
        請生成 5 個相關的面試問題。
        """
        
        response = await ollama.generate(
            model=self.model_name,
            prompt=prompt
        )
        
        return self._parse_questions_response(response)

    def _parse_analysis_response(self, response: str) -> Dict:
        """解析 AI 分析結果"""
        # TODO: 實現解析邏輯
        return {
            "skills": ["Python", "FastAPI"],
            "experience": ["Software Engineer"],
            "education": ["Computer Science"],
            "missing_requirements": ["Kubernetes"],
            "match_score": 0.85
        }

    def _parse_questions_response(self, response: str) -> List[str]:
        """解析面試問題生成結果"""
        # TODO: 實現解析邏輯
        return [
            "請描述您在 AI 專案中的經驗",
            "您如何處理大型專案的技術挑戰？"
        ] 