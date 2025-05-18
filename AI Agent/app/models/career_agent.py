from pydantic_ai import Agent, Tool
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
import ollama
import PyPDF2
import io
import logging
import json
import re

logger = logging.getLogger(__name__)

class Resume(BaseModel):
    content: Union[str, bytes] = Field(..., description="履歷內容")
    format: str = Field(default="text", description="履歷格式 (text/pdf)")

    def get_text_content(self) -> str:
        """獲取履歷的文字內容"""
        if self.format == 'pdf':
            return self._extract_text_from_pdf(self.content)
        elif isinstance(self.content, bytes):
            return self.content.decode('utf-8')
        return self.content

    @staticmethod
    def _extract_text_from_pdf(pdf_content: bytes) -> str:
        """從 PDF 文件中提取文本"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"PDF 解析錯誤: {str(e)}")
            raise ValueError(f"無法解析 PDF 文件: {str(e)}")

class JobDescription(BaseModel):
    title: str = Field(..., description="職缺標題")
    description: str = Field(..., description="職缺描述")
    requirements: List[str] = Field(..., description="職缺要求")

class AnalysisResult(BaseModel):
    skills: List[str] = Field(..., description="識別出的技能")
    experience: List[str] = Field(..., description="工作經驗")
    education: List[str] = Field(..., description="教育背景")
    missing_requirements: List[str] = Field(..., description="缺失的要求")
    match_score: float = Field(..., description="匹配分數")

class InterviewQuestion(BaseModel):
    question: str = Field(..., description="面試問題")
    context: str = Field(..., description="問題背景")
    difficulty: str = Field(..., description="問題難度")

class CareerAgent(Agent):
    """職涯顧問 AI Agent"""
    
    def __init__(self, model_name: str = "qwen2.5:7b"):
        self.model_name = model_name
        super().__init__(
            name="Career Advisor",
            description="專業的職涯顧問，協助分析履歷、準備面試",
            tools=[
                Tool(
                    name="analyze_resume",
                    description="分析履歷內容並與職缺要求比對",
                    function=self.analyze_resume
                ),
                Tool(
                    name="generate_interview_questions",
                    description="生成個人化的面試問題",
                    function=self.generate_interview_questions
                ),
                Tool(
                    name="provide_career_advice",
                    description="提供職涯發展建議",
                    function=self.provide_career_advice
                )
            ]
        )

    def _generate_response(self, prompt: str) -> str:
        """使用 Ollama 生成回應"""
        try:
            logger.info(f"使用模型 {self.model_name} 生成回應")
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"生成回應時發生錯誤: {str(e)}")
            raise RuntimeError(f"AI 模型回應錯誤: {str(e)}")

    async def analyze_resume(self, resume: Resume, job_description: JobDescription) -> AnalysisResult:
        """分析履歷並與職缺要求比對"""
        try:
            # 獲取履歷文字內容
            resume_content = resume.get_text_content()

            prompt = f"""
            作為專業的職涯顧問，請分析以下履歷與職缺的匹配度：

            履歷內容：
            {resume_content}

            職缺要求：
            標題：{job_description.title}
            描述：{job_description.description}
            要求：{', '.join(job_description.requirements)}

            請提供詳細的分析，包括：
            1. 技能匹配度
            2. 經驗匹配度
            3. 教育背景相關性
            4. 缺失的技能或經驗
            5. 整體匹配分數（0-1）

            請以 JSON 格式回應，包含以下欄位：
            {{
                "skills": ["技能1", "技能2", ...],
                "experience": ["經驗1", "經驗2", ...],
                "education": ["教育1", "教育2", ...],
                "missing_requirements": ["缺失1", "缺失2", ...],
                "match_score": 0.85
            }}
            """
            
            response = self._generate_response(prompt)
            return self._parse_analysis_response(response)
            
        except Exception as e:
            logger.error(f"分析履歷時發生錯誤: {str(e)}")
            raise

    async def generate_interview_questions(
        self, 
        resume: Resume, 
        job_description: JobDescription,
        count: int = 5
    ) -> List[InterviewQuestion]:
        """生成個人化的面試問題"""
        try:
            # 獲取履歷文字內容
            resume_content = resume.get_text_content()

            prompt = f"""
            基於以下履歷和職缺描述，生成 {count} 個相關的面試問題：

            履歷：
            {resume_content}

            職缺：
            {job_description.title}
            {job_description.description}

            請生成具有挑戰性且相關的面試問題，並說明每個問題的背景和難度。
            請以 JSON 格式回應，格式如下：
            [
                {{
                    "question": "問題1",
                    "context": "背景1",
                    "difficulty": "難度1"
                }},
                ...
            ]
            """
            
            response = self._generate_response(prompt)
            return self._parse_questions_response(response)
            
        except Exception as e:
            logger.error(f"生成面試問題時發生錯誤: {str(e)}")
            raise

    async def provide_career_advice(
        self, 
        resume: Resume, 
        job_description: JobDescription
    ) -> str:
        """提供職涯發展建議"""
        try:
            # 獲取履歷文字內容
            resume_content = resume.get_text_content()

            prompt = f"""
            作為專業的職涯顧問，請為求職者提供具體的職涯發展建議：

            履歷：
            {resume_content}

            目標職缺：
            {job_description.title}
            {job_description.description}

            請提供：
            1. 短期改進建議
            2. 長期職涯規劃
            3. 技能提升方向

            請以結構化的方式回應，使用標題和段落來組織內容。
            """
            
            response = self._generate_response(prompt)
            return response
            
        except Exception as e:
            logger.error(f"生成職涯建議時發生錯誤: {str(e)}")
            raise

    def _parse_analysis_response(self, response: str) -> AnalysisResult:
        """解析分析結果"""
        try:
            # 嘗試從回應中提取 JSON 部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return AnalysisResult(
                    skills=data.get('skills', []),
                    experience=data.get('experience', []),
                    education=data.get('education', []),
                    missing_requirements=data.get('missing_requirements', []),
                    match_score=float(data.get('match_score', 0.0))
                )
            else:
                logger.warning("無法在回應中找到 JSON 格式的資料")
                raise ValueError("AI 回應格式不正確")
                
        except Exception as e:
            logger.error(f"解析分析結果時發生錯誤: {str(e)}")
            raise ValueError(f"無法解析 AI 回應: {str(e)}")

    def _parse_questions_response(self, response: str) -> List[InterviewQuestion]:
        """解析面試問題生成結果"""
        try:
            # 嘗試從回應中提取 JSON 部分
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return [
                    InterviewQuestion(
                        question=item.get('question', ''),
                        context=item.get('context', ''),
                        difficulty=item.get('difficulty', '中等')
                    )
                    for item in data
                ]
            else:
                logger.warning("無法在回應中找到 JSON 格式的資料")
                raise ValueError("AI 回應格式不正確")
                
        except Exception as e:
            logger.error(f"解析問題結果時發生錯誤: {str(e)}")
            raise ValueError(f"無法解析 AI 回應: {str(e)}") 