import os
import json

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile, scrape_linkedin_company_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

if __name__ == "__main__":
    print("hello LangChain!")

    linkedin_urls= json.loads(linkedin_lookup_agent(name="Oliver Kicks", company="Concept Ventures"))
    linkedin_profile_url = linkedin_urls["linkedin_url"]
    company_linkedin_profile_url = linkedin_urls["company_linkedin_url"]

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. a short summary
    2. a company description
    3. two interesting facts about them
    4. the last 2 company updates on linkedin (don't mention how many likes or comments it got)
    5. their company website url (just respond with the URL)

    Respond with an object with the following keys: summary, company_description, profile_facts, company_updates, website_url 
    """

    sumary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

    chain = LLMChain(llm=llm, prompt=sumary_prompt_template)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    company_linkedin_data = scrape_linkedin_company_profile(company_linkedin_profile_url=company_linkedin_profile_url)

    print(chain.run(information=f"{linkedin_data}, {company_linkedin_data}"))
