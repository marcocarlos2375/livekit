// Sample resumes, job descriptions, and voices for interview simulation

export type Language = 'en' | 'fr'

export interface Voice {
  id: string
  name: string
  description: string
  language: Language
}

export const availableVoices: Voice[] = [
  // English voices
  { id: 'aura-2-thalia-en', name: 'Thalia', description: 'Female, clear & confident', language: 'en' },
  { id: 'aura-2-andromeda-en', name: 'Andromeda', description: 'Female, casual & expressive', language: 'en' },
  { id: 'aura-2-apollo-en', name: 'Apollo', description: 'Male, confident & comfortable', language: 'en' },
  { id: 'aura-2-athena-en', name: 'Athena', description: 'Female, wise & professional', language: 'en' },
  { id: 'aura-2-orion-en', name: 'Orion', description: 'Male, strong & authoritative', language: 'en' },
  { id: 'aura-2-luna-en', name: 'Luna', description: 'Female, soft & calming', language: 'en' },
  { id: 'aura-2-zeus-en', name: 'Zeus', description: 'Male, deep & powerful', language: 'en' },
  { id: 'aura-2-aurora-en', name: 'Aurora', description: 'Female, warm & friendly', language: 'en' },
  { id: 'aura-2-hermes-en', name: 'Hermes', description: 'Male, quick & energetic', language: 'en' },
  { id: 'aura-2-helena-en', name: 'Helena', description: 'Female, elegant & refined', language: 'en' },
  { id: 'aura-2-orpheus-en', name: 'Orpheus', description: 'Male, melodic & expressive', language: 'en' },
  { id: 'aura-2-iris-en', name: 'Iris', description: 'Female, bright & cheerful', language: 'en' },
  // French voices
  { id: 'aura-2-agathe-fr', name: 'Agathe', description: 'Femme, joyeuse & amicale', language: 'fr' },
  { id: 'aura-2-hector-fr', name: 'Hector', description: 'Homme, confiant & expressif', language: 'fr' },
]

export interface Resume {
  id: string
  language: Language
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
  language: Language
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
  // English resumes
  {
    id: 'alex-chen',
    language: 'en',
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
    language: 'en',
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
    language: 'en',
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
  },
  // French resumes
  {
    id: 'marie-dupont',
    language: 'fr',
    name: 'Marie Dupont',
    summary: 'Développeuse full-stack avec 5 ans d\'expérience dans la création d\'applications web performantes. Passionnée par le code propre et l\'expérience utilisateur.',
    experience: [
      {
        title: 'Ingénieure Logiciel Senior',
        company: 'TechFrance',
        duration: '2021 - Présent',
        responsibilities: [
          'Direction du développement d\'une architecture microservices pour 500K+ utilisateurs',
          'Mentorat des développeurs juniors et revues de code',
          'Mise en place de pipelines CI/CD réduisant le temps de déploiement de 50%'
        ]
      },
      {
        title: 'Développeuse Logiciel',
        company: 'StartupParis',
        duration: '2019 - 2021',
        responsibilities: [
          'Développement d\'un tableau de bord React pour l\'analyse en temps réel',
          'Création d\'APIs RESTful avec Node.js et PostgreSQL',
          'Collaboration avec l\'équipe design pour l\'amélioration UX'
        ]
      }
    ],
    education: [
      {
        degree: 'Master Informatique',
        school: 'École Polytechnique',
        year: '2019'
      }
    ],
    skills: {
      languages: ['TypeScript', 'Python', 'Java', 'SQL'],
      frontend: ['React', 'Vue.js', 'Next.js', 'Tailwind CSS'],
      backend: ['Node.js', 'Django', 'PostgreSQL', 'Redis'],
      tools: ['Docker', 'Kubernetes', 'AWS', 'GitLab CI']
    },
    certifications: ['AWS Solutions Architect', 'Scrum Master']
  },
  {
    id: 'thomas-martin',
    language: 'fr',
    name: 'Thomas Martin',
    summary: 'Ingénieur backend avec 6 ans d\'expérience en systèmes distribués et infrastructure cloud. Expert en services haute disponibilité.',
    experience: [
      {
        title: 'Lead Technique',
        company: 'CloudEurope',
        duration: '2020 - Présent',
        responsibilities: [
          'Architecture d\'un système événementiel traitant 5M événements/jour',
          'Réduction des coûts infrastructure de 35% par optimisation',
          'Migration d\'un monolithe vers une architecture microservices'
        ]
      },
      {
        title: 'Développeur Backend',
        company: 'DataTech',
        duration: '2018 - 2020',
        responsibilities: [
          'Construction de pipelines de données pour l\'entraînement ML',
          'Implémentation de streaming temps réel avec Kafka',
          'Conception et maintenance de bases PostgreSQL'
        ]
      }
    ],
    education: [
      {
        degree: 'Diplôme d\'Ingénieur',
        school: 'INSA Lyon',
        year: '2018'
      }
    ],
    skills: {
      languages: ['Go', 'Python', 'Java', 'SQL'],
      frontend: ['React'],
      backend: ['gRPC', 'Kafka', 'PostgreSQL', 'MongoDB', 'Redis'],
      tools: ['Kubernetes', 'Terraform', 'GCP', 'Prometheus']
    },
    certifications: ['GCP Professional Cloud Architect', 'CKA (Kubernetes)']
  },
  {
    id: 'sophie-bernard',
    language: 'fr',
    name: 'Sophie Bernard',
    summary: 'Spécialiste frontend avec 4 ans d\'expérience dans la création d\'applications web accessibles et performantes. Focus sur l\'UX et le design system.',
    experience: [
      {
        title: 'Développeuse Frontend Senior',
        company: 'DesignLab Paris',
        duration: '2022 - Présent',
        responsibilities: [
          'Création d\'une bibliothèque de composants utilisée sur 8 produits',
          'Amélioration des scores Lighthouse de 60 à 95+',
          'Implémentation des standards d\'accessibilité RGAA'
        ]
      },
      {
        title: 'Développeuse Frontend',
        company: 'AgenceWeb',
        duration: '2020 - 2022',
        responsibilities: [
          'Développement de sites responsive pour 30+ clients',
          'Création d\'animations et expériences interactives',
          'Optimisation des performances et du temps de chargement'
        ]
      }
    ],
    education: [
      {
        degree: 'Master Design Numérique',
        school: 'Gobelins',
        year: '2020'
      }
    ],
    skills: {
      languages: ['JavaScript', 'TypeScript', 'HTML', 'CSS'],
      frontend: ['React', 'Vue.js', 'Nuxt', 'SCSS', 'Framer Motion'],
      backend: ['Node.js', 'Express'],
      tools: ['Figma', 'Storybook', 'Jest', 'Cypress']
    },
    certifications: ['Google UX Design', 'Opquast']
  }
]

export const sampleJobs: JobDescription[] = [
  // English jobs
  {
    id: 'senior-fullstack',
    language: 'en',
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
    language: 'en',
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
    language: 'en',
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
  },
  // French jobs
  {
    id: 'ingenieur-fullstack-senior',
    language: 'fr',
    title: 'Ingénieur Full-Stack Senior',
    company: 'TechInnov',
    about_company: 'TechInnov est une entreprise SaaS en forte croissance qui développe des outils de productivité nouvelle génération. Nous servons plus de 30 000 entreprises en Europe.',
    about_role: 'Nous recherchons un Ingénieur Full-Stack Senior pour rejoindre notre équipe produit. Vous travaillerez sur notre application web principale utilisée par des milliers d\'utilisateurs quotidiennement.',
    responsibilities: [
      'Concevoir et implémenter des fonctionnalités de bout en bout',
      'Collaborer avec les équipes produit et design',
      'Encadrer les développeurs juniors',
      'Participer aux décisions d\'architecture',
      'Écrire du code propre, testé et documenté'
    ],
    requirements: {
      must_have: [
        '5+ ans d\'expérience en développement logiciel',
        'Maîtrise de TypeScript et React',
        'Expérience avec Node.js ou Python backend',
        'Expérience en conception de bases de données (SQL et NoSQL)',
        'Excellentes compétences en communication'
      ],
      nice_to_have: [
        'Expérience avec AWS ou GCP',
        'Connaissance des pratiques CI/CD',
        'Expérience avec les microservices',
        'Contributions open source'
      ]
    },
    benefits: ['Salaire compétitif', 'Télétravail flexible', 'Mutuelle', 'BSPCE']
  },
  {
    id: 'lead-frontend',
    language: 'fr',
    title: 'Lead Technique Frontend',
    company: 'DesignApps',
    about_company: 'DesignApps crée des outils de design et collaboration pour les équipes créatives. Nos produits sont utilisés par les designers des plus grandes entreprises françaises.',
    about_role: 'Dirigez notre équipe frontend dans la création d\'applications performantes et élégantes. Vous définirez la direction technique et encadrerez une équipe de 5 ingénieurs.',
    responsibilities: [
      'Diriger les décisions d\'architecture frontend',
      'Encadrer et faire progresser les membres de l\'équipe',
      'Piloter les initiatives de performance et d\'accessibilité',
      'Collaborer avec les équipes backend et design',
      'Livrer des fonctionnalités de haute qualité dans les délais'
    ],
    requirements: {
      must_have: [
        '6+ ans d\'expérience en développement frontend',
        'Expertise de l\'écosystème React',
        'Expérience en management d\'équipes techniques',
        'Solide compréhension des performances web',
        'Passion pour l\'expérience utilisateur'
      ],
      nice_to_have: [
        'Expérience avec canvas/WebGL',
        'Connaissance des design systems',
        'Expérience avec la collaboration temps réel',
        'Background en design'
      ]
    },
    benefits: ['Salaire attractif', 'RTT illimités', 'Budget formation', 'BSPCE']
  },
  {
    id: 'ingenieur-backend',
    language: 'fr',
    title: 'Ingénieur Backend',
    company: 'DataFlow',
    about_company: 'DataFlow fournit une infrastructure de données temps réel pour les applications modernes. Notre plateforme traite des milliards d\'événements par jour.',
    about_role: 'Rejoignez notre équipe infrastructure pour construire et faire évoluer notre pipeline de données. Vous travaillerez sur des problématiques complexes de systèmes distribués.',
    responsibilities: [
      'Construire et maintenir les pipelines de traitement de données',
      'Optimiser les performances et la fiabilité du système',
      'Concevoir des APIs pour usage interne et externe',
      'Participer aux astreintes',
      'Rédiger la documentation technique'
    ],
    requirements: {
      must_have: [
        '4+ ans d\'expérience en développement backend',
        'Maîtrise de Go ou Python',
        'Expérience avec les systèmes distribués',
        'Connaissance des files de messages (Kafka, RabbitMQ)',
        'Compétences en SQL et optimisation de bases de données'
      ],
      nice_to_have: [
        'Expérience avec Kubernetes',
        'Connaissance du stream processing',
        'Familiarité avec les outils d\'observabilité',
        'Expérience avec les systèmes à haut débit'
      ]
    },
    benefits: ['Rémunération compétitive', 'Télétravail', 'PEE avec abondement', 'Budget conférences']
  }
]
