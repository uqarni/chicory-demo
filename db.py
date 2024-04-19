from supabase import create_client, Client
import os

def initialize_prompt_and_text(session_state):
    #connect to supabase database
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)
    data, count = supabase.table("bots_dev").select("*").eq("id", "cole").execute()
    bot_info = data[1][0]

    system_prompt = bot_info['system_prompt']
    initial_text = bot_info['initial_text']
    to_format = {
        'lead_first_name': session_state.lead_first_name,
        'lead_last_name': session_state.lead_last_name,
        'lead_email': session_state.lead_email,
        'agent_name': 'Cole',
        'company_name': session_state.company_name,
        'company_description': session_state.company_description,
        'booking_link': session_state.booking_link
    }
    initial_text = initial_text.format(**to_format)
    system_prompt = system_prompt.format(**to_format)

    session_state.system_prompt = system_prompt
    session_state.initial_text = initial_text
    session_state.messages.insert(0, {'role': 'assistant', 'content': initial_text})

def get_initial_message(key):
    initial_messages = {
        "hiring_engineer": """{first_name},
    
    I saw that you are hiring data engineers. Typically this means that there is a backlog of tickets that need attention. Have you considered any generative AI automations to replace some of the data engineering tasks?
    
    Let me know if I can share a brief video we put together for {company_name}.
    
    Cole 
    
    Cole Thomas
    Growth @ Chicory
    + 1 206-330-7817
    Unsubscribe | Book a time""",
    
        "on_call_engineer": """{first_name},
    
    Noticed that you are part of the data team at {company_name}. I'm curious, have you considered any generative AI automations to replace some of your on-call engineering tasks? We can help you add hours back to your day.
    
    Let me know if I can share a brief video my CEO put together for {company_name}.
    
    Cole 
    
    Cole Thomas
    Growth @ Chicory
    + 1 206-330-7817
    Unsubscribe | Book a time""",
    
        "missed_timeline": """{first_name},
    
    Do you have any ongoing data migrations at the moment? Our team spent years at Apple and Amazon running similar projects and are now building generative AI automations to help folks like {company_name}. 
    
    Let me know if I can share a brief video my CEO put together for you.
    
    Cole 
    
    Cole Thomas
    Growth @ Chicory
    + 1 206-330-7817
    Unsubscribe | Book a time""",
    
        "repetitive_schema": """{first_name},
    
    Are you frustrated to create the same db schema over and over again? 
    
    I ask because I'm looking for feedback. We build generative AI automations to replace repetitive data engineering tasks. We have built similar in the past for companies like Apple and Amazon. 
    
    Are you open to sharing how we could build it to help {company_name}?
     
    Cole 
    
    Cole Thomas
    Growth @ Chicory
    + 1 206-330-7817
    Unsubscribe | Book a time"""
    }

    if key:
        return initial_messages[key]
    else:
        return initial_messages.keys()

    
