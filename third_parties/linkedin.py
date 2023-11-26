import os
import requests

# headers = {'Authorization': 'Bearer ' + api_key}
# api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/resolve'
# params = {
#     'company_domain': 'gatesfoundation.org',
#     'first_name': 'Bill',
#     'similarity_checks': 'include',
#     'enrich_profile': 'enrich',
#     'location': 'Seattle',
#     'title': 'Co-chair',
#     'last_name': 'Gates',
# }

# response = requests.get(api_endpoint,
#                         params=params,
#                         headers=headers)


def scrape_linkedin_profile(linkedin_profile_url: str):
    """ "scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXY_CURL_API")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def scrape_linkedin_company_profile(company_linkedin_profile_url: str):
    """ "scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/linkedin/company"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXY_CURL_API")}'}

    response = requests.get(
        api_endpoint, params={"url": company_linkedin_profile_url}, headers=header_dic
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
