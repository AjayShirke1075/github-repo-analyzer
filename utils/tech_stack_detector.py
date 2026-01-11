def detect_tech_stack(file_list):
    """
    Detects technologies, frameworks, and tools used in a repository.
    
    Args:
        file_list: List of file paths in the repository
        
    Returns:
        list: Sorted list of detected technologies
    """
    tech = set()

    for file in file_list:
        file_lower = file.lower()
        
        # Programming Languages
        if file.endswith(".py"):
            tech.add("Python")
        if file.endswith(".js"):
            tech.add("JavaScript")
        if file.endswith(".ts"):
            tech.add("TypeScript")
        if file.endswith(".jsx"):
            tech.add("React (JSX)")
        if file.endswith(".tsx"):
            tech.add("React (TypeScript)")
        if file.endswith(".vue"):
            tech.add("Vue.js")
        if file.endswith(".java"):
            tech.add("Java")
        if file.endswith(".cpp") or file.endswith(".cc") or file.endswith(".cxx"):
            tech.add("C++")
        if file.endswith(".c"):
            tech.add("C")
        if file.endswith(".cs"):
            tech.add("C#")
        if file.endswith(".go"):
            tech.add("Go")
        if file.endswith(".rs"):
            tech.add("Rust")
        if file.endswith(".rb"):
            tech.add("Ruby")
        if file.endswith(".php"):
            tech.add("PHP")
        if file.endswith(".swift"):
            tech.add("Swift")
        if file.endswith(".kt"):
            tech.add("Kotlin")
        if file.endswith(".scala"):
            tech.add("Scala")
        if file.endswith(".r"):
            tech.add("R")
        
        # Web Technologies
        if file.endswith(".html") or file.endswith(".htm"):
            tech.add("HTML")
        if file.endswith(".css"):
            tech.add("CSS")
        if file.endswith(".scss") or file.endswith(".sass"):
            tech.add("Sass/SCSS")
        if file.endswith(".less"):
            tech.add("Less")
        
        # Configuration & Package Managers
        if "requirements.txt" in file:
            tech.add("Python (pip)")
        if "pyproject.toml" in file:
            tech.add("Python (Poetry/PDM)")
        if "pipfile" in file_lower:
            tech.add("Python (Pipenv)")
        if "package.json" in file:
            tech.add("Node.js")
        if "yarn.lock" in file:
            tech.add("Yarn")
        if "pnpm-lock.yaml" in file:
            tech.add("pnpm")
        if "composer.json" in file:
            tech.add("PHP (Composer)")
        if "gemfile" in file_lower:
            tech.add("Ruby (Bundler)")
        if "cargo.toml" in file:
            tech.add("Rust (Cargo)")
        if "go.mod" in file:
            tech.add("Go Modules")
        if "pom.xml" in file:
            tech.add("Maven")
        if "build.gradle" in file:
            tech.add("Gradle")
        
        # Frameworks & Libraries
        if "django" in file_lower:
            tech.add("Django")
        if "flask" in file_lower:
            tech.add("Flask")
        if "fastapi" in file_lower:
            tech.add("FastAPI")
        if "next.config" in file_lower:
            tech.add("Next.js")
        if "nuxt.config" in file_lower:
            tech.add("Nuxt.js")
        if "angular.json" in file:
            tech.add("Angular")
        if "svelte.config" in file_lower:
            tech.add("Svelte")
        
        # DevOps & Infrastructure
        if "dockerfile" in file_lower:
            tech.add("Docker")
        if "docker-compose" in file_lower:
            tech.add("Docker Compose")
        if ".github/workflows" in file:
            tech.add("GitHub Actions")
        if ".gitlab-ci" in file:
            tech.add("GitLab CI")
        if "jenkinsfile" in file_lower:
            tech.add("Jenkins")
        if "terraform" in file_lower and file.endswith(".tf"):
            tech.add("Terraform")
        if "kubernetes" in file_lower or file.endswith(".yaml") and "k8s" in file_lower:
            tech.add("Kubernetes")
        if ".circleci" in file:
            tech.add("CircleCI")
        
        # Testing
        if "pytest" in file_lower or "test_" in file_lower and file.endswith(".py"):
            tech.add("Pytest")
        if "jest.config" in file_lower or file.endswith(".test.js") or file.endswith(".spec.js"):
            tech.add("Jest")
        if "cypress" in file_lower:
            tech.add("Cypress")
        if "selenium" in file_lower:
            tech.add("Selenium")
        
        # Databases
        if "mongodb" in file_lower or "mongo" in file_lower:
            tech.add("MongoDB")
        if "postgres" in file_lower or "postgresql" in file_lower:
            tech.add("PostgreSQL")
        if "mysql" in file_lower:
            tech.add("MySQL")
        if "redis" in file_lower:
            tech.add("Redis")
        if "sqlite" in file_lower or file.endswith(".db") or file.endswith(".sqlite"):
            tech.add("SQLite")
        
        # Build Tools
        if "webpack.config" in file_lower:
            tech.add("Webpack")
        if "vite.config" in file_lower:
            tech.add("Vite")
        if "rollup.config" in file_lower:
            tech.add("Rollup")
        if "gulpfile" in file_lower:
            tech.add("Gulp")
        if "gruntfile" in file_lower:
            tech.add("Grunt")
        
        # Code Quality
        if ".eslintrc" in file or "eslint.config" in file_lower:
            tech.add("ESLint")
        if ".prettierrc" in file or "prettier.config" in file_lower:
            tech.add("Prettier")
        if "pylint" in file_lower or ".pylintrc" in file:
            tech.add("Pylint")
        if ".flake8" in file:
            tech.add("Flake8")
        
        # Documentation
        if "readme.md" in file_lower:
            tech.add("Markdown Docs")
        if "mkdocs" in file_lower:
            tech.add("MkDocs")
        if "sphinx" in file_lower:
            tech.add("Sphinx")

    return sorted(list(tech))

