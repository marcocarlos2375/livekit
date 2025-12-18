// Sample resumes, job descriptions, and voices for interview simulation

export interface Voice {
  id: string
  name: string
  description: string
}

export const availableVoices: Voice[] = [
  // English voices
  { id: 'aura-2-thalia-en', name: 'Thalia', description: 'Female, clear & confident' },
  { id: 'aura-2-andromeda-en', name: 'Andromeda', description: 'Female, casual & expressive' },
  { id: 'aura-2-apollo-en', name: 'Apollo', description: 'Male, confident & comfortable' },
  { id: 'aura-2-athena-en', name: 'Athena', description: 'Female, wise & professional' },
  { id: 'aura-2-orion-en', name: 'Orion', description: 'Male, strong & authoritative' },
  { id: 'aura-2-luna-en', name: 'Luna', description: 'Female, soft & calming' },
  { id: 'aura-2-zeus-en', name: 'Zeus', description: 'Male, deep & powerful' },
  { id: 'aura-2-aurora-en', name: 'Aurora', description: 'Female, warm & friendly' },
  { id: 'aura-2-hermes-en', name: 'Hermes', description: 'Male, quick & energetic' },
  { id: 'aura-2-helena-en', name: 'Helena', description: 'Female, elegant & refined' },
  { id: 'aura-2-orpheus-en', name: 'Orpheus', description: 'Male, melodic & expressive' },
  { id: 'aura-2-iris-en', name: 'Iris', description: 'Female, bright & cheerful' },
  // French voices
  { id: 'aura-2-agathe-fr', name: 'Agathe (FR)', description: 'Female, cheerful & friendly' },
  { id: 'aura-2-hector-fr', name: 'Hector (FR)', description: 'Male, confident & expressive' },
]

export interface Resume {
  id: string
  name: string
  summary: string
  experience: Array<{
    title: string
    company: string
    duration: string
    responsibilities: string[]
  }>
  education: Array<{
    degree: string
    school: string
    year: string
  }>
  skills: {
    languages: string[]
    frontend: string[]
    backend: string[]
    tools: string[]
  }
  certifications: string[]
}

export interface JobDescription {
  id: string
  title: string
  company: string
  about_company: string
  about_role: string
  responsibilities: string[]
  requirements: {
    must_have: string[]
    nice_to_have: string[]
  }
  benefits: string[]
}

export const sampleResumes: Resume[] = [
  {
    id: 'alex-chen',
    name: 'Alex Chen',
    summary: 'Full-stack developer with 5 years of experience building scalable web applications. Passionate about clean code and user experience.',
    experience: [
      {
        title: 'Senior Software Engineer',
        company: 'TechCorp Inc.',
        duration: '2021 - Present',
        responsibilities: [
          'Led development of microservices architecture serving 1M+ users',
          'Mentored junior developers and conducted code reviews',
          'Implemented CI/CD pipelines reducing deployment time by 60%'
        ]
      },
      {
        title: 'Software Engineer',
        company: 'StartupXYZ',
        duration: '2019 - 2021',
        responsibilities: [
          'Built React-based dashboard for real-time analytics',
          'Developed RESTful APIs using Node.js and PostgreSQL',
          'Collaborated with design team on UI/UX improvements'
        ]
      }
    ],
    education: [
      {
        degree: 'B.S. Computer Science',
        school: 'University of California, Berkeley',
        year: '2019'
      }
    ],
    skills: {
      languages: ['TypeScript', 'Python', 'Go', 'SQL'],
      frontend: ['React', 'Vue.js', 'Next.js', 'Tailwind CSS'],
      backend: ['Node.js', 'FastAPI', 'PostgreSQL', 'Redis'],
      tools: ['Docker', 'Kubernetes', 'AWS', 'GitHub Actions']
    },
    certifications: ['AWS Solutions Architect', 'Google Cloud Professional']
  },
  {
    id: 'sarah-johnson',
    name: 'Sarah Johnson',
    summary: 'Frontend specialist with 4 years of experience creating beautiful, accessible web applications. Strong focus on performance and user experience.',
    experience: [
      {
        title: 'Frontend Developer',
        company: 'DesignStudio',
        duration: '2022 - Present',
        responsibilities: [
          'Developed component library used across 5 products',
          'Improved Lighthouse scores from 65 to 95+',
          'Implemented accessibility standards (WCAG 2.1 AA)'
        ]
      },
      {
        title: 'Junior Developer',
        company: 'WebAgency',
        duration: '2020 - 2022',
        responsibilities: [
          'Built responsive websites for 20+ clients',
          'Created animations and interactive experiences',
          'Optimized images and assets for fast loading'
        ]
      }
    ],
    education: [
      {
        degree: 'B.A. Digital Media',
        school: 'NYU',
        year: '2020'
      }
    ],
    skills: {
      languages: ['JavaScript', 'TypeScript', 'HTML', 'CSS'],
      frontend: ['React', 'Vue.js', 'Svelte', 'SCSS', 'Framer Motion'],
      backend: ['Node.js', 'Express'],
      tools: ['Figma', 'Storybook', 'Jest', 'Playwright']
    },
    certifications: ['Meta Frontend Developer', 'Google UX Design']
  },
  {
    id: 'michael-torres',
    name: 'Michael Torres',
    summary: 'Backend engineer with 6 years of experience in distributed systems and cloud infrastructure. Expert in building high-availability services.',
    experience: [
      {
        title: 'Staff Engineer',
        company: 'CloudScale',
        duration: '2020 - Present',
        responsibilities: [
          'Architected event-driven system processing 10M events/day',
          'Reduced infrastructure costs by 40% through optimization',
          'Led migration from monolith to microservices'
        ]
      },
      {
        title: 'Backend Developer',
        company: 'DataFlow Inc.',
        duration: '2018 - 2020',
        responsibilities: [
          'Built data pipelines for ML model training',
          'Implemented real-time streaming with Kafka',
          'Designed and maintained PostgreSQL databases'
        ]
      }
    ],
    education: [
      {
        degree: 'M.S. Computer Science',
        school: 'MIT',
        year: '2018'
      }
    ],
    skills: {
      languages: ['Go', 'Python', 'Rust', 'SQL'],
      frontend: ['React'],
      backend: ['gRPC', 'Kafka', 'PostgreSQL', 'MongoDB', 'Redis'],
      tools: ['Kubernetes', 'Terraform', 'AWS', 'GCP', 'Prometheus']
    },
    certifications: ['AWS DevOps Professional', 'CKA (Kubernetes)']
  }
]

export const sampleJobs: JobDescription[] = [
  {
    id: 'senior-fullstack',
    title: 'Senior Full-Stack Engineer',
    company: 'InnovateTech',
    about_company: 'InnovateTech is a fast-growing SaaS company building the next generation of productivity tools. We serve over 50,000 businesses worldwide.',
    about_role: 'We are looking for a Senior Full-Stack Engineer to join our core product team. You will work on our main web application used by thousands of users daily.',
    responsibilities: [
      'Design and implement new features end-to-end',
      'Collaborate with product and design teams',
      'Mentor junior developers',
      'Participate in architecture decisions',
      'Write clean, tested, and documented code'
    ],
    requirements: {
      must_have: [
        '5+ years of software development experience',
        'Strong proficiency in TypeScript and React',
        'Experience with Node.js or Python backends',
        'Database design experience (SQL and NoSQL)',
        'Excellent communication skills'
      ],
      nice_to_have: [
        'Experience with AWS or GCP',
        'Knowledge of CI/CD practices',
        'Experience with microservices',
        'Open source contributions'
      ]
    },
    benefits: ['Competitive salary', 'Remote-first', 'Health insurance', 'Equity']
  },
  {
    id: 'frontend-lead',
    title: 'Frontend Tech Lead',
    company: 'VisualApps',
    about_company: 'VisualApps creates design and collaboration tools for creative teams. Our products are used by designers at Fortune 500 companies.',
    about_role: 'Lead our frontend team in building beautiful, performant applications. You will set technical direction and mentor a team of 5 engineers.',
    responsibilities: [
      'Lead frontend architecture decisions',
      'Mentor and grow team members',
      'Drive performance and accessibility initiatives',
      'Collaborate with backend and design teams',
      'Ship high-quality features on schedule'
    ],
    requirements: {
      must_have: [
        '6+ years of frontend development experience',
        'Expert knowledge of React ecosystem',
        'Experience leading engineering teams',
        'Strong understanding of web performance',
        'Passion for great user experience'
      ],
      nice_to_have: [
        'Experience with canvas/WebGL',
        'Knowledge of design systems',
        'Experience with real-time collaboration',
        'Background in design'
      ]
    },
    benefits: ['Top-tier salary', 'Unlimited PTO', 'Learning budget', 'Stock options']
  },
  {
    id: 'backend-engineer',
    title: 'Backend Engineer',
    company: 'DataStream',
    about_company: 'DataStream provides real-time data infrastructure for modern applications. Our platform handles billions of events per day.',
    about_role: 'Join our infrastructure team to build and scale our core data pipeline. You will work on challenging distributed systems problems.',
    responsibilities: [
      'Build and maintain data processing pipelines',
      'Optimize system performance and reliability',
      'Design APIs for internal and external use',
      'Participate in on-call rotation',
      'Write technical documentation'
    ],
    requirements: {
      must_have: [
        '4+ years of backend development experience',
        'Proficiency in Go or Python',
        'Experience with distributed systems',
        'Knowledge of message queues (Kafka, RabbitMQ)',
        'SQL and database optimization skills'
      ],
      nice_to_have: [
        'Experience with Kubernetes',
        'Knowledge of stream processing',
        'Familiarity with observability tools',
        'Experience with high-throughput systems'
      ]
    },
    benefits: ['Competitive pay', 'Remote friendly', '401k matching', 'Conference budget']
  }
]
