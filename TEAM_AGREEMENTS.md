# Engineering Team Development Rules

## Project Context
This project follows hexagonal architecture in backend and feature-based structure in frontend. These rules ensure consistency, maintainability, and high code quality across the team.

## Code Quality Standards

### Git Workflow Standards
- **Branch naming convention**: 
  - Features: `feature/TICKET-123-short-description`
  - Bug fixes: `fix/bug-description`
  - Hotfixes: `hotfix/critical-issue`
- **Commit messages**: Use English, be descriptive, prefer conventional commits format
- **Pull Requests**: Require minimum 2 reviewers, maximum 3 days for review cycle
- **Merge requirements**: All tests passing + minimum 2 approvals

### Code Review Guidelines
- **Focus on code quality**: Review logic, patterns, and architecture adherence
- **Be specific and constructive**: Provide actionable feedback with examples
- **Use prefixes**: "nit:" for minor issues, "blocking:" for critical problems
- **Response time**: Maximum 24 hours for initial review

### Testing Requirements
- **Unit tests**: Mandatory for all business logic and use cases
- **Integration tests**: Required for API endpoints and critical user flows
- **Test coverage**: Minimum 80% but focus on critical paths over percentage
- **No merge without**: All tests passing and no linter errors

### Architecture Compliance
- **Backend**: Strict hexagonal architecture - follow existing patterns in `src/application`, `src/domain`, `src/infrastructure`
- **Frontend**: Feature-based structure - organize by domain in `src/features/`
- **Shared code**: Common components in `src/core/`, utilities in `src/lib/`
- **Dependencies**: Discuss new dependencies with team before adding

## Development Environment Standards

### Environment Management
- **Development**: Open for experimentation and feature development
- **Staging**: Complete features only, production simulation environment
- **Production**: Requires tech lead approval and careful monitoring

### Deployment Guidelines
- **Staging deployments**: Anytime during development
- **Production deployments**: Scheduled windows (Tuesday/Thursday 10:00-12:00)
- **Hotfixes**: Emergency only with proper change management
- **Rollback policy**: Immediate rollback on production issues, debug afterward

## Code Implementation Standards

### Definition of Done
- [ ] Code implemented and peer reviewed
- [ ] All tests passing (unit + integration)
- [ ] Documentation updated (README, inline comments)
- [ ] Successfully deployed to staging environment
- [ ] Quality assurance approved (when applicable)
- [ ] Zero linter errors or warnings

### Naming Conventions
- **TypeScript/JavaScript**: camelCase for variables/functions, PascalCase for components/classes
- **Python**: snake_case for variables/functions, PascalCase for classes
- **Files**: kebab-case for component files, snake_case for Python modules
- **Constants**: UPPER_SNAKE_CASE in both languages

### Error Handling
- **Backend**: Use domain-specific exceptions, proper HTTP status codes
- **Frontend**: Implement error boundaries, user-friendly error messages
- **Logging**: Structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)

### Performance Guidelines
- **Frontend**: Lazy loading, code splitting, memoization for expensive computations
- **Backend**: Database query optimization, caching strategies, async operations
- **Both**: Minimize dependencies, profile critical paths

### Security Standards
- **Authentication**: JWT tokens with proper expiration
- **Authorization**: Role-based access control
- **Input validation**: Server-side validation for all inputs
- **Data sanitization**: Prevent XSS and injection attacks

## Development Workflow

### Feature Development Process
1. **Planning**: Break down features into small, testable units
2. **Implementation**: Follow TDD approach when possible
3. **Testing**: Write tests for critical business logic
4. **Documentation**: Update relevant docs and comments
5. **Review**: Submit PR with clear description and test plan

### Technical Debt Management
- **Refactoring**: Continuous improvement, Boy Scout Rule
- **Documentation**: Keep architecture decisions recorded
- **Monitoring**: Track technical debt in code reviews
- **Prioritization**: Balance feature work with maintenance

## Quality Assurance

### Code Quality Metrics
- **Complexity**: Keep cyclomatic complexity low
- **Duplication**: DRY principle, extract common patterns
- **Maintainability**: Self-documenting code, clear abstractions
- **Testability**: Dependency injection, pure functions when possible

### Continuous Integration
- **Automated testing**: All tests must pass before merge
- **Code formatting**: Automatic formatting with Prettier/Black
- **Linting**: ESLint for frontend, pylint/ruff for backend
- **Type checking**: TypeScript strict mode, Python type hints

---

**Last updated**: September 2025
**Review cycle**: Quarterly or as needed

*"Consistency in code leads to predictability in behavior"*
