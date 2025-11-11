# Reflection Log - Assignment 2

## What I Learned from Multi-Agent Workflow
Building this travel planner taught me how agents can complement each other's strengths. The Planner works from general knowledge to create a draft quickly, while the Reviewer uses internet search to verify details. This division of labor matches real world workflows where initial brainstorming is separate from fact checking. 
The most interesting insight was seeing how tool access fundamentally changes an agent's behavior. The Reviewer with internet_search produces much more accurate, current information compared to the Planner working from memory alone. This shows that multi-agent systems can systematically address reliability issues that single-agent systems struggle with.

## Challenges and Solutions
The main challenge was writing prompts that were clear enough to produce consistent outputs but flexible enough to handle varied user requests. Initially, I worried about the Planner making up information, but I realized that's actually acceptable because the Reviewer's job is to catch and fix those issues. 
Another challenge was balancing prompt length. I settled on a conversational tone with specific requirements organized clearly. Using phrases like "Don't skip searches" instead of formal instructions made the prompts feel more natural while still being directive.

## Design Choices
I keep the Planner offline to let it work fast without extra research with the internet to save the processing time, then having the Reviewer do targeted searches. This is more efficient than having both agents search everything. The Delta List format was designed to show the review process transparently, helping users understand what changed and why.

## Tools and Assistance Used
I used GPT to give me some initial prompt structure hints and ensure it can have a better effect on the both models.

