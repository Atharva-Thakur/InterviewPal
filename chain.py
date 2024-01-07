import chainlit as cl
import google.generativeai as palm
from dotenv import load_dotenv
import os
import random
import pandas as pd


#---Chainlit imports---
from chainlit.input_widget import Select


load_dotenv()

API_KEY=os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# def main():
#     eval ="0"
    #!Code below works fine
    # n=0
    # convo=""
    # for i in range(5):
    #     job_title='data scientist'
    #     que,ans = generate_ques(job_title)
    #     print(que)
    #     candidate_ans = input("Enter answer ->")
    #     eval = get_and_eval_response(que,ans,candidate_ans,job_title)
    #     print(eval)
    #     n=n+1
    #     convo = convo + "Question " + str(n+1) + ".: " + que + "\nCorrect Answer: " + ans + "\nCandidate Answer: " + candidate_ans + "\nEvaluation: " + eval + "\n\n"
    # decision = get_Decision(job_title, convo)
    # reason = get_Reason(job_title, convo, decision)
    # print(reason)


@cl.on_chat_start
async def main():

    job_title_select = await cl.ChatSettings(
        [
            Select(
                id="job_title",
                label="Job Title",
                values=['data scientist', 'cyber security engineer','devops engineer'],
                initial_index=0,
            )
        ]
    ).send()
    job_title = job_title_select["job_title"]

    que,ans = generate_ques(job_title)

    res = await cl.AskUserMessage(content=que, timeout=10).send()
    if res:
        eval = get_and_eval_response(que,ans,candidate_ans,job_title)
        await cl.Message(
            content=eval,
        ).send()

def generate_ques(job_title):
    if job_title == "data scientist":
        df = pd.read_csv("MLDL-train.csv", encoding='utf-8')
    elif job_title == "cyber security engineer":
        df = pd.read_csv("Cyber-Data.csv", encoding='utf-8')
    elif job_title == "devops engineer":
        df = pd.read_csv("DevOps-Data.csv", encoding='utf-8')
    i = random.randint(0,len(df)-1)
    que = df.iloc[i,0]
    ans = df.iloc[i,1]
    return que,ans

def get_and_eval_response(que,ans,candidate_ans,job_title):
    
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
    return eval


def get_Decision(job_title, convo):
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

def get_Reason(job_title, convo, decision):
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

if __name__ == "__main__":
    main()