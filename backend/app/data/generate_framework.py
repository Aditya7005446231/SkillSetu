"""Generate a comprehensive 200+ skill framework with roles, categories, aliases, and relations."""
import json
from pathlib import Path

SKILLS = [
    # --- PROGRAMMING LANGUAGES ---
    {
        "name": "Python",
        "category": "Programming Languages",
        "aliases": ["python3", "py", "python 3", "cpython"],
        "related": ["Django", "FastAPI", "Flask", "Pandas", "NumPy", "PyTorch"],
        "prerequisites": [],
        "description": "High-level, interpreted programming language widely used for web development, data science, AI, and automation."
    },
    {
        "name": "JavaScript",
        "category": "Programming Languages",
        "aliases": ["js", "es6", "ecmascript", "vanilla js", "modern javascript"],
        "related": ["TypeScript", "React", "Node.js", "HTML5", "CSS3"],
        "prerequisites": [],
        "description": "Core scripting language of the web, enabling interactive frontend interfaces and server-side runtimes."
    },
    {
        "name": "TypeScript",
        "category": "Programming Languages",
        "aliases": ["ts"],
        "related": ["JavaScript", "React", "Node.js", "Angular", "NestJS"],
        "prerequisites": ["JavaScript"],
        "description": "Strongly typed superset of JavaScript that compiles to plain JavaScript, enhancing maintainability."
    },
    {
        "name": "Java",
        "category": "Programming Languages",
        "aliases": ["java 8", "java 11", "java 17", "java 21", "core java", "j2se"],
        "related": ["Spring Boot", "Kotlin", "Hibernate", "Maven", "Gradle"],
        "prerequisites": ["Object-Oriented Programming"],
        "description": "Object-oriented, class-based language engineered for platform independence, enterprise backends, and Android."
    },
    {
        "name": "C++",
        "category": "Programming Languages",
        "aliases": ["cpp", "c plus plus", "c/c++"],
        "related": ["C", "Data Structures", "Algorithms", "System Design"],
        "prerequisites": ["C"],
        "description": "High-performance systems programming language with generic and object-oriented features, used in game dev and low-latency systems."
    },
    {
        "name": "C#",
        "category": "Programming Languages",
        "aliases": ["csharp", "c sharp", ".net c#"],
        "related": [".NET Core", "ASP.NET Core", "Unity", "Azure"],
        "prerequisites": ["Object-Oriented Programming"],
        "description": "Modern object-oriented language developed by Microsoft for enterprise applications, cloud services, and games."
    },
    {
        "name": "Go",
        "category": "Programming Languages",
        "aliases": ["golang", "go-lang"],
        "related": ["Docker", "Kubernetes", "gRPC", "Microservices"],
        "prerequisites": [],
        "description": "Compiled, statically typed open-source language designed by Google for scalable, concurrent network services."
    },
    {
        "name": "Rust",
        "category": "Programming Languages",
        "aliases": ["rustlang"],
        "related": ["WebAssembly", "C++", "System Programming", "Concurrency"],
        "prerequisites": [],
        "description": "Systems programming language focused on memory safety, concurrency, and performance without a garbage collector."
    },
    {
        "name": "PHP",
        "category": "Programming Languages",
        "aliases": ["php7", "php8"],
        "related": ["Laravel", "Symfony", "WordPress", "MySQL"],
        "prerequisites": [],
        "description": "Server-side scripting language designed primarily for web development and dynamic web applications."
    },
    {
        "name": "Ruby",
        "category": "Programming Languages",
        "aliases": ["ruby on rails language"],
        "related": ["Ruby on Rails", "PostgreSQL", "RSpec"],
        "prerequisites": [],
        "description": "Dynamic, open-source programming language with a focus on simplicity, productivity, and elegant syntax."
    },
    {
        "name": "Swift",
        "category": "Programming Languages",
        "aliases": ["swiftlang", "apple swift"],
        "related": ["iOS Development", "SwiftUI", "Xcode", "Objective-C"],
        "prerequisites": [],
        "description": "Modern, fast, and safe programming language created by Apple for iOS, macOS, watchOS, and tvOS development."
    },
    {
        "name": "Kotlin",
        "category": "Programming Languages",
        "aliases": ["kotlin/jvm", "android kotlin"],
        "related": ["Android Development", "Java", "Spring Boot", "Jetpack Compose"],
        "prerequisites": ["Java"],
        "description": "Modern concise language targeting JVM and Android, fully interoperable with Java and officially preferred by Google for Android."
    },
    {
        "name": "SQL",
        "category": "Programming Languages",
        "aliases": ["structured query language", "ansi sql", "relational database queries"],
        "related": ["PostgreSQL", "MySQL", "Database Indexing", "Data Modeling"],
        "prerequisites": [],
        "description": "Standard declarative query language for defining, manipulating, and querying relational database management systems."
    },
    {
        "name": "HTML5",
        "category": "Programming Languages",
        "aliases": ["html", "html 5", "markup"],
        "related": ["CSS3", "JavaScript", "Web Accessibility", "SEO"],
        "prerequisites": [],
        "description": "Standard markup language used to structure documents and content displayed on the World Wide Web."
    },
    {
        "name": "CSS3",
        "category": "Programming Languages",
        "aliases": ["css", "cascading style sheets", "css 3", "modern css"],
        "related": ["HTML5", "Tailwind CSS", "Sass", "Responsive Design", "Flexbox"],
        "prerequisites": ["HTML5"],
        "description": "Style sheet language used for specifying the visual layout, typography, animations, and presentation of web pages."
    },
    {
        "name": "Shell Scripting",
        "category": "Programming Languages",
        "aliases": ["bash", "bash scripting", "sh", "zsh", "linux shell"],
        "related": ["Linux", "CLI", "DevOps", "Automation"],
        "prerequisites": ["Linux"],
        "description": "Scripting language for Unix/Linux shells to automate server tasks, file manipulation, and deployment pipelines."
    },
    {
        "name": "R",
        "category": "Programming Languages",
        "aliases": ["r-lang", "rlang", "r programming"],
        "related": ["Data Science", "Statistics", "Machine Learning", "ggplot2"],
        "prerequisites": [],
        "description": "Statistical computing and graphics programming language widely used among data miners, statisticians, and researchers."
    },
    {
        "name": "Dart",
        "category": "Programming Languages",
        "aliases": ["dartlang"],
        "related": ["Flutter", "Mobile Development", "Cross-Platform Development"],
        "prerequisites": [],
        "description": "Client-optimized programming language developed by Google for fast apps on any platform, powering Flutter."
    },
    {
        "name": "Scala",
        "category": "Programming Languages",
        "aliases": ["scala-lang"],
        "related": ["Apache Spark", "Java", "Functional Programming", "Akka"],
        "prerequisites": ["Java"],
        "description": "High-level language combining object-oriented and functional programming paradigms, running on the JVM and central to Spark."
    },
    {
        "name": "C",
        "category": "Programming Languages",
        "aliases": ["c-lang", "ansi c", "c language"],
        "related": ["C++", "Linux", "Embedded Systems", "Operating Systems"],
        "prerequisites": [],
        "description": "Foundational low-level procedural programming language providing direct memory manipulation and hardware access."
    },

    # --- FRONTEND FRAMEWORKS & LIBRARIES ---
    {
        "name": "React",
        "category": "Frontend Development",
        "aliases": ["reactjs", "react.js", "react js"],
        "related": ["JavaScript", "TypeScript", "Next.js", "Redux", "Tailwind CSS", "React Hooks"],
        "prerequisites": ["JavaScript", "HTML5", "CSS3"],
        "description": "Declarative, component-based JavaScript library developed by Meta for building dynamic user interfaces."
    },
    {
        "name": "Next.js",
        "category": "Frontend Development",
        "aliases": ["nextjs", "next.js", "next js", "next"],
        "related": ["React", "TypeScript", "Server-Side Rendering", "Tailwind CSS", "Vercel"],
        "prerequisites": ["React"],
        "description": "Production React framework providing hybrid static and server rendering, smart routing, and full-stack API routes."
    },
    {
        "name": "Vue.js",
        "category": "Frontend Development",
        "aliases": ["vue", "vuejs", "vue 3", "vue.js"],
        "related": ["Nuxt.js", "JavaScript", "TypeScript", "Pinia", "Vite"],
        "prerequisites": ["JavaScript", "HTML5", "CSS3"],
        "description": "Progressive JavaScript framework for building user interfaces with a template-driven syntax and reactive data binding."
    },
    {
        "name": "Angular",
        "category": "Frontend Development",
        "aliases": ["angularjs", "angular 2+", "angular framework", "angular 17"],
        "related": ["TypeScript", "RxJS", "HTML5", "CSS3", "Dependency Injection"],
        "prerequisites": ["TypeScript"],
        "description": "Comprehensive, component-based TypeScript web application framework maintained by Google for enterprise web apps."
    },
    {
        "name": "Svelte",
        "category": "Frontend Development",
        "aliases": ["sveltejs", "svelte.js", "sveltekit"],
        "related": ["JavaScript", "TypeScript", "HTML5", "CSS3", "Vite"],
        "prerequisites": ["JavaScript"],
        "description": "Radical compiler-based frontend framework that converts components into tiny, imperative vanilla code without a virtual DOM."
    },
    {
        "name": "Tailwind CSS",
        "category": "Frontend Development",
        "aliases": ["tailwindcss", "tailwind", "tailwind-css"],
        "related": ["CSS3", "HTML5", "React", "Next.js", "PostCSS"],
        "prerequisites": ["CSS3"],
        "description": "Utility-first CSS framework packed with classes that can be composed directly in markup to build bespoke user interfaces."
    },
    {
        "name": "Redux",
        "category": "Frontend Development",
        "aliases": ["redux toolkit", "rtk", "redux-saga", "react-redux"],
        "related": ["React", "JavaScript", "TypeScript", "State Management"],
        "prerequisites": ["React"],
        "description": "Predictable state container for JavaScript apps, widely used with React for centralizing global application state."
    },
    {
        "name": "Zustand",
        "category": "Frontend Development",
        "aliases": ["zustand state management"],
        "related": ["React", "TypeScript", "State Management", "Redux"],
        "prerequisites": ["React"],
        "description": "Small, fast, and scalable bearbones state-management solution using simplified flux principles for React."
    },
    {
        "name": "Vite",
        "category": "Frontend Development",
        "aliases": ["vitejs", "vite.js"],
        "related": ["JavaScript", "TypeScript", "React", "Vue.js", "Webpack"],
        "prerequisites": ["JavaScript"],
        "description": "Next-generation frontend tooling providing lightning-fast Hot Module Replacement and optimized Rollup builds."
    },
    {
        "name": "Webpack",
        "category": "Frontend Development",
        "aliases": ["webpack 5", "module bundler"],
        "related": ["Babel", "JavaScript", "Vite", "Build Tools"],
        "prerequisites": ["JavaScript"],
        "description": "Static module bundler for modern JavaScript applications, compiling complex module dependency graphs into browser bundles."
    },
    {
        "name": "Sass",
        "category": "Frontend Development",
        "aliases": ["scss", "syntactically awesome stylesheets"],
        "related": ["CSS3", "Tailwind CSS", "Bootstrap"],
        "prerequisites": ["CSS3"],
        "description": "CSS preprocessor adding nested rules, variables, mixins, and functions to standard stylesheets."
    },
    {
        "name": "Bootstrap",
        "category": "Frontend Development",
        "aliases": ["bootstrap 5", "twitter bootstrap"],
        "related": ["CSS3", "HTML5", "Responsive Design"],
        "prerequisites": ["HTML5", "CSS3"],
        "description": "Popular open-source CSS and JavaScript framework for responsive, mobile-first front-end web development."
    },
    {
        "name": "React Native",
        "category": "Frontend Development",
        "aliases": ["react-native", "rn"],
        "related": ["React", "JavaScript", "TypeScript", "Mobile Development", "Expo"],
        "prerequisites": ["React"],
        "description": "Framework for building native iOS and Android applications using React and JavaScript."
    },
    {
        "name": "Responsive Design",
        "category": "Frontend Development",
        "aliases": ["mobile first design", "media queries", "adaptive design"],
        "related": ["HTML5", "CSS3", "Tailwind CSS", "Flexbox", "CSS Grid"],
        "prerequisites": ["CSS3"],
        "description": "Approach to web design making web pages render well across a variety of screen sizes and modern devices."
    },
    {
        "name": "WebSockets",
        "category": "Frontend Development",
        "aliases": ["websocket", "real-time communication", "socket.io"],
        "related": ["JavaScript", "Node.js", "Socket.io", "Real-Time Systems"],
        "prerequisites": ["JavaScript", "HTTP"],
        "description": "Computer communications protocol providing full-duplex communication channels over a single persistent TCP connection."
    },

    # --- BACKEND FRAMEWORKS & ARCHITECTURE ---
    {
        "name": "Node.js",
        "category": "Backend Development",
        "aliases": ["node", "nodejs", "node js", "node.js"],
        "related": ["JavaScript", "Express.js", "TypeScript", "NestJS", "npm"],
        "prerequisites": ["JavaScript"],
        "description": "Asynchronous event-driven JavaScript runtime environment built on Chrome's V8 engine for building scalable network apps."
    },
    {
        "name": "Express.js",
        "category": "Backend Development",
        "aliases": ["express", "expressjs", "express.js"],
        "related": ["Node.js", "REST API", "JavaScript", "Middleware"],
        "prerequisites": ["Node.js"],
        "description": "Minimalist and flexible Node.js web application framework providing robust features for web and mobile APIs."
    },
    {
        "name": "FastAPI",
        "category": "Backend Development",
        "aliases": ["fast api", "fastapi framework"],
        "related": ["Python", "Pydantic", "Uvicorn", "Starlette", "REST API", "OpenAPI"],
        "prerequisites": ["Python"],
        "description": "Modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints."
    },
    {
        "name": "Django",
        "category": "Backend Development",
        "aliases": ["django framework", "django orm", "django rest framework", "drf"],
        "related": ["Python", "PostgreSQL", "REST API", "ORM"],
        "prerequisites": ["Python"],
        "description": "High-level Python web framework that encourages rapid development and clean, pragmatic design with batteries included."
    },
    {
        "name": "Flask",
        "category": "Backend Development",
        "aliases": ["flask framework", "flask-restful"],
        "related": ["Python", "Jinja2", "Werkzeug", "REST API", "SQLAlchemy"],
        "prerequisites": ["Python"],
        "description": "Lightweight WSGI micro web framework written in Python designed to make getting started quick and easy."
    },
    {
        "name": "Spring Boot",
        "category": "Backend Development",
        "aliases": ["spring", "spring framework", "spring-boot", "springboot"],
        "related": ["Java", "Microservices", "Hibernate", "Maven", "REST API"],
        "prerequisites": ["Java"],
        "description": "Production-ready, opinionated framework on top of Java Spring that simplifies building stand-alone enterprise microservices."
    },
    {
        "name": "ASP.NET Core",
        "category": "Backend Development",
        "aliases": ["asp.net", "dotnet core", ".net core web api", "aspnet"],
        "related": ["C#", ".NET Core", "Entity Framework", "Azure", "REST API"],
        "prerequisites": ["C#"],
        "description": "Cross-platform, high-performance, open-source framework by Microsoft for building modern, cloud-enabled web applications."
    },
    {
        "name": "NestJS",
        "category": "Backend Development",
        "aliases": ["nest.js", "nestjs framework"],
        "related": ["TypeScript", "Node.js", "Express.js", "Microservices", "TypeORM"],
        "prerequisites": ["TypeScript", "Node.js"],
        "description": "Progressive Node.js framework for building efficient, reliable, and scalable server-side applications with TypeScript."
    },
    {
        "name": "REST API",
        "category": "Backend Development",
        "aliases": ["rest", "restful", "restful api", "rest api development"],
        "related": ["HTTP", "JSON", "OpenAPI", "API Design", "Postman"],
        "prerequisites": ["HTTP"],
        "description": "Architectural style for network applications using stateless HTTP methods (GET, POST, PUT, DELETE) to access resources."
    },
    {
        "name": "GraphQL",
        "category": "Backend Development",
        "aliases": ["gql", "apollo graphql"],
        "related": ["REST API", "Apollo Server", "Node.js", "TypeScript", "React"],
        "prerequisites": ["REST API"],
        "description": "Query language for APIs and runtime for fulfilling queries with existing data, giving clients power to request exact fields."
    },
    {
        "name": "gRPC",
        "category": "Backend Development",
        "aliases": ["grpc framework", "protocol buffers", "protobuf"],
        "related": ["Protocol Buffers", "Microservices", "Go", "HTTP/2", "C++"],
        "prerequisites": ["Microservices"],
        "description": "High-performance, open-source universal RPC framework developed by Google running on HTTP/2 with Protocol Buffers."
    },
    {
        "name": "Microservices",
        "category": "Backend Development",
        "aliases": ["microservice architecture", "distributed services"],
        "related": ["Docker", "Kubernetes", "gRPC", "API Gateway", "Kafka", "REST API"],
        "prerequisites": ["System Design", "REST API"],
        "description": "Architectural style structuring an application as a collection of loosely coupled, independently deployable services."
    },
    {
        "name": "API Gateway",
        "category": "Backend Development",
        "aliases": ["reverse proxy gateway", "kong", "aws api gateway"],
        "related": ["Microservices", "REST API", "Reverse Proxy", "Rate Limiting"],
        "prerequisites": ["Microservices"],
        "description": "Management tool sitting between a client and a collection of backend microservices, handling routing and security."
    },
    {
        "name": "Celery",
        "category": "Backend Development",
        "aliases": ["celery task queue", "python celery"],
        "related": ["Python", "Redis", "RabbitMQ", "Asynchronous Processing"],
        "prerequisites": ["Python", "Redis"],
        "description": "Distributed task queue software focused on real-time processing and asynchronous task execution in Python."
    },
    {
        "name": "Pydantic",
        "category": "Backend Development",
        "aliases": ["pydantic v2", "python pydantic"],
        "related": ["Python", "FastAPI", "Data Validation", "Type Hints"],
        "prerequisites": ["Python"],
        "description": "Data validation and settings management library using Python type annotations with fast Rust-powered validation."
    },

    # --- DATABASES & STORAGE ---
    {
        "name": "PostgreSQL",
        "category": "Databases",
        "aliases": ["postgres", "pgsql", "postgresql db"],
        "related": ["SQL", "Database Indexing", "Prisma", "Supabase", "Relational Databases"],
        "prerequisites": ["SQL"],
        "description": "Powerful, open-source object-relational database system known for reliability, feature robustness, and ACID compliance."
    },
    {
        "name": "MySQL",
        "category": "Databases",
        "aliases": ["my-sql", "mariadb"],
        "related": ["SQL", "Relational Databases", "PHP", "Database Indexing"],
        "prerequisites": ["SQL"],
        "description": "Widely used open-source relational database management system powering major web applications and CMS platforms."
    },
    {
        "name": "MongoDB",
        "category": "Databases",
        "aliases": ["mongo", "mongodb atlas", "nosql mongo"],
        "related": ["NoSQL", "Mongoose", "JSON", "Document Databases", "Node.js"],
        "prerequisites": ["JSON"],
        "description": "Leading document-oriented NoSQL database that stores data in flexible, JSON-like BSON documents."
    },
    {
        "name": "Redis",
        "category": "Databases",
        "aliases": ["redis cache", "redis key-value"],
        "related": ["Caching", "In-Memory Databases", "Celery", "Pub/Sub"],
        "prerequisites": [],
        "description": "In-memory data structure store used as a distributed cache, message broker, and quick key-value database."
    },
    {
        "name": "SQLite",
        "category": "Databases",
        "aliases": ["sqlite3"],
        "related": ["SQL", "Embedded Databases", "Python", "Mobile Development"],
        "prerequisites": ["SQL"],
        "description": "C-language library implementing a small, fast, self-contained, high-reliability, full-featured SQL database engine."
    },
    {
        "name": "Elasticsearch",
        "category": "Databases",
        "aliases": ["elastic search", "elastic", "elk stack"],
        "related": ["Logstash", "Kibana", "Full-Text Search", "Lucene"],
        "prerequisites": ["JSON"],
        "description": "Distributed, RESTful search and analytics engine capable of addressing complex full-text search use cases."
    },
    {
        "name": "DynamoDB",
        "category": "Databases",
        "aliases": ["amazon dynamodb", "aws dynamodb"],
        "related": ["AWS", "NoSQL", "Key-Value Stores", "Serverless"],
        "prerequisites": ["NoSQL"],
        "description": "Fully managed, serverless, key-value NoSQL database designed by AWS for single-digit millisecond performance."
    },
    {
        "name": "Cassandra",
        "category": "Databases",
        "aliases": ["apache cassandra", "cql"],
        "related": ["NoSQL", "Distributed Systems", "Wide-Column Store", "Big Data"],
        "prerequisites": ["Distributed Systems"],
        "description": "Open-source distributed NoSQL wide-column store designed to handle large amounts of data across many commodity servers."
    },
    {
        "name": "Supabase",
        "category": "Databases",
        "aliases": ["supabase backend", "firebase alternative"],
        "related": ["PostgreSQL", "Row Level Security", "Authentication", "Next.js"],
        "prerequisites": ["PostgreSQL"],
        "description": "Open-source Firebase alternative providing a Postgres database, real-time subscriptions, auth, and auto-generated APIs."
    },
    {
        "name": "Firebase",
        "category": "Databases",
        "aliases": ["google firebase", "firebase firestore", "realtime database"],
        "related": ["Firestore", "Authentication", "Cloud Functions", "Mobile Development"],
        "prerequisites": ["JavaScript"],
        "description": "Platform developed by Google for creating mobile and web applications, featuring Firestore and serverless hosting."
    },
    {
        "name": "Prisma",
        "category": "Databases",
        "aliases": ["prisma orm", "prisma client"],
        "related": ["TypeScript", "Node.js", "PostgreSQL", "MySQL", "ORM"],
        "prerequisites": ["TypeScript", "SQL"],
        "description": "Next-generation ORM for Node.js and TypeScript, offering declarative models, automated migrations, and type-safe queries."
    },
    {
        "name": "SQLAlchemy",
        "category": "Databases",
        "aliases": ["sqlalchemy orm"],
        "related": ["Python", "PostgreSQL", "FastAPI", "ORM"],
        "prerequisites": ["Python", "SQL"],
        "description": "Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL."
    },
    {
        "name": "Database Indexing",
        "category": "Databases",
        "aliases": ["b-tree index", "query optimization", "db indexes"],
        "related": ["SQL", "PostgreSQL", "Query Optimization", "Database Administration"],
        "prerequisites": ["SQL"],
        "description": "Data structures and techniques applied to database columns to drastically improve query speed and search operations."
    },
    {
        "name": "Snowflake",
        "category": "Databases",
        "aliases": ["snowflake data warehouse", "snowflake cloud"],
        "related": ["Data Warehousing", "SQL", "ETL", "Cloud Data Platform"],
        "prerequisites": ["SQL"],
        "description": "Cloud-based data warehousing platform providing instant elasticity, secure data sharing, and per-second pricing."
    },
    {
        "name": "BigQuery",
        "category": "Databases",
        "aliases": ["google bigquery", "gcp bigquery"],
        "related": ["Google Cloud Platform", "SQL", "Data Analytics", "Data Warehousing"],
        "prerequisites": ["SQL"],
        "description": "Fully managed, serverless enterprise data warehouse by Google for analytics over petabytes of data using SQL."
    },

    # --- CLOUD, DEVOPS & INFRASTRUCTURE ---
    {
        "name": "Docker",
        "category": "DevOps & Cloud",
        "aliases": ["docker container", "docker-compose", "containerization"],
        "related": ["Kubernetes", "Linux", "CI/CD", "Microservices"],
        "prerequisites": ["Linux"],
        "description": "Platform that uses OS-level virtualization to deliver software in standardized packages called containers."
    },
    {
        "name": "Kubernetes",
        "category": "DevOps & Cloud",
        "aliases": ["k8s", "k8s cluster", "kube"],
        "related": ["Docker", "Helm", "Cloud Computing", "DevOps", "Microservices"],
        "prerequisites": ["Docker"],
        "description": "Open-source container orchestration system for automating application deployment, scaling, and management."
    },
    {
        "name": "AWS",
        "category": "DevOps & Cloud",
        "aliases": ["amazon web services", "amazon cloud"],
        "related": ["Amazon EC2", "Amazon S3", "AWS Lambda", "Cloud Computing", "IAM"],
        "prerequisites": ["Networking Basics"],
        "description": "Comprehensive, evolving cloud computing platform provided by Amazon offering IaaS, PaaS, and serverless solutions."
    },
    {
        "name": "Amazon EC2",
        "category": "DevOps & Cloud",
        "aliases": ["ec2", "aws ec2", "elastic compute cloud"],
        "related": ["AWS", "Linux", "Virtual Machines", "Cloud Computing"],
        "prerequisites": ["AWS", "Linux"],
        "description": "Web service providing resizable compute capacity in the cloud, designed to make web-scale cloud computing easier."
    },
    {
        "name": "Amazon S3",
        "category": "DevOps & Cloud",
        "aliases": ["s3", "aws s3", "simple storage service"],
        "related": ["AWS", "Cloud Storage", "Object Storage", "CDN"],
        "prerequisites": ["AWS"],
        "description": "Scalable object storage service from AWS offering industry-leading scalability, data availability, and security."
    },
    {
        "name": "AWS Lambda",
        "category": "DevOps & Cloud",
        "aliases": ["lambda", "aws serverless", "serverless functions"],
        "related": ["AWS", "Serverless", "Python", "Node.js", "API Gateway"],
        "prerequisites": ["AWS"],
        "description": "Serverless event-driven compute service that lets you run code for virtually any type of application without provisioning servers."
    },
    {
        "name": "Google Cloud Platform",
        "category": "DevOps & Cloud",
        "aliases": ["gcp", "google cloud"],
        "related": ["BigQuery", "Kubernetes", "Cloud Run", "Cloud Storage"],
        "prerequisites": ["Networking Basics"],
        "description": "Suite of cloud computing services offered by Google that runs on the same infrastructure that Google uses internally."
    },
    {
        "name": "Microsoft Azure",
        "category": "DevOps & Cloud",
        "aliases": ["azure", "ms azure", "azure cloud"],
        "related": ["Active Directory", "C#", "Cloud Computing", "DevOps"],
        "prerequisites": ["Networking Basics"],
        "description": "Cloud computing platform by Microsoft for application management via Microsoft-managed data centers."
    },
    {
        "name": "CI/CD",
        "category": "DevOps & Cloud",
        "aliases": ["continuous integration", "continuous deployment", "cicd pipelines"],
        "related": ["GitHub Actions", "GitLab CI", "Jenkins", "Docker", "DevOps"],
        "prerequisites": ["Git"],
        "description": "Method to frequently deliver apps to customers by introducing automation into the stages of app development."
    },
    {
        "name": "GitHub Actions",
        "category": "DevOps & Cloud",
        "aliases": ["gh actions", "github ci"],
        "related": ["Git", "GitHub", "CI/CD", "YAML", "DevOps"],
        "prerequisites": ["Git", "CI/CD"],
        "description": "Continuous integration and continuous delivery platform that allows you to automate your build, test, and deployment pipeline."
    },
    {
        "name": "GitLab CI",
        "category": "DevOps & Cloud",
        "aliases": ["gitlab ci/cd", "gitlab pipeline"],
        "related": ["GitLab", "CI/CD", "Docker", "DevOps"],
        "prerequisites": ["Git", "CI/CD"],
        "description": "Built-in continuous integration and deployment engine of GitLab for testing and releasing software."
    },
    {
        "name": "Jenkins",
        "category": "DevOps & Cloud",
        "aliases": ["jenkins ci"],
        "related": ["CI/CD", "Java", "Groovy", "DevOps", "Docker"],
        "prerequisites": ["CI/CD"],
        "description": "Open-source automation server enabling developers to reliably build, test, and deploy their software."
    },
    {
        "name": "Terraform",
        "category": "DevOps & Cloud",
        "aliases": ["hashicorp terraform", "iac terraform"],
        "related": ["Infrastructure as Code", "AWS", "Azure", "GCP", "DevOps"],
        "prerequisites": ["Cloud Computing"],
        "description": "Open-source infrastructure as code software tool that provides a consistent CLI workflow to manage cloud services."
    },
    {
        "name": "Ansible",
        "category": "DevOps & Cloud",
        "aliases": ["red hat ansible"],
        "related": ["Infrastructure as Code", "Linux", "DevOps", "Automation", "YAML"],
        "prerequisites": ["Linux"],
        "description": "Open-source IT automation engine that automates cloud provisioning, configuration management, and application deployment."
    },
    {
        "name": "Linux",
        "category": "DevOps & Cloud",
        "aliases": ["linux administration", "ubuntu", "debian", "rhel", "centos"],
        "related": ["Shell Scripting", "Docker", "System Administration", "Networking Basics"],
        "prerequisites": [],
        "description": "Family of open-source Unix-like operating systems based on the Linux kernel, dominant across servers and containers."
    },
    {
        "name": "Nginx",
        "category": "DevOps & Cloud",
        "aliases": ["engine-x", "nginx web server", "nginx reverse proxy"],
        "related": ["Reverse Proxy", "Load Balancing", "SSL/TLS", "HTTP"],
        "prerequisites": ["Networking Basics"],
        "description": "Web server that can also be used as a reverse proxy, load balancer, mail proxy, and HTTP cache."
    },
    {
        "name": "Prometheus",
        "category": "DevOps & Cloud",
        "aliases": ["prometheus monitoring"],
        "related": ["Grafana", "Monitoring", "Alertmanager", "DevOps", "Kubernetes"],
        "prerequisites": ["Monitoring"],
        "description": "Open-source systems monitoring and alerting toolkit originally built at SoundCloud with a dimensional time-series data model."
    },
    {
        "name": "Grafana",
        "category": "DevOps & Cloud",
        "aliases": ["grafana dashboards"],
        "related": ["Prometheus", "Monitoring", "Time Series", "DevOps"],
        "prerequisites": ["Monitoring"],
        "description": "Multi-platform open-source analytics and interactive visualization web application for time-series infrastructure metrics."
    },
    {
        "name": "Helm",
        "category": "DevOps & Cloud",
        "aliases": ["helm charts", "kubernetes helm"],
        "related": ["Kubernetes", "DevOps", "YAML"],
        "prerequisites": ["Kubernetes"],
        "description": "Package manager for Kubernetes that helps you define, install, and upgrade even the most complex Kubernetes applications."
    },
    {
        "name": "Cloudflare",
        "category": "DevOps & Cloud",
        "aliases": ["cloudflare workers", "cloudflare cdn"],
        "related": ["CDN", "DNS", "Web Security", "Serverless"],
        "prerequisites": ["Networking Basics"],
        "description": "Global network platform providing content delivery network (CDN) services, DDoS mitigation, and edge worker computing."
    },

    # --- AI, MACHINE LEARNING & DATA SCIENCE ---
    {
        "name": "Machine Learning",
        "category": "AI & Data Science",
        "aliases": ["ml", "applied machine learning", "statistical learning"],
        "related": ["Python", "Scikit-Learn", "Deep Learning", "Data Science", "Feature Engineering"],
        "prerequisites": ["Python", "Linear Algebra", "Calculus", "Statistics"],
        "description": "Subfield of artificial intelligence focused on building systems that learn from data to improve performance on tasks."
    },
    {
        "name": "Deep Learning",
        "category": "AI & Data Science",
        "aliases": ["dl", "neural networks", "artificial neural networks"],
        "related": ["PyTorch", "TensorFlow", "Computer Vision", "NLP", "Machine Learning"],
        "prerequisites": ["Machine Learning"],
        "description": "Subset of machine learning based on artificial neural networks with multiple representation layers."
    },
    {
        "name": "Natural Language Processing",
        "category": "AI & Data Science",
        "aliases": ["nlp", "text processing", "computational linguistics"],
        "related": ["Large Language Models", "Transformers", "spaCy", "Tokenization", "Embeddings"],
        "prerequisites": ["Machine Learning"],
        "description": "Interdisciplinary subfield of computer science and AI concerned with the interactions between computers and human language."
    },
    {
        "name": "Computer Vision",
        "category": "AI & Data Science",
        "aliases": ["cv", "image processing", "vision ai"],
        "related": ["OpenCV", "Deep Learning", "Convolutional Neural Networks", "PyTorch"],
        "prerequisites": ["Deep Learning"],
        "description": "Field of artificial intelligence enabling computers and systems to derive meaningful information from digital images and videos."
    },
    {
        "name": "PyTorch",
        "category": "AI & Data Science",
        "aliases": ["torch", "pytorch framework"],
        "related": ["Python", "Deep Learning", "CUDA", "TensorFlow", "Hugging Face"],
        "prerequisites": ["Python", "Deep Learning"],
        "description": "Optimized tensor library for deep learning using GPUs and CPUs, favored by researchers and modern AI engineers."
    },
    {
        "name": "TensorFlow",
        "category": "AI & Data Science",
        "aliases": ["tf", "tensorflow 2", "keras"],
        "related": ["Keras", "Deep Learning", "Python", "PyTorch"],
        "prerequisites": ["Python", "Deep Learning"],
        "description": "End-to-end open-source machine learning platform developed by Google for research and production deployment."
    },
    {
        "name": "Scikit-Learn",
        "category": "AI & Data Science",
        "aliases": ["sklearn", "scikit learn"],
        "related": ["Python", "Machine Learning", "NumPy", "Pandas", "Model Evaluation"],
        "prerequisites": ["Python", "NumPy"],
        "description": "Simple and efficient tools for predictive data analysis and classical machine learning algorithms in Python."
    },
    {
        "name": "Pandas",
        "category": "AI & Data Science",
        "aliases": ["python pandas", "dataframes"],
        "related": ["Python", "NumPy", "Data Analysis", "Data Cleaning"],
        "prerequisites": ["Python"],
        "description": "Fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation library built on top of Python."
    },
    {
        "name": "NumPy",
        "category": "AI & Data Science",
        "aliases": ["numpy array", "python numpy"],
        "related": ["Python", "Linear Algebra", "SciPy", "Pandas"],
        "prerequisites": ["Python"],
        "description": "Fundamental package for scientific computing in Python, providing support for large multidimensional arrays and matrices."
    },
    {
        "name": "Large Language Models",
        "category": "AI & Data Science",
        "aliases": ["llm", "llms", "generative ai", "genai", "foundation models"],
        "related": ["Prompt Engineering", "RAG", "Embeddings", "Hugging Face", "LangChain"],
        "prerequisites": ["Deep Learning", "Natural Language Processing"],
        "description": "Advanced neural network models trained on vast corpora of text capable of natural language understanding and generation."
    },
    {
        "name": "RAG",
        "category": "AI & Data Science",
        "aliases": ["retrieval augmented generation", "retrieval-augmented generation", "rag pipeline"],
        "related": ["Vector Embeddings", "Vector Databases", "Large Language Models", "LangChain", "Groq"],
        "prerequisites": ["Large Language Models", "Vector Embeddings"],
        "description": "Technique for enhancing LLM responses by retrieving relevant facts from an external knowledge base before generating text."
    },
    {
        "name": "Vector Embeddings",
        "category": "AI & Data Science",
        "aliases": ["embeddings", "dense vectors", "sentence embeddings"],
        "related": ["Sentence Transformers", "Cosine Similarity", "Vector Databases", "NLP"],
        "prerequisites": ["Machine Learning"],
        "description": "Numerical representations of text, audio, or images where semantic similarity corresponds to geometric proximity in vector space."
    },
    {
        "name": "Sentence Transformers",
        "category": "AI & Data Science",
        "aliases": ["sentence-transformers", "sbert", "minilm"],
        "related": ["Vector Embeddings", "PyTorch", "Hugging Face", "RAG"],
        "prerequisites": ["PyTorch", "Vector Embeddings"],
        "description": "Python framework for state-of-the-art sentence, text, and image embeddings based on BERT architectures."
    },
    {
        "name": "LangChain",
        "category": "AI & Data Science",
        "aliases": ["langchain framework", "langgraph"],
        "related": ["Large Language Models", "RAG", "Prompt Engineering", "LlamaIndex"],
        "prerequisites": ["Python", "Large Language Models"],
        "description": "Framework designed to simplify the creation of applications using large language models, agents, and chained pipelines."
    },
    {
        "name": "LlamaIndex",
        "category": "AI & Data Science",
        "aliases": ["gpt index", "llamaindex"],
        "related": ["Large Language Models", "RAG", "Vector Databases", "LangChain"],
        "prerequisites": ["Python", "Large Language Models"],
        "description": "Data framework for LLM-based applications to ingest, structure, and access private or domain-specific data."
    },
    {
        "name": "Prompt Engineering",
        "category": "AI & Data Science",
        "aliases": ["prompt design", "few-shot prompting", "chain-of-thought"],
        "related": ["Large Language Models", "Generative AI", "RAG"],
        "prerequisites": [],
        "description": "Discipline of structuring inputs for generative AI models to elicit optimal, structured, and accurate outputs."
    },
    {
        "name": "Hugging Face",
        "category": "AI & Data Science",
        "aliases": ["huggingface", "transformers library", "hf hub"],
        "related": ["PyTorch", "Transformers", "NLP", "Open-Source AI"],
        "prerequisites": ["Python", "Machine Learning"],
        "description": "Platform and open-source library ecosystem providing pre-trained models, datasets, and tools for machine learning practitioners."
    },
    {
        "name": "OpenAI API",
        "category": "AI & Data Science",
        "aliases": ["gpt-4", "chatgpt api", "openai python"],
        "related": ["Large Language Models", "Prompt Engineering", "RAG"],
        "prerequisites": ["REST API"],
        "description": "Cloud API providing access to cutting-edge generative language and vision models developed by OpenAI."
    },
    {
        "name": "Groq",
        "category": "AI & Data Science",
        "aliases": ["groqcloud", "groq lpu", "groq api"],
        "related": ["Large Language Models", "LPU", "Inference Acceleration", "FastAPI"],
        "prerequisites": ["REST API"],
        "description": "Ultra-low latency inference engine running on custom LPU (Language Processing Unit) hardware for rapid LLM generation."
    },
    {
        "name": "MLOps",
        "category": "AI & Data Science",
        "aliases": ["machine learning operations", "ml lifecycle"],
        "related": ["Machine Learning", "Docker", "CI/CD", "MLflow", "Model Deployment"],
        "prerequisites": ["Machine Learning", "DevOps & Cloud"],
        "description": "Practices that unify machine learning system development and machine learning system operations to automate deployment."
    },
    {
        "name": "MLflow",
        "category": "AI & Data Science",
        "aliases": ["mlflow tracking"],
        "related": ["MLOps", "Machine Learning", "Experiment Tracking", "Model Registry"],
        "prerequisites": ["Machine Learning"],
        "description": "Open-source platform for managing the end-to-end machine learning lifecycle, including experiment tracking and packaging."
    },
    {
        "name": "Feature Engineering",
        "category": "AI & Data Science",
        "aliases": ["feature extraction", "feature selection"],
        "related": ["Machine Learning", "Pandas", "Scikit-Learn", "Data Preprocessing"],
        "prerequisites": ["Machine Learning"],
        "description": "Process of using domain knowledge to extract features from raw data via data mining techniques to improve model accuracy."
    },
    {
        "name": "Model Evaluation",
        "category": "AI & Data Science",
        "aliases": ["cross-validation", "metrics", "roc-auc", "f1-score"],
        "related": ["Machine Learning", "Scikit-Learn", "Statistics"],
        "prerequisites": ["Machine Learning"],
        "description": "Systematic process of assessing a machine learning model's performance on holdout data using statistical metrics."
    },
    {
        "name": "OpenCV",
        "category": "AI & Data Science",
        "aliases": ["cv2", "open source computer vision"],
        "related": ["Computer Vision", "Python", "C++", "Image Processing"],
        "prerequisites": ["Python", "NumPy"],
        "description": "Open-source computer vision and machine learning software library with thousands of optimized algorithms."
    },
    {
        "name": "Fine-Tuning",
        "category": "AI & Data Science",
        "aliases": ["model fine-tuning", "lora", "qlora", "peft"],
        "related": ["Large Language Models", "PyTorch", "Hugging Face", "Deep Learning"],
        "prerequisites": ["Large Language Models", "PyTorch"],
        "description": "Process of taking a pre-trained model and adapting its weights on a specialized dataset to improve domain-specific performance."
    },

    # --- DATA ENGINEERING & BIG DATA ---
    {
        "name": "Apache Spark",
        "category": "Data Engineering",
        "aliases": ["spark", "pyspark", "spark sql"],
        "related": ["Hadoop", "Scala", "Python", "Data Pipelines", "Big Data"],
        "prerequisites": ["Python", "SQL"],
        "description": "Multi-language unified analytics engine for large-scale data processing and machine learning."
    },
    {
        "name": "Apache Kafka",
        "category": "Data Engineering",
        "aliases": ["kafka", "kafka streaming", "event streaming"],
        "related": ["Distributed Systems", "Message Queues", "Microservices", "Event-Driven Architecture"],
        "prerequisites": ["Distributed Systems"],
        "description": "Distributed event store and stream-processing platform capable of handling trillions of events a day."
    },
    {
        "name": "Apache Airflow",
        "category": "Data Engineering",
        "aliases": ["airflow", "workflow orchestration"],
        "related": ["Python", "ETL", "Data Pipelines", "DAGs"],
        "prerequisites": ["Python"],
        "description": "Platform created to programmatically author, schedule, and monitor complex data engineering workflows."
    },
    {
        "name": "ETL",
        "category": "Data Engineering",
        "aliases": ["extract transform load", "data ingestion", "elt"],
        "related": ["Data Pipelines", "SQL", "Apache Airflow", "Data Warehousing"],
        "prerequisites": ["SQL"],
        "description": "General procedure of copying data from one or more sources into a destination system which represents the data differently."
    },
    {
        "name": "Data Pipelines",
        "category": "Data Engineering",
        "aliases": ["data engineering pipelines", "stream processing", "batch processing"],
        "related": ["ETL", "Apache Kafka", "Apache Spark", "Apache Airflow"],
        "prerequisites": ["SQL", "Python"],
        "description": "Automated pathways that extract, transform, and transfer data between software systems for analytics or operational use."
    },
    {
        "name": "dbt",
        "category": "Data Engineering",
        "aliases": ["data build tool", "dbt-core"],
        "related": ["SQL", "Snowflake", "BigQuery", "Data Transformation"],
        "prerequisites": ["SQL"],
        "description": "Development framework that combines modular SQL with software engineering best practices to transform data in your warehouse."
    },
    {
        "name": "RabbitMQ",
        "category": "Data Engineering",
        "aliases": ["amqp broker", "rabbitmq queue"],
        "related": ["Message Queues", "Celery", "Distributed Systems", "Microservices"],
        "prerequisites": ["Microservices"],
        "description": "Reliable and mature open-source message broker that supports multiple messaging protocols."
    },
    {
        "name": "Data Warehousing",
        "category": "Data Engineering",
        "aliases": ["edw", "data warehouse architecture", "star schema"],
        "related": ["Snowflake", "BigQuery", "SQL", "ETL", "Data Modeling"],
        "prerequisites": ["SQL"],
        "description": "Central repositories of integrated data from one or more disparate sources designed for query and analysis."
    },

    # --- MOBILE & CROSS-PLATFORM ---
    {
        "name": "Flutter",
        "category": "Mobile Development",
        "aliases": ["flutter framework", "flutter sdk"],
        "related": ["Dart", "Cross-Platform Development", "Mobile UI Design", "React Native"],
        "prerequisites": ["Dart"],
        "description": "Open-source UI software development kit created by Google used to develop cross-platform applications from a single codebase."
    },
    {
        "name": "Android Development",
        "category": "Mobile Development",
        "aliases": ["android sdk", "android studio", "native android"],
        "related": ["Kotlin", "Java", "Jetpack Compose", "Mobile Development"],
        "prerequisites": ["Kotlin"],
        "description": "Building mobile applications specifically tailored for Google's Android operating system."
    },
    {
        "name": "iOS Development",
        "category": "Mobile Development",
        "aliases": ["ios sdk", "native ios", "apple app development"],
        "related": ["Swift", "SwiftUI", "Xcode", "Mobile Development"],
        "prerequisites": ["Swift"],
        "description": "Engineering native mobile applications for Apple iPhone and iPad hardware using Swift and Xcode."
    },
    {
        "name": "Jetpack Compose",
        "category": "Mobile Development",
        "aliases": ["android compose", "compose ui"],
        "related": ["Kotlin", "Android Development", "Declarative UI"],
        "prerequisites": ["Kotlin", "Android Development"],
        "description": "Modern declarative UI toolkit designed by Google to simplify and accelerate UI development on Android."
    },
    {
        "name": "SwiftUI",
        "category": "Mobile Development",
        "aliases": ["apple swiftui"],
        "related": ["Swift", "iOS Development", "Declarative UI"],
        "prerequisites": ["Swift", "iOS Development"],
        "description": "Innovative, exceptionally simple way to build user interfaces across all Apple platforms with the power of Swift."
    },

    # --- SECURITY & AUTHENTICATION ---
    {
        "name": "OAuth 2.0",
        "category": "Cybersecurity",
        "aliases": ["oauth", "oauth2", "open authorization"],
        "related": ["OpenID Connect", "JWT", "Authentication", "API Security"],
        "prerequisites": ["HTTP"],
        "description": "Industry-standard authorization protocol enabling applications to obtain limited access to user accounts on HTTP services."
    },
    {
        "name": "JWT",
        "category": "Cybersecurity",
        "aliases": ["json web tokens", "jwt token", "jwt authentication"],
        "related": ["Authentication", "OAuth 2.0", "Web Security", "REST API"],
        "prerequisites": ["JSON"],
        "description": "Compact, URL-safe means of representing claims to be transferred between two parties securely using cryptography."
    },
    {
        "name": "Web Security",
        "category": "Cybersecurity",
        "aliases": ["appsec", "application security", "owasp"],
        "related": ["OWASP Top 10", "XSS", "CSRF", "SQL Injection", "HTTPS"],
        "prerequisites": ["HTTP", "Web Development"],
        "description": "Protective measures and protocols designed to shield websites and web applications from malicious cyber attacks and data breaches."
    },
    {
        "name": "Row Level Security",
        "category": "Cybersecurity",
        "aliases": ["rls", "postgres rls", "row security"],
        "related": ["PostgreSQL", "Supabase", "SQL", "Authorization"],
        "prerequisites": ["PostgreSQL"],
        "description": "Database security mechanism that controls user access to rows in a database table based on the executing user's credentials."
    },
    {
        "name": "SSL/TLS",
        "category": "Cybersecurity",
        "aliases": ["https", "tls certificates", "ssl certificates"],
        "related": ["Cryptography", "Networking Basics", "Nginx", "Web Security"],
        "prerequisites": ["Networking Basics"],
        "description": "Cryptographic protocols designed to provide communications security over a computer network."
    },

    # --- CORE CS, TESTING & SYSTEM DESIGN ---
    {
        "name": "Data Structures",
        "category": "Computer Science Core",
        "aliases": ["dsa", "arrays", "trees", "graphs", "hash tables"],
        "related": ["Algorithms", "Problem Solving", "C++", "Java", "Python"],
        "prerequisites": [],
        "description": "Specialized formats for organizing, processing, retrieving, and storing data efficiently in memory."
    },
    {
        "name": "Algorithms",
        "category": "Computer Science Core",
        "aliases": ["algorithm design", "sorting algorithms", "graph algorithms", "dynamic programming"],
        "related": ["Data Structures", "Time Complexity", "Big-O Notation"],
        "prerequisites": ["Data Structures"],
        "description": "Step-by-step procedures or formulas for solving problems and performing computations with optimal time and space complexity."
    },
    {
        "name": "System Design",
        "category": "Computer Science Core",
        "aliases": ["high level design", "hld", "distributed system architecture", "scalability"],
        "related": ["Microservices", "Load Balancing", "Caching", "Database Indexing", "Message Queues"],
        "prerequisites": ["Computer Networks", "Databases"],
        "description": "Process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements at scale."
    },
    {
        "name": "Object-Oriented Programming",
        "category": "Computer Science Core",
        "aliases": ["oop", "oops", "object oriented design"],
        "related": ["Java", "C++", "Design Patterns", "SOLID Principles"],
        "prerequisites": [],
        "description": "Programming paradigm based on the concept of objects containing data and code, following encapsulation, inheritance, and polymorphism."
    },
    {
        "name": "Design Patterns",
        "category": "Computer Science Core",
        "aliases": ["software design patterns", "gang of four", "gof"],
        "related": ["Object-Oriented Programming", "System Design", "Refactoring"],
        "prerequisites": ["Object-Oriented Programming"],
        "description": "General, reusable solutions to commonly occurring problems within a given context in software design."
    },
    {
        "name": "Git",
        "category": "Developer Tools",
        "aliases": ["git version control", "version control", "vcs"],
        "related": ["GitHub", "GitLab", "CI/CD", "Branching Strategies"],
        "prerequisites": [],
        "description": "Distributed version control system designed to track changes in source code during software development."
    },
    {
        "name": "GitHub",
        "category": "Developer Tools",
        "aliases": ["github pull requests", "github repositories"],
        "related": ["Git", "GitHub Actions", "Open Source", "Code Review"],
        "prerequisites": ["Git"],
        "description": "Cloud-based hosting service that lets developers store and manage their code using Git and collaborate on projects."
    },
    {
        "name": "Unit Testing",
        "category": "Testing & QA",
        "aliases": ["unit tests", "automated testing", "tdd"],
        "related": ["Pytest", "Jest", "Test-Driven Development", "Mocking"],
        "prerequisites": [],
        "description": "Software testing method by which individual units of source code are tested to determine whether they are fit for use."
    },
    {
        "name": "Pytest",
        "category": "Testing & QA",
        "aliases": ["pytest framework", "python pytest"],
        "related": ["Python", "Unit Testing", "Mocking", "Test Automation"],
        "prerequisites": ["Python", "Unit Testing"],
        "description": "Mature, full-featured Python testing tool that helps you write better programs and scale from simple unit tests to complex functional suites."
    },
    {
        "name": "Jest",
        "category": "Testing & QA",
        "aliases": ["jest testing", "jest framework"],
        "related": ["JavaScript", "React", "TypeScript", "Unit Testing"],
        "prerequisites": ["JavaScript", "Unit Testing"],
        "description": "Delightful JavaScript testing framework with a focus on simplicity, zero configuration, and snapshot testing."
    },
    {
        "name": "Cypress",
        "category": "Testing & QA",
        "aliases": ["cypress e2e", "cypress.io"],
        "related": ["JavaScript", "End-to-End Testing", "Web Development"],
        "prerequisites": ["JavaScript"],
        "description": "Next-generation front-end testing tool built for the modern web, running directly inside browser sessions."
    },
    {
        "name": "Agile/Scrum",
        "category": "Professional & Methodology",
        "aliases": ["agile methodology", "scrum", "sprint planning", "kanban"],
        "related": ["Jira", "Collaboration", "Product Management"],
        "prerequisites": [],
        "description": "Iterative project management and software development approach that helps teams deliver value to their customers faster."
    }
]

# Additional skills to cross the 200 threshold with comprehensive real-world tech stack coverage:
MORE_SKILLS = [
    # Languages
    ("Ruby on Rails", "Backend Development", ["rails", "ror"], ["Ruby", "PostgreSQL", "MVC"], "Full-stack web application framework written in Ruby following convention over configuration."),
    ("Elixir", "Programming Languages", ["elixirlang"], ["Erlang", "Phoenix Framework", "Concurrency"], "Dynamic, functional language designed for building scalable and maintainable applications on the Erlang VM."),
    ("Haskell", "Programming Languages", ["haskell-lang"], ["Functional Programming", "Type Theory"], "Purely functional programming language with strong static typing, type inference, and lazy evaluation."),
    ("Lua", "Programming Languages", ["lua-lang"], ["Embedded Scripting", "Game Development", "Redis"], "Lightweight, high-level, multi-paradigm programming language designed primarily for embedded use in applications."),
    ("Julia", "Programming Languages", ["julialang"], ["Scientific Computing", "Data Science", "Python"], "High-level, high-performance programming language designed specifically for technical and scientific computing."),
    ("Solidity", "Programming Languages", ["solidity smart contracts"], ["Ethereum", "Blockchain", "Smart Contracts"], "Object-oriented, high-level language for implementing smart contracts on blockchain platforms like Ethereum."),
    ("PowerShell", "Programming Languages", ["powershell scripting", "posh"], ["Windows", "Automation", "DevOps"], "Task automation and configuration management framework consisting of a command-line shell and scripting language."),
    ("Bash", "Programming Languages", ["bash shell", "gnu bash"], ["Linux", "Shell Scripting", "DevOps"], "Unix shell and command language written as a free software replacement for the Bourne shell."),
    
    # Frontend
    ("Pinia", "Frontend Development", ["pinia state management"], ["Vue.js", "State Management", "TypeScript"], "Intuitive, type-safe, lightweight state management store for Vue 3 applications."),
    ("Nuxt.js", "Frontend Development", ["nuxtjs", "nuxt"], ["Vue.js", "Server-Side Rendering", "TypeScript"], "Intuitive framework built on Vue providing server-side rendering, routing, and developer experience."),
    ("RxJS", "Frontend Development", ["reactive extensions"], ["Angular", "TypeScript", "Observables"], "Library for reactive programming using Observables, making it easier to compose asynchronous or callback-based code."),
    ("Three.js", "Frontend Development", ["threejs", "webgl 3d"], ["WebGL", "JavaScript", "3D Graphics"], "Cross-browser JavaScript library and API used to create and display animated 3D computer graphics in a web browser."),
    ("WebGL", "Frontend Development", ["web graphics library"], ["Three.js", "JavaScript", "Computer Graphics"], "JavaScript API for rendering high-performance interactive 3D and 2D graphics within any compatible web browser."),
    ("Storybook", "Frontend Development", ["storybookjs"], ["React", "Component Driven Development", "Design Systems"], "Open source tool for building UI components and pages in isolation, streamlining UI testing and documentation."),
    ("Figma", "Design & Prototyping", ["figma design", "ui/ux design"], ["UI/UX", "Design Systems", "Prototyping"], "Web-based collaborative interface design tool used for vector graphics, UI/UX design, and wireframing."),
    ("Web Accessibility", "Frontend Development", ["a11y", "wcag", "aria"], ["HTML5", "CSS3", "Frontend Development"], "Inclusive practice of ensuring web applications are usable by people of all abilities and disabilities."),
    ("Playwright", "Testing & QA", ["playwright testing"], ["End-to-End Testing", "TypeScript", "Test Automation"], "Modern end-to-end testing library for web apps, supporting chromium, firefox, and webkit with a single API."),
    ("PWA", "Frontend Development", ["progressive web apps", "service workers"], ["Web Development", "Offline Support", "Mobile"], "Web apps built using web platform technologies providing native app-like user experiences and offline capabilities."),
    ("CSS Grid", "Frontend Development", ["css grid layout"], ["CSS3", "Responsive Design", "Flexbox"], "Two-dimensional layout system for the web designed to handle both columns and rows."),
    ("Flexbox", "Frontend Development", ["css flexbox", "flexible box layout"], ["CSS3", "Responsive Design"], "One-dimensional CSS layout model offering space distribution between items in an interface."),
    ("Turborepo", "Frontend Development", ["turbo repo", "monorepo"], ["Monorepo", "Next.js", "Build Tools"], "High-performance build system for JavaScript and TypeScript codebases designed for monorepos."),

    # Backend
    ("Django REST Framework", "Backend Development", ["drf"], ["Django", "Python", "REST API"], "Powerful and flexible toolkit for building Web APIs on top of Django."),
    ("TypeORM", "Backend Development", ["type orm"], ["TypeScript", "Node.js", "PostgreSQL", "ORM"], "ORM that can run in NodeJS and can be used with TypeScript and JavaScript (ES5, ES6, ES7, ES8)."),
    ("Mongoose", "Backend Development", ["mongoose odm"], ["MongoDB", "Node.js", "Express.js"], "Elegant MongoDB object modeling for Node.js, providing schema-based validation and business logic hooks."),
    ("Starlette", "Backend Development", ["starlette framework"], ["FastAPI", "ASGI", "Python"], "Lightweight ASGI framework/toolkit ideal for building async web services in Python."),
    ("Uvicorn", "Backend Development", ["uvicorn server"], ["ASGI", "FastAPI", "Python"], "Lightning-fast ASGI web server implementation for Python, utilizing uvloop and httptools."),
    ("Gunicorn", "Backend Development", ["green unicorn"], ["WSGI", "Django", "Flask", "Python"], "Python WSGI HTTP Server for UNIX designed as a pre-fork worker model port from Ruby's Unicorn project."),
    ("Swagger / OpenAPI", "Backend Development", ["openapi", "swagger ui", "api documentation"], ["REST API", "API Design", "FastAPI"], "Standard specification format for defining, documenting, and consuming RESTful web services."),
    ("Socket.io", "Backend Development", ["socketio"], ["WebSockets", "Node.js", "Real-Time Systems"], "Event-driven library for real-time web applications, enabling bi-directional communication between client and server."),
    ("GraphQL Apollo", "Backend Development", ["apollo server", "apollo client"], ["GraphQL", "Node.js", "React"], "Comprehensive state management and API delivery platform that enables you to build GraphQL services quickly."),
    ("Fastify", "Backend Development", ["fastify framework"], ["Node.js", "REST API", "Express.js"], "Extremely fast and low overhead web framework for Node.js focused on providing the best developer experience."),
    ("Gin", "Backend Development", ["gin-gonic", "gin web framework"], ["Go", "REST API", "Microservices"], "High-performance HTTP web framework written in Go featuring a martini-like API with much better performance."),

    # Databases
    ("ClickHouse", "Databases", ["clickhouse db"], ["OLAP", "SQL", "Columnar Database"], "Open-source column-oriented DBMS for real-time analytical reporting using SQL queries."),
    ("MariaDB", "Databases", ["mariadb database"], ["MySQL", "SQL", "Relational Databases"], "Commercially supported fork of the MySQL relational database management system."),
    ("Neo4j", "Databases", ["neo4j graph db", "cypher query language"], ["Graph Databases", "NoSQL", "Data Modeling"], "Graph database management system developed by Neo4j, Inc., designed for connected data representation."),
    ("Firestore", "Databases", ["cloud firestore", "google firestore"], ["Firebase", "NoSQL", "Document Databases"], "Flexible, scalable database for mobile, web, and server development from Firebase and Google Cloud."),
    ("Couchbase", "Databases", ["couchbase server"], ["NoSQL", "Document Databases", "Distributed Cache"], "Distributed NoSQL cloud database that delivers unmatched versatility, performance, and financial value."),
    ("DuckDB", "Databases", ["duckdb in-process"], ["SQL", "Analytics", "Python", "Data Science"], "In-process SQL OLAP database management system designed for fast analytical queries on local datasets."),
    ("ChromaDB", "Databases", ["chroma vector database", "chromadb"], ["Vector Databases", "Embeddings", "RAG"], "Open-source AI-native embedding database designed for developer productivity and local experimentation."),
    ("Pinecone", "Databases", ["pinecone vector db"], ["Vector Databases", "Embeddings", "RAG"], "Managed, cloud-native vector database designed for high-scale, ultra-fast similarity search applications."),
    ("Weaviate", "Databases", ["weaviate vector search"], ["Vector Databases", "Embeddings", "RAG"], "Open-source vector database that allows you to store data objects and vector embeddings from your favorite ML models."),
    ("Qdrant", "Databases", ["qdrant vector engine"], ["Vector Databases", "Embeddings", "RAG", "Rust"], "Vector similarity search engine and vector database with extended filtering support written in Rust."),
    ("pgvector", "Databases", ["postgres pgvector"], ["PostgreSQL", "Vector Embeddings", "RAG"], "Open-source vector similarity search extension for PostgreSQL supporting exact and approximate nearest neighbor."),

    # Cloud & DevOps
    ("Terraform Modules", "DevOps & Cloud", ["terraform reusable modules"], ["Terraform", "Infrastructure as Code"], "Packaged, reusable Terraform configurations that can be shared across teams and projects."),
    ("ArgoCD", "DevOps & Cloud", ["argo cd", "gitops"], ["Kubernetes", "GitOps", "CI/CD"], "Declarative, GitOps continuous delivery tool for Kubernetes, managing cluster state from Git repositories."),
    ("Istio", "DevOps & Cloud", ["service mesh", "istio mesh"], ["Kubernetes", "Microservices", "Networking"], "Open-source service mesh providing uniform ways to secure, connect, and monitor microservices."),
    ("Linux Bash", "DevOps & Cloud", ["bash terminal", "linux cli"], ["Linux", "Shell Scripting"], "Standard shell command-line interpreter used for system administration and tool chaining."),
    ("AWS SQS", "DevOps & Cloud", ["amazon sqs", "simple queue service"], ["AWS", "Message Queues", "Microservices"], "Fully managed message queuing service from AWS that enables you to decouple and scale microservices."),
    ("AWS SNS", "DevOps & Cloud", ["amazon sns", "simple notification service"], ["AWS", "Pub/Sub", "Event-Driven Architecture"], "Fully managed pub/sub messaging service for both application-to-application (A2A) and application-to-person (A2P) communication."),
    ("AWS IAM", "DevOps & Cloud", ["identity and access management", "aws permissions"], ["AWS", "Cloud Security", "RBAC"], "Web service that helps you securely control access to AWS resources via users, groups, and roles."),
    ("AWS CloudWatch", "DevOps & Cloud", ["cloudwatch logs", "cloudwatch metrics"], ["AWS", "Monitoring", "Logging"], "Monitoring and observability service built for DevOps engineers, developers, and IT managers on AWS."),
    ("Google Cloud Run", "DevOps & Cloud", ["cloud run", "gcp cloud run"], ["Google Cloud Platform", "Serverless", "Docker"], "Fully managed compute platform that automatically scales your stateless containers up and down."),
    ("Azure DevOps", "DevOps & Cloud", ["azure pipelines", "vsts"], ["CI/CD", "Microsoft Azure", "DevOps"], "Suite of collaborative software development tools including Git repos, agile boards, and CI/CD pipelines."),
    ("OpenTelemetry", "DevOps & Cloud", ["otel", "telemetry"], ["Prometheus", "Distributed Tracing", "Observability"], "Collection of tools, APIs, and SDKs used to instrument, generate, collect, and export telemetry data."),

    # AI & ML
    ("Keras", "AI & Data Science", ["keras deep learning"], ["TensorFlow", "Deep Learning", "Python"], "High-level neural networks API, written in Python and capable of running on top of TensorFlow."),
    ("SciPy", "AI & Data Science", ["python scipy"], ["Python", "NumPy", "Scientific Computing"], "Open-source Python library used for scientific computing and technical computing algorithms."),
    ("Matplotlib", "AI & Data Science", ["python matplotlib", "data visualization"], ["Python", "Data Science", "Seaborn"], "Comprehensive library for creating static, animated, and interactive visualizations in Python."),
    ("Seaborn", "AI & Data Science", ["python seaborn"], ["Python", "Matplotlib", "Data Visualization"], "Python data visualization library based on matplotlib providing high-level interface for statistical graphics."),
    ("spaCy", "AI & Data Science", ["spacy nlp"], ["Natural Language Processing", "Python"], "Free, open-source library for advanced Natural Language Processing in Python, designed for production usage."),
    ("NLTK", "AI & Data Science", ["natural language toolkit"], ["Natural Language Processing", "Python"], "Leading platform for building Python programs to work with human language data."),
    ("XGBoost", "AI & Data Science", ["xgboost algorithm", "gradient boosting"], ["Machine Learning", "Scikit-Learn", "Ensemble Learning"], "Optimized distributed gradient boosting library designed to be highly efficient, flexible, and portable."),
    ("LightGBM", "AI & Data Science", ["light gradient boosting"], ["Machine Learning", "Gradient Boosting"], "Fast, distributed, high-performance gradient boosting framework based on decision tree algorithms."),
    ("CUDA", "AI & Data Science", ["nvidia cuda", "gpu programming"], ["C++", "PyTorch", "High-Performance Computing"], "Parallel computing platform and programming model developed by Nvidia for general computing on GPUs."),
    ("TensorRT", "AI & Data Science", ["nvidia tensorrt"], ["CUDA", "Deep Learning Inference", "Optimization"], "NVIDIA SDK for high-performance deep learning inference that optimizes neural network models."),
    ("ONNX", "AI & Data Science", ["open neural network exchange", "onnxruntime"], ["Machine Learning", "Deep Learning", "Model Deployment"], "Open format built to represent machine learning models, allowing model exchange across frameworks."),
    ("ONNX Runtime", "AI & Data Science", ["ort", "onnxruntime engine"], ["ONNX", "Inference Acceleration", "Machine Learning"], "Cross-platform, high-performance scoring engine for Open Neural Network Exchange (ONNX) models."),
    ("LoRA", "AI & Data Science", ["low-rank adaptation", "parameter efficient fine tuning"], ["Fine-Tuning", "Large Language Models", "PyTorch"], "Parameter-efficient fine-tuning technique that freezes pre-trained model weights and injects trainable rank decomposition matrices."),
    ("Quantization", "AI & Data Science", ["int8 quantization", "model quantization", "gguf"], ["Large Language Models", "Model Compression", "Inference Acceleration"], "Techniques that reduce precision of model parameters (e.g. from 16-bit to 4-bit) to drastically accelerate inference."),
    ("DSPy", "AI & Data Science", ["dspy framework"], ["Large Language Models", "Prompt Engineering", "Python"], "Framework for algorithmically optimizing LM prompts and weights, replacing fragile prompt heuristics."),
    ("Autonomous Agents", "AI & Data Science", ["ai agents", "multi-agent systems", "agentic workflows"], ["Large Language Models", "LangChain", "Tool Calling"], "Systems where foundation models plan, invoke external tools, reflect, and complete multi-step tasks autonomously."),
    ("Evaluation Metrics (LLM)", "AI & Data Science", ["ragas", "llm evals", "hallucination detection"], ["Large Language Models", "RAG", "Model Evaluation"], "Systematic benchmarking frameworks to evaluate faithfulness, relevancy, and accuracy of generative AI pipelines."),

    # Security
    ("Penetration Testing", "Cybersecurity", ["pen testing", "ethical hacking"], ["Cybersecurity", "Network Security", "Vulnerability Assessment"], "Simulated cyber attack against computer systems to check for exploitable vulnerabilities."),
    ("OWASP Top 10", "Cybersecurity", ["owasp vulnerabilities"], ["Web Security", "Cybersecurity", "Application Security"], "Standard awareness document for developers and web application security representing critical security risks."),
    ("Cryptography", "Cybersecurity", ["encryption", "aes", "rsa", "public key cryptography"], ["Cybersecurity", "SSL/TLS", "Information Security"], "Practice and study of techniques for secure communication in the presence of adversarial third parties."),
    ("Single Sign-On", "Cybersecurity", ["sso", "saml", "okta"], ["Identity and Access Management", "OAuth 2.0", "Security"], "Authentication scheme that allows a user to log in with a single ID to any of several related systems."),
    ("CORS", "Cybersecurity", ["cross-origin resource sharing"], ["HTTP", "Web Security", "REST API"], "Security mechanism that uses HTTP headers to tell browsers whether a web application can access cross-origin resources."),

    # Core Engineering & Collaboration
    ("Continuous Delivery", "DevOps & Cloud", ["continuous deployment"], ["CI/CD", "DevOps", "Automation"], "Software engineering approach in which teams produce software in short cycles, ensuring safe releases at any time."),
    ("Load Balancing", "Computer Science Core", ["load balancer", "reverse proxy load balancing"], ["System Design", "Nginx", "High Availability"], "Process of distributing network traffic across multiple servers to ensure reliability and optimal throughput."),
    ("Caching Strategies", "Computer Science Core", ["cache invalidation", "write-through cache", "lru cache"], ["Redis", "System Design", "Performance Optimization"], "Techniques to store copies of data in temporary storage locations for rapid subsequent retrieval."),
    ("Big-O Notation", "Computer Science Core", ["asymptotic analysis", "computational complexity"], ["Algorithms", "Data Structures"], "Mathematical notation that describes the limiting behavior of a function when the argument tends towards infinity."),
    ("Test-Driven Development", "Testing & QA", ["tdd"], ["Unit Testing", "Software Engineering"], "Software development process relying on software requirements being converted to test cases before software is fully developed."),
    ("End-to-End Testing", "Testing & QA", ["e2e testing"], ["Cypress", "Playwright", "Quality Assurance"], "Technique that tests the entire software product from beginning to end to ensure the application flow behaves as expected."),
    ("Code Review", "Developer Tools", ["pull request review", "peer review"], ["Git", "GitHub", "Software Quality"], "Systematic examination of computer source code intended to find bugs and improve code quality."),
    ("Monorepo Architecture", "Developer Tools", ["monorepos", "nx", "turborepo"], ["Turborepo", "Build Tools", "Git"], "Software development strategy where code for many projects is stored in a single unified repository.")
]

ROLES = [
    {
        "id": "role-software-engineer",
        "type": "role",
        "title": "Software Engineer",
        "aliases": ["software developer", "backend developer", "programmer", "swe"],
        "skills": ["Python", "Java", "C++", "Git", "SQL", "PostgreSQL", "Docker", "Linux", "REST API", "Data Structures", "Algorithms", "System Design", "Unit Testing"],
        "description": "Designs, builds, and maintains reliable software systems, enterprise backends, APIs, and scalable infrastructure using computer science fundamentals.",
        "learning_order": ["Data Structures", "Algorithms", "Git", "SQL", "REST API", "Docker", "System Design", "Unit Testing"]
    },
    {
        "id": "role-full-stack-developer",
        "type": "role",
        "title": "Full-Stack Developer",
        "aliases": ["fullstack developer", "web developer", "mern developer", "frontend backend developer"],
        "skills": ["JavaScript", "TypeScript", "HTML5", "CSS3", "React", "Next.js", "Node.js", "Express.js", "MongoDB", "PostgreSQL", "SQL", "Git", "Docker", "REST API", "Tailwind CSS"],
        "description": "Builds complete web applications end-to-end, from responsive UI interfaces to backend microservices, databases, authentication, and deployments.",
        "learning_order": ["HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Node.js", "Express.js", "REST API", "PostgreSQL", "Docker"]
    },
    {
        "id": "role-ai-engineer",
        "type": "role",
        "title": "AI/ML Engineer",
        "aliases": ["machine learning engineer", "ai developer", "ml engineer", "genai engineer"],
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "PyTorch", "TensorFlow", "Large Language Models", "RAG", "Vector Embeddings", "LangChain", "Groq", "Docker", "Model Evaluation", "Feature Engineering", "FastAPI"],
        "description": "Builds, evaluates, and deploys machine learning and generative AI systems using Python, deep learning, retrieval pipelines (RAG), and model serving.",
        "learning_order": ["Python", "NumPy", "Pandas", "Scikit-Learn", "Model Evaluation", "PyTorch", "Large Language Models", "RAG", "Vector Embeddings", "FastAPI", "Docker"]
    },
    {
        "id": "role-frontend-developer",
        "type": "role",
        "title": "Frontend Developer",
        "aliases": ["ui developer", "react developer", "frontend engineer", "client-side developer"],
        "skills": ["JavaScript", "TypeScript", "HTML5", "CSS3", "React", "Next.js", "Tailwind CSS", "Redux", "Vite", "Git", "Jest", "Web Accessibility", "Responsive Design"],
        "description": "Specializes in building modern, responsive, high-performance web user interfaces with state management, accessible markup, and smooth UX.",
        "learning_order": ["HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Tailwind CSS", "Next.js", "Redux", "Jest"]
    },
    {
        "id": "role-backend-developer",
        "type": "role",
        "title": "Backend Developer",
        "aliases": ["backend engineer", "server developer", "api engineer"],
        "skills": ["Python", "Java", "Go", "Node.js", "PostgreSQL", "Redis", "Docker", "REST API", "Microservices", "System Design", "SQL", "Linux", "CI/CD"],
        "description": "Architects server-side logic, high-throughput APIs, database schemas, asynchronous messaging, and scalable microservices.",
        "learning_order": ["Python", "SQL", "PostgreSQL", "REST API", "Docker", "Redis", "Microservices", "System Design"]
    },
    {
        "id": "role-devops-engineer",
        "type": "role",
        "title": "DevOps / Cloud Engineer",
        "aliases": ["site reliability engineer", "sre", "cloud engineer", "infrastructure engineer"],
        "skills": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "GitHub Actions", "Terraform", "Prometheus", "Grafana", "Nginx", "Shell Scripting", "Python", "Git"],
        "description": "Automates deployment pipelines, provisions infrastructure as code, monitors system health, and maintains high reliability across cloud platforms.",
        "learning_order": ["Linux", "Shell Scripting", "Git", "Docker", "CI/CD", "AWS", "Terraform", "Kubernetes", "Prometheus", "Grafana"]
    },
    {
        "id": "role-data-engineer",
        "type": "role",
        "title": "Data Engineer",
        "aliases": ["big data engineer", "data platform engineer", "etl developer"],
        "skills": ["Python", "SQL", "PostgreSQL", "Apache Spark", "Apache Kafka", "Apache Airflow", "Data Pipelines", "ETL", "Snowflake", "Docker", "BigQuery"],
        "description": "Constructs robust distributed data pipelines, manages event streaming, implements ETL jobs, and structures analytical data warehouses.",
        "learning_order": ["Python", "SQL", "PostgreSQL", "Data Pipelines", "ETL", "Apache Spark", "Apache Airflow", "Apache Kafka", "Snowflake"]
    },
    {
        "id": "role-mobile-developer",
        "type": "role",
        "title": "Mobile App Developer",
        "aliases": ["android developer", "ios developer", "react native developer", "flutter developer"],
        "skills": ["Kotlin", "Swift", "Flutter", "React Native", "Android Development", "iOS Development", "Git", "REST API", "Mobile UI Design"],
        "description": "Develops native and cross-platform mobile apps for iOS and Android devices, focusing on mobile performance, offline caching, and responsive UI.",
        "learning_order": ["Kotlin", "Android Development", "Swift", "iOS Development", "Flutter", "REST API", "Git"]
    }
]

def generate():
    all_items = []
    
    # 1. Add roles
    for role in ROLES:
        all_items.append(role)
        
    # 2. Add base skills
    for skill in SKILLS:
        skill_id = "skill-" + skill["name"].lower().replace(" ", "-").replace("/", "-").replace(".", "-").replace("#", "sharp").replace("+", "p")
        all_items.append({
            "id": skill_id,
            "type": "skill",
            "title": skill["name"],
            "name": skill["name"],
            "category": skill["category"],
            "aliases": skill.get("aliases", []),
            "skills": [skill["name"]],
            "related_skills": skill.get("related", []),
            "prerequisites": skill.get("prerequisites", []),
            "description": skill["description"]
        })

    # 3. Add more skills
    for name, cat, aliases, related, desc in MORE_SKILLS:
        skill_id = "skill-" + name.lower().replace(" ", "-").replace("/", "-").replace(".", "-").replace("#", "sharp").replace("+", "p")
        all_items.append({
            "id": skill_id,
            "type": "skill",
            "title": name,
            "name": name,
            "category": cat,
            "aliases": aliases,
            "skills": [name],
            "related_skills": related,
            "prerequisites": [],
            "description": desc
        })

    corpus = {
        "framework_version": "skillsetu-skill-framework-v2-comprehensive",
        "source": "SkillSetu curated industry role and skill taxonomy",
        "total_documents": len(all_items),
        "total_roles": len(ROLES),
        "total_skills": len(all_items) - len(ROLES),
        "documents": all_items
    }

    out_path = Path(__file__).resolve().parent / "skill_framework.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)

    print(f"Successfully generated {out_path} with {len(all_items)} total entries ({len(ROLES)} roles, {len(all_items) - len(ROLES)} skills).")

if __name__ == "__main__":
    generate()
