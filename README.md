# Clarity Care was created on 8/23/2025 at CrewAI's 1st Hackathon

Clarity Care is a software for simplifying medical documentation. Using crewAI, groq, browserbase, and serper, Clarity Care is agentic and the UI was built using Windsurf. 

You can find the CrewAI Enterprise version here: https://claritycare-86512f9b-a9d7-4aae-ab94-d6beb90-d41e1995.crewai.com 

What Clarity Care can currently do: It can parse through a pdf converted to an image and extract numbers along with information about the health care provider as found on the web and the medical document. 

# Problems and Next Steps 

Problems:
- Scanned pdf wasn’t able to be used and needed to convert into a png so that it could be read

Next steps: 

- Integrate a voice agent so that people can talk to a customer service provider

- Figure out best ways to parse over a scanned pdf using OCR 


# Clarity Care Crew AI Implementation 

Welcome to the Claritycare Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/claritycare/config/agents.yaml` to define your agents
- Modify `src/claritycare/config/tasks.yaml` to define your tasks
- Modify `src/claritycare/crew.py` to add your own logic, tools and specific args
- Modify `src/claritycare/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the claritycare Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The claritycare Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Claritycare Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
