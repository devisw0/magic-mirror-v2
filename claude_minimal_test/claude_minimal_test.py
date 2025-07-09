import os
import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate


def return_llm(type="claude"):
    profile = os.getenv("AWS_PROFILE", "iff_aws_crtveapps_aitools_user-889166750058")
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("CLAUDE_MODEL_ID", "us.anthropic.claude-3-7-sonnet-20250219-v1:0")

    session = boto3.Session(profile_name=profile)
    bedrock_client = session.client('bedrock-runtime', region_name=region)

    model_kwargs = {
        "max_tokens": 2048,
        "temperature": 0.0,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman"],
    }

    return ChatBedrock(
        client=bedrock_client,
        model_id=model_id,
        model_kwargs=model_kwargs
    )

model = return_llm("claude")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

llm_chain = prompt | model

results = llm_chain.invoke({"question": "What is the capital of Japan?"})
print(results.content) 