<jira_ticket>
#$ARGUMENTS
</jira_tickete>
1- git worktree add ./.trees/feature-issue-$ARGUMENTS -b feature-issue-$ARGUMENTS
2- cd .trees/feature-issue-$ARGUMENTS
3- activate plan mode on
4- determine the agents to be used and if they can be paralelized
5- analyze the Jira ticket #$ARGUMENTS using MCP
6- at the end after the confirmation of the user, commit the changes and push them to the branch