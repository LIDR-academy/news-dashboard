Please analyze and fix the Jira ticket: $ARGUMENTS.

Follow these steps:

1. Use Jira MCP to get the ticket details, whether it is the ticket id/number, keywords referring to the ticket or indicating status, like "the one in progress"
2. Understand the problem described in the ticket
3. Search the codebase for relevant files
4. Start a new branch using the ID of the ticket (for example NEWS-1)
5. Implement the necessary changes to solve the ticket 
6. Write and run tests to verify the solution
7. Ensure code passes linting and type checking
8. Create a descriptive commit message that includes the Jira ticket ID (e.g., "NEWS-1") in both the commit title and description for proper linking
9. Push and create a PR, including the Jira ticket ID (e.g., "NEWS-1") in the PR title and description so it gets linked in the Jira ticket

Remember to use the GitHub CLI (`gh`) for all GitHub-related tasks.