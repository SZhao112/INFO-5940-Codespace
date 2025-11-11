# Reflection Log - Assignment 2

## What I Learned from Multi-Agent Workflow
Building this travel planner showed me that a fast Planner and a careful Reviewer can cover each other’s gaps. The Planner uses general knowledge to draft quickly, while the Reviewer uses internet search to verify hours, prices, and logistics. This split mirrors real work where brainstorming and fact checking are separate. I also saw how tool access changes behavior: the Reviewer with search is more precise and current, and the offline Planner focuses on speed and coverage. A simple delta list made changes traceable; for example, the Reviewer corrected a drafted opening time after checking a current source and the plan was adjusted accordingly.

## Challenges and Solutions
My main challenge was writing prompts that stay consistent but still handle varied requests. Early on I worried about the Planner making up details, but that is acceptable here because the Reviewer’s role is to catch and fix those parts. I also had to balance length and tone. I settled on a conversational style with clear requirements and phrases like “Don’t skip searches,” which kept guidance firm without sounding rigid. Going forward I will tighten the language on which items the Reviewer must always check.

## Design Choices
I kept the Planner offline so it can work fast, then had the Reviewer do targeted searches. This is more efficient than making both agents search everything and keeps attention on facts that are likely to change. The delta list format makes updates transparent and helps users see what changed and why, which supports trust and quicker iteration.

## Tools and Assistance Used
I used GPT to get initial prompt structure hints and to improve how the two prompts fit together. Next step maybe I will add explicit triggers for review (dates, prices, schedules) and keep a small set of repeated issues as a quick test after edits.





