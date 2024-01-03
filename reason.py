import google.generativeai as palm

palm.configure(api_key='AIzaSyAmqklOAqWd6N0OzZ2-CqC1e35LB3vV5XI')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

def getReason(job_title, convo, decision):
    prompt = f"""
    You are in the role of a senior interviewer representing a prominent company. 
    A candidate has recently undergone an interview for the position of {job_title}
    The interview conversation is provided in the form of {convo}. 
    Subsequently, the candidate's performance is evaluated and the candidate is labelled as {decision}. 
    Substantiate the decision with a brief explanation, taking into account the candidate's performance in the interview.
    """

    res = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_output_tokens=200)
    
    return res.result