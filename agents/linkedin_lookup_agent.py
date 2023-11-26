from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url, get_company_profile_url


def lookup(name: str, company: str) -> str:
    llm = ChatOpenAI(temperature=0, tiktoken_model_name="gpt-3.5-turbo")
    template = """"given the full name {name_of_person} and company name {company_name} I want you to get me a link to their Linkedin profile page and the company's Linkedin profile page.
    Your answer be an object with linkedin_url and company_linkedin_url
    """

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            description="useful for when you need to get the Linkedin Page URL",
            func=get_profile_url,
        ), 
        Tool(
            name="Crawl Google for company's linkedin profile page",
            description="useful for when you need to get a company's Linkedin Page URL",
            func=get_company_profile_url,
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        llm=llm,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person", "company_name"]
    )

    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name, company_name=company))

    return linkedin_profile_url
