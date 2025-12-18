"""
Technical Interview Simulator
=============================
A voice-based AI interviewer that conducts technical interviews.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
import os
import random

load_dotenv(".env")


class TechnicalInterviewer(Agent):
    """AI Technical Interviewer that asks coding and system design questions."""

    def __init__(self):
        super().__init__(
            instructions="""You are a friendly but professional technical interviewer at a top tech company.

Your role:
- Conduct a technical interview with the candidate
- Ask one question at a time and wait for their response
- Listen carefully to answers and ask follow-up questions when needed
- Provide brief encouragement but stay professional
- After each answer, give brief feedback (1-2 sentences) then move to the next question

Interview style:
- Be conversational and natural, like a real interview
- If the candidate is stuck, offer a small hint
- Keep responses concise - this is a voice conversation
- Don't repeat the question unless asked

Start by introducing yourself briefly and asking the first question."""
        )

        self.questions = {
            "python": [
                "What's the difference between a list and a tuple in Python?",
                "Explain what a decorator is and give an example of when you'd use one.",
                "What are Python generators and why would you use them?",
                "How does garbage collection work in Python?",
                "What's the difference between deep copy and shallow copy?",
            ],
            "javascript": [
                "Explain the difference between let, const, and var.",
                "What is the event loop in JavaScript and how does it work?",
                "What's the difference between == and === in JavaScript?",
                "Explain closures and give an example.",
                "What are Promises and how do they differ from callbacks?",
            ],
            "system_design": [
                "How would you design a URL shortener like bit.ly?",
                "Walk me through how you'd design a rate limiter.",
                "How would you design a cache system for a web application?",
                "Explain how you'd design a simple chat application.",
                "How would you handle file uploads for a system with millions of users?",
            ],
            "data_structures": [
                "What's the difference between an array and a linked list? When would you use each?",
                "Explain how a hash table works and what its time complexity is.",
                "What's the difference between a stack and a queue?",
                "When would you use a tree versus a graph data structure?",
                "Explain what Big O notation means and why it matters.",
            ],
            "general": [
                "Tell me about a challenging technical problem you solved recently.",
                "How do you approach debugging a complex issue?",
                "What's your process for learning a new technology?",
                "How do you handle technical disagreements with teammates?",
                "Describe your ideal development workflow.",
            ],
        }

        self.current_topic = None
        self.questions_asked = []
        self.current_question_index = 0
        self.max_questions = 5

    @function_tool
    async def start_interview(self, context: RunContext, topic: str) -> str:
        """Start the interview with a specific topic.

        Args:
            topic: The topic to focus on - python, javascript, system_design, data_structures, or general
        """
        topic_lower = topic.lower().replace(" ", "_")

        if topic_lower not in self.questions:
            available = ", ".join(self.questions.keys())
            return f"Topic '{topic}' not available. Choose from: {available}"

        self.current_topic = topic_lower
        self.questions_asked = random.sample(self.questions[topic_lower],
                                             min(self.max_questions, len(self.questions[topic_lower])))
        self.current_question_index = 0

        return f"Starting {topic} interview with {len(self.questions_asked)} questions. First question: {self.questions_asked[0]}"

    @function_tool
    async def next_question(self, context: RunContext) -> str:
        """Move to the next interview question."""
        if not self.current_topic:
            return "No interview started. Ask the candidate which topic they'd like to focus on: Python, JavaScript, System Design, Data Structures, or General."

        self.current_question_index += 1

        if self.current_question_index >= len(self.questions_asked):
            return "INTERVIEW_COMPLETE: All questions have been asked. Provide a brief summary of how the candidate did and thank them for their time."

        return f"Next question ({self.current_question_index + 1}/{len(self.questions_asked)}): {self.questions_asked[self.current_question_index]}"

    @function_tool
    async def get_hint(self, context: RunContext) -> str:
        """Provide a hint for the current question if the candidate is stuck."""
        if not self.current_topic or self.current_question_index >= len(self.questions_asked):
            return "No current question to provide a hint for."

        hints = {
            "What's the difference between a list and a tuple in Python?":
                "Think about mutability - can you change the contents after creation?",
            "Explain what a decorator is and give an example of when you'd use one.":
                "Think of it as a wrapper around a function. Common uses include logging or timing.",
            "How would you design a URL shortener like bit.ly?":
                "Consider: How do you generate short codes? Where do you store mappings? How do you handle collisions?",
            "What's the difference between an array and a linked list?":
                "Think about memory layout and how that affects insertion, deletion, and access times.",
        }

        current_q = self.questions_asked[self.current_question_index]
        return hints.get(current_q, "Think about the core concepts involved and try to explain your reasoning step by step.")

    @function_tool
    async def get_progress(self, context: RunContext) -> str:
        """Check how far along the interview is."""
        if not self.current_topic:
            return "No interview in progress."

        return f"Topic: {self.current_topic}, Question {self.current_question_index + 1} of {len(self.questions_asked)}"


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the interview agent."""

    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4.1-mini")),
        tts=openai.TTS(voice="echo"),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=TechnicalInterviewer()
    )

    await session.generate_reply(
        instructions="Introduce yourself as Alex, a technical interviewer. Ask the candidate which topic they'd like to focus on: Python, JavaScript, System Design, Data Structures, or General technical questions. Keep it brief and friendly."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
