import google.generativeai as palm
import pandas as pd
from text import getText
import random

palm.configure(api_key='API')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

convo = ""
columns = ["Question", "Correct Answer", "Candidate Answer", "Evaluation"]
report = pd.DataFrame(columns=columns)
n = 0

def questions(job_title):
    if job_title == "data scientist":
        df = pd.read_csv("MLDL-train.csv", encoding='utf-8')
    elif job_title == "cyber security engineer":
        df = pd.read_csv("cyber-data.csv", encoding='utf-8')
    elif job_title == "devops engineer":
        df = pd.read_csv("devops.csv", encoding='utf-8')
    
    
    i = random.randint(0,len(df)-1)
    que = df.iloc[i,0]
    ans = df.iloc[i,1]
    print("Question",n+1,".",que)
    candidate_ans = getText()
    prompt = f"""
            You are an interviewer at a big company. 
            A candidate applying for the position of {job_title} has been asked the question {que}.
            The correct answer to the question is {ans}.
            The candidate has answered to the given question with {candidate_ans}.
            Rate the answer out of 100 on the basis of how correct and detailed the answer is.
            An ideal answer should be about 30 words and similar to {ans}.
            Return only a number between 0 and 100 inclusive.
            """

    evaluation = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0.5,
                max_output_tokens=800)
    eval = evaluation.result

    new_row_df = pd.DataFrame([que,ans,candidate_ans,eval], columns=report.columns)
    report = pd.concat([report, new_row_df], ignore_index=True)
            
    n += 1
    convo = convo + "Question " + str(n+1) + ".: " + que + "\nCorrect Answer: " + ans + "\nCandidate Answer: " + candidate_ans + "\nEvaluation: " + eval + "\n\n"

    return convo, report