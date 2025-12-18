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


class JobInterviewer(Agent):
    """AI Interviewer that asks questions based on resume and job description."""

    def __init__(self, resume: dict, job: dict):
        self.resume = resume
        self.job = job

        # Build context for the interviewer
        resume_summary = self._format_resume()
        job_summary = self._format_job()

        # Interviewer identity
        self.interviewer_name = "Sarah Mitchell"
        self.interviewer_title = "Engineering Hiring Manager"
        self.interviewer_years = 8

        super().__init__(
            instructions=f"""You are {self.interviewer_name}, {self.interviewer_title} at {self.job.get('company', 'the company')}.

YOUR BACKGROUND:
- Name: {self.interviewer_name}
- Role: {self.interviewer_title} at {self.job.get('company', 'the company')}
- Experience: {self.interviewer_years} years in tech, 3 years at {self.job.get('company', 'the company')}
- Personality: Warm, approachable, but thorough. You genuinely want candidates to succeed.
- Style: You like to have natural conversations rather than rigid Q&A sessions.

When introducing yourself, mention your name, role, and briefly how long you've been with the company. Make the candidate feel comfortable.

You are conducting a job interview for the position of {self.job.get('title', 'the role')}.

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
            exp_text += f"\n- {exp.get('title', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'N/A')})"
            for resp in exp.get('responsibilities', [])[:2]:
                exp_text += f"\n  * {resp}"

        # Format skills
        skills = r.get('skills', {})
        if isinstance(skills, dict):
            skills_text = ", ".join(
                skills.get('languages', []) +
                skills.get('frontend', [])[:2] +
                skills.get('backend', [])[:2]
            )
        else:
            skills_text = str(skills)

        # Format education
        education = r.get('education', [{}])
        if isinstance(education, list) and len(education) > 0:
            edu = education[0]
            edu_text = f"{edu.get('degree', 'N/A')} from {edu.get('school', 'N/A')}"
        else:
            edu_text = "N/A"

        return f"""Name: {r.get('name', 'Candidate')}
Summary: {r.get('summary', 'No summary provided')}
Experience:{exp_text if exp_text else ' No experience listed'}
Education: {edu_text}
Key Skills: {skills_text if skills_text else 'Not specified'}
Certifications: {', '.join(r.get('certifications', [])) if r.get('certifications') else 'None listed'}"""

    def _format_job(self) -> str:
        """Format job description into readable text."""
        j = self.job

        reqs = j.get('requirements', {})
        if isinstance(reqs, dict):
            must_have = ", ".join(reqs.get('must_have', [])[:5])
        else:
            must_have = str(reqs)

        responsibilities = j.get('responsibilities', [])
        resp_text = ', '.join(responsibilities[:3]) if responsibilities else 'Not specified'

        return f"""Position: {j.get('title', 'Position')}
Company: {j.get('company', 'Company')}
About: {j.get('about_company', 'No company description')}
Role: {j.get('about_role', 'No role description')}
Key Requirements: {must_have if must_have else 'Not specified'}
Responsibilities: {resp_text}"""

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
                result += f"\n{exp.get('title', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'N/A')}):\n"
                for resp in exp.get('responsibilities', []):
                    result += f"  - {resp}\n"
            return result

        elif section == "skills":
            skills = self.resume.get('skills', {})
            if isinstance(skills, dict):
                return f"""Candidate's skills:
Languages: {', '.join(skills.get('languages', []))}
Frontend: {', '.join(skills.get('frontend', []))}
Backend: {', '.join(skills.get('backend', []))}
Tools: {', '.join(skills.get('tools', []))}"""
            return f"Skills: {skills}"

        elif section == "education":
            education = self.resume.get('education', [{}])
            if isinstance(education, list) and len(education) > 0:
                edu = education[0]
                return f"Education: {edu.get('degree')} from {edu.get('school')} ({edu.get('year')})"
            return "Education: Not specified"

        elif section == "certifications":
            certs = self.resume.get('certifications', [])
            return f"Certifications: {', '.join(certs) if certs else 'None listed'}"

        else:
            return f"Unknown section: {section}. Available: experience, skills, education, certifications"

    @function_tool
    async def get_job_requirements(self, context: RunContext) -> str:
        """Get the detailed job requirements to formulate relevant questions."""
        reqs = self.job.get('requirements', {})

        if isinstance(reqs, dict):
            result = "Must-have requirements:\n"
            for req in reqs.get('must_have', []):
                result += f"  - {req}\n"

            result += "\nNice-to-have:\n"
            for req in reqs.get('nice_to_have', []):
                result += f"  - {req}\n"
            return result

        return f"Requirements: {reqs}"

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

Candidate: {self.resume.get('name', 'Candidate')}
Position: {self.job.get('title', 'Position')} at {self.job.get('company', 'Company')}
Questions asked: {self.questions_asked}

Thank the candidate for their time, ask if they have any questions about the role or company, and explain that the team will be in touch about next steps."""


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the interview agent."""
    import asyncio
    import logging
    logger = logging.getLogger("interview-agent")

    # Get resume and job from room metadata
    metadata = ctx.room.metadata
    logger.info(f"Room metadata: {metadata}")

    if metadata:
        try:
            data = json.loads(metadata)
            resume = data.get('resume', {})
            job = data.get('job', {})
            logger.info(f"Loaded resume for: {resume.get('name', 'Unknown')}")
            logger.info(f"Loaded job: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse room metadata: {e}")
            resume = {}
            job = {}
    else:
        logger.warning("No room metadata found, using empty resume and job")
        resume = {}
        job = {}

    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4.1-mini")),
        tts=openai.TTS(voice="shimmer"),  # Female voice for Sarah
        vad=silero.VAD.load(),
    )

    # Track and publish agent state changes to the room
    @session.on("agent_state_changed")
    def on_agent_state_changed(ev):
        """Publish agent state to room so frontend can display it."""
        state_name = str(ev.new_state).lower()
        # Extract just the state name (e.g., "AgentState.SPEAKING" -> "speaking")
        if "." in state_name:
            state_name = state_name.split(".")[-1]
        logger.info(f"Agent state changed: {state_name}")
        # Run async set_attributes in the event loop
        asyncio.create_task(
            ctx.room.local_participant.set_attributes({"agent_state": state_name})
        )

    await session.start(
        room=ctx.room,
        agent=JobInterviewer(resume=resume, job=job)
    )

    await session.generate_reply(
        instructions="Introduce yourself warmly as Sarah Mitchell. Mention your role as Engineering Hiring Manager, that you've been with the company for 3 years, and thank the candidate for taking the time to interview. Then briefly describe the role and start with your first question, referencing something from their resume."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
