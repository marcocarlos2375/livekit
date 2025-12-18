"""
Job Interview Simulator
=======================
A voice-based AI interviewer that conducts personalized interviews
based on the candidate's resume and the target job description.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
import os
import json

load_dotenv(".env")


def load_json_file(filename: str) -> dict:
    """Load a JSON file from the same directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'r') as f:
        return json.load(f)


class JobInterviewer(Agent):
    """AI Interviewer that asks questions based on resume and job description."""

    def __init__(self):
        # Load resume and job description
        self.resume = load_json_file("resume.json")
        self.job = load_json_file("job_description.json")

        # Build context for the interviewer
        resume_summary = self._format_resume()
        job_summary = self._format_job()

        # Interviewer identity
        self.interviewer_name = "Sarah Mitchell"
        self.interviewer_title = "Engineering Hiring Manager"
        self.interviewer_years = 8

        super().__init__(
            instructions=f"""You are {self.interviewer_name}, {self.interviewer_title} at {self.job['company']}.

YOUR BACKGROUND:
- Name: {self.interviewer_name}
- Role: {self.interviewer_title} at {self.job['company']}
- Experience: {self.interviewer_years} years in tech, 3 years at {self.job['company']}
- Personality: Warm, approachable, but thorough. You genuinely want candidates to succeed.
- Style: You like to have natural conversations rather than rigid Q&A sessions.

When introducing yourself, mention your name, role, and briefly how long you've been with the company. Make the candidate feel comfortable.

You are conducting a job interview for the position of {self.job['title']}.

Your goals:
1. Assess if the candidate is a good fit for the role
2. Ask questions that relate their past experience to the job requirements
3. Evaluate both technical skills and soft skills
4. Be professional but friendly and conversational
5. Make the candidate feel at ease while still being thorough

CANDIDATE'S RESUME:
{resume_summary}

JOB DESCRIPTION:
{job_summary}

INTERVIEW GUIDELINES:
- Start by introducing yourself warmly (name, role, time at company) and the position
- Ask one question at a time and listen carefully to the response
- Reference specific items from their resume when asking follow-up questions
- Mix behavioral questions (past experience) with situational questions (hypotheticals)
- Show genuine interest in their answers with brief acknowledgments
- Keep responses concise - this is a voice conversation
- After 5-7 questions, wrap up the interview professionally

QUESTION TYPES TO INCLUDE:
1. Experience-based: "I see you worked on X at Y company. Can you tell me more about..."
2. Technical: Questions about their listed skills relevant to the job
3. Behavioral: "Tell me about a time when..." (related to job requirements)
4. Situational: "How would you handle..." (based on job responsibilities)
5. Motivation: Why they want this role, what interests them about the company"""
        )

        self.questions_asked = 0
        self.max_questions = 7

    def _format_resume(self) -> str:
        """Format resume data into readable text."""
        r = self.resume

        # Format experience
        exp_text = ""
        for exp in r.get('experience', []):
            exp_text += f"\n- {exp['title']} at {exp['company']} ({exp['duration']})"
            for resp in exp.get('responsibilities', [])[:2]:
                exp_text += f"\n  * {resp}"

        # Format skills
        skills = r.get('skills', {})
        skills_text = ", ".join(skills.get('languages', []) + skills.get('frontend', [])[:2] + skills.get('backend', [])[:2])

        return f"""Name: {r.get('name')}
Summary: {r.get('summary')}
Experience:{exp_text}
Education: {r.get('education', [{}])[0].get('degree', 'N/A')} from {r.get('education', [{}])[0].get('school', 'N/A')}
Key Skills: {skills_text}
Certifications: {', '.join(r.get('certifications', []))}"""

    def _format_job(self) -> str:
        """Format job description into readable text."""
        j = self.job

        reqs = j.get('requirements', {})
        must_have = ", ".join(reqs.get('must_have', [])[:5])

        return f"""Position: {j.get('title')}
Company: {j.get('company')}
About: {j.get('about_company')}
Role: {j.get('about_role')}
Key Requirements: {must_have}
Responsibilities: {', '.join(j.get('responsibilities', [])[:3])}"""

    @function_tool
    async def get_resume_detail(self, context: RunContext, section: str) -> str:
        """Get specific details from the candidate's resume.

        Args:
            section: The section to retrieve - experience, skills, education, or certifications
        """
        section = section.lower()

        if section == "experience":
            result = "Candidate's work experience:\n"
            for exp in self.resume.get('experience', []):
                result += f"\n{exp['title']} at {exp['company']} ({exp['duration']}):\n"
                for resp in exp.get('responsibilities', []):
                    result += f"  - {resp}\n"
            return result

        elif section == "skills":
            skills = self.resume.get('skills', {})
            return f"""Candidate's skills:
Languages: {', '.join(skills.get('languages', []))}
Frontend: {', '.join(skills.get('frontend', []))}
Backend: {', '.join(skills.get('backend', []))}
Tools: {', '.join(skills.get('tools', []))}"""

        elif section == "education":
            edu = self.resume.get('education', [{}])[0]
            return f"Education: {edu.get('degree')} from {edu.get('school')} ({edu.get('year')})"

        elif section == "certifications":
            return f"Certifications: {', '.join(self.resume.get('certifications', []))}"

        else:
            return f"Unknown section: {section}. Available: experience, skills, education, certifications"

    @function_tool
    async def get_job_requirements(self, context: RunContext) -> str:
        """Get the detailed job requirements to formulate relevant questions."""
        reqs = self.job.get('requirements', {})

        result = "Must-have requirements:\n"
        for req in reqs.get('must_have', []):
            result += f"  - {req}\n"

        result += "\nNice-to-have:\n"
        for req in reqs.get('nice_to_have', []):
            result += f"  - {req}\n"

        return result

    @function_tool
    async def track_question(self, context: RunContext) -> str:
        """Track that a question was asked. Call this after each question."""
        self.questions_asked += 1
        remaining = self.max_questions - self.questions_asked

        if remaining <= 0:
            return "INTERVIEW_COMPLETE: You've asked enough questions. Please wrap up the interview by thanking the candidate, asking if they have questions, and explaining next steps."
        elif remaining <= 2:
            return f"You've asked {self.questions_asked} questions. Start wrapping up soon - {remaining} questions remaining."
        else:
            return f"Question {self.questions_asked} of {self.max_questions} asked. Continue with the interview."

    @function_tool
    async def end_interview(self, context: RunContext) -> str:
        """End the interview and provide a summary."""
        return f"""Interview complete!

Candidate: {self.resume.get('name')}
Position: {self.job.get('title')} at {self.job.get('company')}
Questions asked: {self.questions_asked}

Thank the candidate for their time, ask if they have any questions about the role or company, and explain that the team will be in touch about next steps."""


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the interview agent."""

    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4.1-mini")),
        tts=openai.TTS(voice="shimmer"),  # Female voice for Sarah
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=JobInterviewer()
    )

    await session.generate_reply(
        instructions="Introduce yourself warmly as Sarah Mitchell. Mention your role as Engineering Hiring Manager, that you've been with the company for 3 years, and thank the candidate for taking the time to interview. Then briefly describe the role and start with your first question, referencing something from their resume."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
