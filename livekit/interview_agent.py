"""
Job Interview Simulator
=======================
A voice-based AI interviewer that conducts personalized interviews
based on the candidate's resume and the target job description.
Supports English and French languages.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
import os
import json

load_dotenv(".env")

# Sample resumes data (English)
SAMPLE_RESUMES = {
    "alex-chen": {
        "id": "alex-chen",
        "name": "Alex Chen",
        "summary": "Full-stack developer with 5 years of experience building scalable web applications. Passionate about clean code and user experience.",
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc.",
                "duration": "2021 - Present",
                "responsibilities": [
                    "Led development of microservices architecture serving 1M+ users",
                    "Mentored junior developers and conducted code reviews",
                    "Implemented CI/CD pipelines reducing deployment time by 60%"
                ]
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "duration": "2019 - 2021",
                "responsibilities": [
                    "Built React-based dashboard for real-time analytics",
                    "Developed RESTful APIs using Node.js and PostgreSQL",
                    "Collaborated with design team on UI/UX improvements"
                ]
            }
        ],
        "education": [{"degree": "B.S. Computer Science", "school": "University of California, Berkeley", "year": "2019"}],
        "skills": {
            "languages": ["TypeScript", "Python", "Go", "SQL"],
            "frontend": ["React", "Vue.js", "Next.js", "Tailwind CSS"],
            "backend": ["Node.js", "FastAPI", "PostgreSQL", "Redis"],
            "tools": ["Docker", "Kubernetes", "AWS", "GitHub Actions"]
        },
        "certifications": ["AWS Solutions Architect", "Google Cloud Professional"]
    },
    "sarah-johnson": {
        "id": "sarah-johnson",
        "name": "Sarah Johnson",
        "summary": "Frontend specialist with 4 years of experience creating beautiful, accessible web applications. Strong focus on performance and user experience.",
        "experience": [
            {
                "title": "Frontend Developer",
                "company": "DesignStudio",
                "duration": "2022 - Present",
                "responsibilities": [
                    "Developed component library used across 5 products",
                    "Improved Lighthouse scores from 65 to 95+",
                    "Implemented accessibility standards (WCAG 2.1 AA)"
                ]
            },
            {
                "title": "Junior Developer",
                "company": "WebAgency",
                "duration": "2020 - 2022",
                "responsibilities": [
                    "Built responsive websites for 20+ clients",
                    "Created animations and interactive experiences",
                    "Optimized images and assets for fast loading"
                ]
            }
        ],
        "education": [{"degree": "B.A. Digital Media", "school": "NYU", "year": "2020"}],
        "skills": {
            "languages": ["JavaScript", "TypeScript", "HTML", "CSS"],
            "frontend": ["React", "Vue.js", "Svelte", "SCSS", "Framer Motion"],
            "backend": ["Node.js", "Express"],
            "tools": ["Figma", "Storybook", "Jest", "Playwright"]
        },
        "certifications": ["Meta Frontend Developer", "Google UX Design"]
    },
    "michael-torres": {
        "id": "michael-torres",
        "name": "Michael Torres",
        "summary": "Backend engineer with 6 years of experience in distributed systems and cloud infrastructure. Expert in building high-availability services.",
        "experience": [
            {
                "title": "Staff Engineer",
                "company": "CloudScale",
                "duration": "2020 - Present",
                "responsibilities": [
                    "Architected event-driven system processing 10M events/day",
                    "Reduced infrastructure costs by 40% through optimization",
                    "Led migration from monolith to microservices"
                ]
            },
            {
                "title": "Backend Developer",
                "company": "DataFlow Inc.",
                "duration": "2018 - 2020",
                "responsibilities": [
                    "Built data pipelines for ML model training",
                    "Implemented real-time streaming with Kafka",
                    "Designed and maintained PostgreSQL databases"
                ]
            }
        ],
        "education": [{"degree": "M.S. Computer Science", "school": "MIT", "year": "2018"}],
        "skills": {
            "languages": ["Go", "Python", "Rust", "SQL"],
            "frontend": ["React"],
            "backend": ["gRPC", "Kafka", "PostgreSQL", "MongoDB", "Redis"],
            "tools": ["Kubernetes", "Terraform", "AWS", "GCP", "Prometheus"]
        },
        "certifications": ["AWS DevOps Professional", "CKA (Kubernetes)"]
    },
    # French resumes
    "marie-dupont": {
        "id": "marie-dupont",
        "name": "Marie Dupont",
        "summary": "Développeuse full-stack avec 5 ans d'expérience dans la création d'applications web performantes. Passionnée par le code propre et l'expérience utilisateur.",
        "experience": [
            {
                "title": "Ingénieure Logiciel Senior",
                "company": "TechFrance",
                "duration": "2021 - Présent",
                "responsibilities": [
                    "Direction du développement d'une architecture microservices pour 500K+ utilisateurs",
                    "Mentorat des développeurs juniors et revues de code",
                    "Mise en place de pipelines CI/CD réduisant le temps de déploiement de 50%"
                ]
            },
            {
                "title": "Développeuse Logiciel",
                "company": "StartupParis",
                "duration": "2019 - 2021",
                "responsibilities": [
                    "Développement d'un tableau de bord React pour l'analyse en temps réel",
                    "Création d'APIs RESTful avec Node.js et PostgreSQL",
                    "Collaboration avec l'équipe design pour l'amélioration UX"
                ]
            }
        ],
        "education": [{"degree": "Master Informatique", "school": "École Polytechnique", "year": "2019"}],
        "skills": {
            "languages": ["TypeScript", "Python", "Java", "SQL"],
            "frontend": ["React", "Vue.js", "Next.js", "Tailwind CSS"],
            "backend": ["Node.js", "Django", "PostgreSQL", "Redis"],
            "tools": ["Docker", "Kubernetes", "AWS", "GitLab CI"]
        },
        "certifications": ["AWS Solutions Architect", "Scrum Master"]
    },
    "thomas-martin": {
        "id": "thomas-martin",
        "name": "Thomas Martin",
        "summary": "Ingénieur backend avec 6 ans d'expérience en systèmes distribués et infrastructure cloud. Expert en services haute disponibilité.",
        "experience": [
            {
                "title": "Lead Technique",
                "company": "CloudEurope",
                "duration": "2020 - Présent",
                "responsibilities": [
                    "Architecture d'un système événementiel traitant 5M événements/jour",
                    "Réduction des coûts infrastructure de 35% par optimisation",
                    "Migration d'un monolithe vers une architecture microservices"
                ]
            },
            {
                "title": "Développeur Backend",
                "company": "DataTech",
                "duration": "2018 - 2020",
                "responsibilities": [
                    "Construction de pipelines de données pour l'entraînement ML",
                    "Implémentation de streaming temps réel avec Kafka",
                    "Conception et maintenance de bases PostgreSQL"
                ]
            }
        ],
        "education": [{"degree": "Diplôme d'Ingénieur", "school": "INSA Lyon", "year": "2018"}],
        "skills": {
            "languages": ["Go", "Python", "Java", "SQL"],
            "frontend": ["React"],
            "backend": ["gRPC", "Kafka", "PostgreSQL", "MongoDB", "Redis"],
            "tools": ["Kubernetes", "Terraform", "GCP", "Prometheus"]
        },
        "certifications": ["GCP Professional Cloud Architect", "CKA (Kubernetes)"]
    },
    "sophie-bernard": {
        "id": "sophie-bernard",
        "name": "Sophie Bernard",
        "summary": "Spécialiste frontend avec 4 ans d'expérience dans la création d'applications web accessibles et performantes. Focus sur l'UX et le design system.",
        "experience": [
            {
                "title": "Développeuse Frontend Senior",
                "company": "DesignLab Paris",
                "duration": "2022 - Présent",
                "responsibilities": [
                    "Création d'une bibliothèque de composants utilisée sur 8 produits",
                    "Amélioration des scores Lighthouse de 60 à 95+",
                    "Implémentation des standards d'accessibilité RGAA"
                ]
            },
            {
                "title": "Développeuse Frontend",
                "company": "AgenceWeb",
                "duration": "2020 - 2022",
                "responsibilities": [
                    "Développement de sites responsive pour 30+ clients",
                    "Création d'animations et expériences interactives",
                    "Optimisation des performances et du temps de chargement"
                ]
            }
        ],
        "education": [{"degree": "Master Design Numérique", "school": "Gobelins", "year": "2020"}],
        "skills": {
            "languages": ["JavaScript", "TypeScript", "HTML", "CSS"],
            "frontend": ["React", "Vue.js", "Nuxt", "SCSS", "Framer Motion"],
            "backend": ["Node.js", "Express"],
            "tools": ["Figma", "Storybook", "Jest", "Cypress"]
        },
        "certifications": ["Google UX Design", "Opquast"]
    }
}

# Sample jobs data
SAMPLE_JOBS = {
    # English jobs
    "senior-fullstack": {
        "id": "senior-fullstack",
        "title": "Senior Full-Stack Engineer",
        "company": "InnovateTech",
        "about_company": "InnovateTech is a fast-growing SaaS company building the next generation of productivity tools. We serve over 50,000 businesses worldwide.",
        "about_role": "We are looking for a Senior Full-Stack Engineer to join our core product team. You will work on our main web application used by thousands of users daily.",
        "responsibilities": [
            "Design and implement new features end-to-end",
            "Collaborate with product and design teams",
            "Mentor junior developers",
            "Participate in architecture decisions",
            "Write clean, tested, and documented code"
        ],
        "requirements": {
            "must_have": [
                "5+ years of software development experience",
                "Strong proficiency in TypeScript and React",
                "Experience with Node.js or Python backends",
                "Database design experience (SQL and NoSQL)",
                "Excellent communication skills"
            ],
            "nice_to_have": [
                "Experience with AWS or GCP",
                "Knowledge of CI/CD practices",
                "Experience with microservices",
                "Open source contributions"
            ]
        },
        "benefits": ["Competitive salary", "Remote-first", "Health insurance", "Equity"]
    },
    "frontend-lead": {
        "id": "frontend-lead",
        "title": "Frontend Tech Lead",
        "company": "VisualApps",
        "about_company": "VisualApps creates design and collaboration tools for creative teams. Our products are used by designers at Fortune 500 companies.",
        "about_role": "Lead our frontend team in building beautiful, performant applications. You will set technical direction and mentor a team of 5 engineers.",
        "responsibilities": [
            "Lead frontend architecture decisions",
            "Mentor and grow team members",
            "Drive performance and accessibility initiatives",
            "Collaborate with backend and design teams",
            "Ship high-quality features on schedule"
        ],
        "requirements": {
            "must_have": [
                "6+ years of frontend development experience",
                "Expert knowledge of React ecosystem",
                "Experience leading engineering teams",
                "Strong understanding of web performance",
                "Passion for great user experience"
            ],
            "nice_to_have": [
                "Experience with canvas/WebGL",
                "Knowledge of design systems",
                "Experience with real-time collaboration",
                "Background in design"
            ]
        },
        "benefits": ["Top-tier salary", "Unlimited PTO", "Learning budget", "Stock options"]
    },
    "backend-engineer": {
        "id": "backend-engineer",
        "title": "Backend Engineer",
        "company": "DataStream",
        "about_company": "DataStream provides real-time data infrastructure for modern applications. Our platform handles billions of events per day.",
        "about_role": "Join our infrastructure team to build and scale our core data pipeline. You will work on challenging distributed systems problems.",
        "responsibilities": [
            "Build and maintain data processing pipelines",
            "Optimize system performance and reliability",
            "Design APIs for internal and external use",
            "Participate in on-call rotation",
            "Write technical documentation"
        ],
        "requirements": {
            "must_have": [
                "4+ years of backend development experience",
                "Proficiency in Go or Python",
                "Experience with distributed systems",
                "Knowledge of message queues (Kafka, RabbitMQ)",
                "SQL and database optimization skills"
            ],
            "nice_to_have": [
                "Experience with Kubernetes",
                "Knowledge of stream processing",
                "Familiarity with observability tools",
                "Experience with high-throughput systems"
            ]
        },
        "benefits": ["Competitive pay", "Remote friendly", "401k matching", "Conference budget"]
    },
    # French jobs
    "ingenieur-fullstack-senior": {
        "id": "ingenieur-fullstack-senior",
        "title": "Ingénieur Full-Stack Senior",
        "company": "TechInnov",
        "about_company": "TechInnov est une entreprise SaaS en forte croissance qui développe des outils de productivité nouvelle génération. Nous servons plus de 30 000 entreprises en Europe.",
        "about_role": "Nous recherchons un Ingénieur Full-Stack Senior pour rejoindre notre équipe produit. Vous travaillerez sur notre application web principale utilisée par des milliers d'utilisateurs quotidiennement.",
        "responsibilities": [
            "Concevoir et implémenter des fonctionnalités de bout en bout",
            "Collaborer avec les équipes produit et design",
            "Encadrer les développeurs juniors",
            "Participer aux décisions d'architecture",
            "Écrire du code propre, testé et documenté"
        ],
        "requirements": {
            "must_have": [
                "5+ ans d'expérience en développement logiciel",
                "Maîtrise de TypeScript et React",
                "Expérience avec Node.js ou Python backend",
                "Expérience en conception de bases de données (SQL et NoSQL)",
                "Excellentes compétences en communication"
            ],
            "nice_to_have": [
                "Expérience avec AWS ou GCP",
                "Connaissance des pratiques CI/CD",
                "Expérience avec les microservices",
                "Contributions open source"
            ]
        },
        "benefits": ["Salaire compétitif", "Télétravail flexible", "Mutuelle", "BSPCE"]
    },
    "lead-frontend": {
        "id": "lead-frontend",
        "title": "Lead Technique Frontend",
        "company": "DesignApps",
        "about_company": "DesignApps crée des outils de design et collaboration pour les équipes créatives. Nos produits sont utilisés par les designers des plus grandes entreprises françaises.",
        "about_role": "Dirigez notre équipe frontend dans la création d'applications performantes et élégantes. Vous définirez la direction technique et encadrerez une équipe de 5 ingénieurs.",
        "responsibilities": [
            "Diriger les décisions d'architecture frontend",
            "Encadrer et faire progresser les membres de l'équipe",
            "Piloter les initiatives de performance et d'accessibilité",
            "Collaborer avec les équipes backend et design",
            "Livrer des fonctionnalités de haute qualité dans les délais"
        ],
        "requirements": {
            "must_have": [
                "6+ ans d'expérience en développement frontend",
                "Expertise de l'écosystème React",
                "Expérience en management d'équipes techniques",
                "Solide compréhension des performances web",
                "Passion pour l'expérience utilisateur"
            ],
            "nice_to_have": [
                "Expérience avec canvas/WebGL",
                "Connaissance des design systems",
                "Expérience avec la collaboration temps réel",
                "Background en design"
            ]
        },
        "benefits": ["Salaire attractif", "RTT illimités", "Budget formation", "BSPCE"]
    },
    "ingenieur-backend": {
        "id": "ingenieur-backend",
        "title": "Ingénieur Backend",
        "company": "DataFlow",
        "about_company": "DataFlow fournit une infrastructure de données temps réel pour les applications modernes. Notre plateforme traite des milliards d'événements par jour.",
        "about_role": "Rejoignez notre équipe infrastructure pour construire et faire évoluer notre pipeline de données. Vous travaillerez sur des problématiques complexes de systèmes distribués.",
        "responsibilities": [
            "Construire et maintenir les pipelines de traitement de données",
            "Optimiser les performances et la fiabilité du système",
            "Concevoir des APIs pour usage interne et externe",
            "Participer aux astreintes",
            "Rédiger la documentation technique"
        ],
        "requirements": {
            "must_have": [
                "4+ ans d'expérience en développement backend",
                "Maîtrise de Go ou Python",
                "Expérience avec les systèmes distribués",
                "Connaissance des files de messages (Kafka, RabbitMQ)",
                "Compétences en SQL et optimisation de bases de données"
            ],
            "nice_to_have": [
                "Expérience avec Kubernetes",
                "Connaissance du stream processing",
                "Familiarité avec les outils d'observabilité",
                "Expérience avec les systèmes à haut débit"
            ]
        },
        "benefits": ["Rémunération compétitive", "Télétravail", "PEE avec abondement", "Budget conférences"]
    }
}


def get_resume_by_id(resume_id: str) -> dict:
    """Get resume by ID, return default if not found."""
    return SAMPLE_RESUMES.get(resume_id, SAMPLE_RESUMES["alex-chen"])


def get_job_by_id(job_id: str) -> dict:
    """Get job by ID, return default if not found."""
    return SAMPLE_JOBS.get(job_id, SAMPLE_JOBS["senior-fullstack"])


class JobInterviewer(Agent):
    """AI Interviewer that asks questions based on resume and job description."""

    def __init__(self, resume: dict, job: dict, language: str = "en"):
        self.resume = resume
        self.job = job
        self.language = language

        # Build context for the interviewer
        resume_summary = self._format_resume()
        job_summary = self._format_job()

        # Interviewer identity based on language
        if language == "fr":
            self.interviewer_name = "Marie Dubois"
            self.interviewer_title = "Responsable Recrutement Tech"
            self.interviewer_years = 8
            instructions = self._get_french_instructions(resume_summary, job_summary)
        else:
            self.interviewer_name = "Sarah Mitchell"
            self.interviewer_title = "Engineering Hiring Manager"
            self.interviewer_years = 8
            instructions = self._get_english_instructions(resume_summary, job_summary)

        super().__init__(instructions=instructions)

        self.questions_asked = 0
        self.max_questions = 7

    def _get_english_instructions(self, resume_summary: str, job_summary: str) -> str:
        return f"""You are {self.interviewer_name}, {self.interviewer_title} at {self.job.get('company', 'the company')}.

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

    def _get_french_instructions(self, resume_summary: str, job_summary: str) -> str:
        company = self.job.get("company", "entreprise")
        title = self.job.get("title", "le poste")
        return f"""Vous êtes {self.interviewer_name}, {self.interviewer_title} chez {company}.

VOTRE PROFIL :
- Nom : {self.interviewer_name}
- Rôle : {self.interviewer_title} chez {company}
- Expérience : {self.interviewer_years} ans dans la tech, 3 ans chez {company}
- Personnalité : Chaleureuse, accessible, mais rigoureuse. Vous souhaitez sincèrement que les candidats réussissent.
- Style : Vous préférez les conversations naturelles plutôt que les sessions Q&R rigides.

Lorsque vous vous présentez, mentionnez votre nom, votre rôle et brièvement depuis combien de temps vous êtes dans cette entreprise. Mettez le candidat à l'aise.

Vous menez un entretien d'embauche pour le poste de {title}.

Vos objectifs :
1. Évaluer si le candidat correspond au poste
2. Poser des questions qui relient son expérience passée aux exigences du poste
3. Évaluer à la fois les compétences techniques et les soft skills
4. Être professionnelle mais amicale et conversationnelle
5. Mettre le candidat à l'aise tout en étant rigoureuse

CV DU CANDIDAT :
{resume_summary}

DESCRIPTION DU POSTE :
{job_summary}

DIRECTIVES POUR L'ENTRETIEN :
- Commencez par vous présenter chaleureusement (nom, rôle, ancienneté) et présenter le poste
- Posez une question à la fois et écoutez attentivement la réponse
- Faites référence à des éléments spécifiques du CV lors des questions de suivi
- Alternez questions comportementales (expérience passée) et situationnelles (hypothétiques)
- Montrez un intérêt sincère pour les réponses avec de brefs commentaires
- Restez concise - c'est une conversation vocale
- Après 5-7 questions, concluez l'entretien professionnellement

TYPES DE QUESTIONS À INCLURE :
1. Basées sur l'expérience : "Je vois que vous avez travaillé sur X chez Y. Pouvez-vous m'en dire plus..."
2. Techniques : Questions sur les compétences listées pertinentes pour le poste
3. Comportementales : "Parlez-moi d'une situation où..." (liée aux exigences du poste)
4. Situationnelles : "Comment géreriez-vous..." (basé sur les responsabilités du poste)
5. Motivation : Pourquoi ce poste, ce qui les intéresse dans cette entreprise

IMPORTANT : Vous devez parler UNIQUEMENT en français pendant tout l'entretien."""

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

        if self.language == "fr":
            if remaining <= 0:
                return "ENTRETIEN_TERMINÉ : Vous avez posé suffisamment de questions. Veuillez conclure l'entretien en remerciant le candidat, en lui demandant s'il a des questions, et en expliquant les prochaines étapes."
            elif remaining <= 2:
                return f"Vous avez posé {self.questions_asked} questions. Commencez à conclure bientôt - {remaining} questions restantes."
            else:
                return f"Question {self.questions_asked} sur {self.max_questions} posée. Continuez l'entretien."
        else:
            if remaining <= 0:
                return "INTERVIEW_COMPLETE: You've asked enough questions. Please wrap up the interview by thanking the candidate, asking if they have questions, and explaining next steps."
            elif remaining <= 2:
                return f"You've asked {self.questions_asked} questions. Start wrapping up soon - {remaining} questions remaining."
            else:
                return f"Question {self.questions_asked} of {self.max_questions} asked. Continue with the interview."

    @function_tool
    async def end_interview(self, context: RunContext) -> str:
        """End the interview and provide a summary."""
        if self.language == "fr":
            return f"""Entretien terminé !

Candidat : {self.resume.get('name', 'Candidat')}
Poste : {self.job.get('title', 'Poste')} chez {self.job.get('company', 'Entreprise')}
Questions posées : {self.questions_asked}

Remerciez le candidat pour son temps, demandez s'il a des questions sur le poste ou l'entreprise, et expliquez que l'équipe le recontactera pour les prochaines étapes."""
        else:
            return f"""Interview complete!

Candidate: {self.resume.get('name', 'Candidate')}
Position: {self.job.get('title', 'Position')} at {self.job.get('company', 'Company')}
Questions asked: {self.questions_asked}

Thank the candidate for their time, ask if they have any questions about the role or company, and explain that the team will be in touch about next steps."""


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the interview agent."""
    import asyncio
    import logging
    import time
    logger = logging.getLogger("interview-agent")

    start_time = time.time()
    def log_timing(step: str):
        elapsed = time.time() - start_time
        logger.info(f"[TIMING] {step}: {elapsed:.2f}s")

    log_timing("Entrypoint started")

    # Default IDs
    resume_id = "alex-chen"
    job_id = "senior-fullstack"
    voice_id = "aura-2-thalia-en"
    language = "en"

    # Connect to the room first
    logger.info("Connecting to room...")
    await ctx.connect()
    log_timing("Room connected")

    # Wait for participant to connect if not already connected
    if not ctx.room.remote_participants:
        logger.info("Waiting for participant to connect...")
        await ctx.wait_for_participant()
        log_timing("Participant connected")

    # Read metadata from participant
    for participant in ctx.room.remote_participants.values():
        if participant.metadata:
            try:
                data = json.loads(participant.metadata)
                resume_id = data.get('resumeId', resume_id)
                job_id = data.get('jobId', job_id)
                voice_id = data.get('voiceId', voice_id)
                language = data.get('language', language)
                logger.info(f"Found participant metadata: resume={resume_id}, job={job_id}, voice={voice_id}, language={language}")
                break
            except json.JSONDecodeError:
                pass

    log_timing("Metadata parsed")

    # Get resume and job data
    resume = get_resume_by_id(resume_id)
    job = get_job_by_id(job_id)
    logger.info(f"Using resume: {resume.get('name')} for job: {job.get('title')} at {job.get('company')} (language: {language})")

    log_timing("Resume/job loaded")

    # Load VAD
    logger.info("Loading VAD model...")
    vad = silero.VAD.load()
    log_timing("VAD loaded")

    # Create STT with language support
    logger.info("Creating STT...")
    stt_language = "fr" if language == "fr" else "en"
    stt = deepgram.STT(model="nova-2", language=stt_language)
    log_timing("STT created")

    # Create LLM
    logger.info("Creating LLM...")
    llm = openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4.1-mini"))
    log_timing("LLM created")

    # Create TTS with selected voice (Deepgram Aura-2)
    logger.info(f"Creating TTS with voice: {voice_id}...")
    tts = deepgram.TTS(model=voice_id)
    log_timing(f"TTS created with voice: {voice_id}")

    # Create session
    logger.info("Creating AgentSession...")
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
    )
    log_timing("AgentSession created")

    # Track and publish agent state changes to the room
    @session.on("agent_state_changed")
    def on_agent_state_changed(ev):
        """Publish agent state to room so frontend can display it."""
        state_name = str(ev.new_state).lower()
        if "." in state_name:
            state_name = state_name.split(".")[-1]
        logger.info(f"Agent state changed: {state_name}")
        asyncio.create_task(
            ctx.room.local_participant.set_attributes({"agent_state": state_name})
        )

    # Start session
    logger.info("Starting session...")
    await session.start(
        room=ctx.room,
        agent=JobInterviewer(resume=resume, job=job, language=language)
    )
    log_timing("Session started")

    # Generate initial reply based on language
    logger.info("Generating initial reply...")
    if language == "fr":
        await session.generate_reply(
            instructions="Présentez-vous chaleureusement en tant que Marie Dubois. Mentionnez votre rôle de Responsable Recrutement Tech, que vous êtes dans l'entreprise depuis 3 ans, et remerciez le candidat d'avoir pris le temps de passer cet entretien. Ensuite, décrivez brièvement le poste et commencez avec votre première question, en faisant référence à quelque chose de son CV."
        )
    else:
        await session.generate_reply(
            instructions="Introduce yourself warmly as Sarah Mitchell. Mention your role as Engineering Hiring Manager, that you've been with the company for 3 years, and thank the candidate for taking the time to interview. Then briefly describe the role and start with your first question, referencing something from their resume."
        )
    log_timing("Initial reply generated")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
