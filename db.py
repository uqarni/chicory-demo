from supabase import create_client, Client
import os

def initialize_prompt(session_state):
    #connect to supabase database
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)
    data, count = supabase.table("bots_dev").select("*").eq("id", "cole").execute()
    bot_info = data[1][0]

    to_format = {
        'lead_first_name': session_state.lead_first_name,
        'lead_last_name': session_state.lead_last_name,
        'lead_email': session_state.lead_email,
        'agent_name': 'Cole',
        'company_name': session_state.company_name,
        'company_description': session_state.company_description,
        'booking_link': session_state.booking_link
    }
    
    system_prompt = bot_info['system_prompt']
    system_prompt = system_prompt.format(**to_format)
    session_state.system_prompt = system_prompt


def get_initial_message(key = None):
    initial_messages = {
        "hiring_engineer": "{lead_first_name},\n\nI saw that you are hiring data engineers. Typically this means that there is a backlog of tickets that need attention. Have you considered any generative AI automations to replace some of the data engineering tasks?\n\nLet me know if I can share a brief video we put together for {company_name}.\n\nCole \n\nCole Thomas \nGrowth @ Chicory \n1 206-330-7817 \nUnsubscribe | Book a time",
    
        "on_call_engineer": "{lead_first_name},\n\nNoticed that you are part of the data team at {company_name}. I'm curious, have you considered any generative AI automations to replace some of your on-call engineering tasks? We can help you add hours back to your day.\n\nLet me know if I can share a brief video my CEO put together for {company_name}.\n\nCole \n\nCole Thomas \nGrowth @ Chicory \n1 206-330-7817 \nUnsubscribe | Book a time",
    
        "missed_timeline": "{lead_first_name},\n\nDo you have any ongoing data migrations at the moment? Our team spent years at Apple and Amazon running similar projects and are now building generative AI automations to help folks like {company_name}. \n\nLet me know if I can share a brief video my CEO put together for you.\n\nCole \n\nCole Thomas\nGrowth @ Chicory\n1 206-330-7817 \nUnsubscribe | Book a time",
    
        "repetitive_schema": "{lead_first_name},\n\nAre you frustrated to create the same db schema over and over again? \n\nI ask because I'm looking for feedback. We build generative AI automations to replace repetitive data engineering tasks. We have built similar in the past for companies like Apple and Amazon. \n\nAre you open to sharing how we could build it to help {company_name}?\n \nCole \n\nCole Thomas\nGrowth @ Chicory \n1 206-330-7817\nUnsubscribe | Book a time"
    }

    if key:
        return initial_messages[key]
    else:
        return initial_messages.keys()

def format_initial_message(im, session_state):
    to_format = {
        'lead_first_name': session_state.lead_first_name,
        'lead_last_name': session_state.lead_last_name,
        'lead_email': session_state.lead_email,
        'agent_name': 'Cole',
        'company_name': session_state.company_name,
        'company_description': session_state.company_description,
        'booking_link': session_state.booking_link
    }
    initial_text = im.format(**to_format)



    session_state.initial_text = initial_text
    session_state.messages.insert(0, {'role': 'assistant', 'content': initial_text})
