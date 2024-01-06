import google.generativeai as palm

palm.configure(api_key='AIzaSyAmqklOAqWd6N0OzZ2-CqC1e35LB3vV5XI')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

def getDecision(job_title, convo):
    prompt = f"""
    You are an interviewer at a big company. 
    A candidate applying for the position of {job_title} has given an interview.
    Analyze the following converstuion of their interview and decide whether the candidate deserves the position or not.
    conversation : {convo}
    Answer in one word only - Approved or Rejected.
    """

    dec = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_output_tokens=100)

    return dec.result