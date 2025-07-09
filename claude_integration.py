import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws.chat_models.bedrock import ChatBedrock

def return_llm(type="claude"):
    """Initialize Claude AI model"""
    try:
        # You'll need to configure your AWS credentials
        session = boto3.Session(profile_name='iff_aws_crtveapps_aitools_user-889166750058')   
        bedrock_client = session.client('bedrock-runtime', region_name='us-east-1')
        
        model_kwargs = {
            "max_tokens": 2048,
            "temperature": 0.7,  # Slightly more creative for conversation
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": ["\n\nHuman"],
        }
        
        return ChatBedrock(
            client=bedrock_client,
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            model_kwargs=model_kwargs
        )
    except Exception as e:
        print(f"❌ Claude initialization error: {e}")
        return None

def get_claude_response(user_input):
    """Get AI response from Claude"""
    try:
        model = return_llm("claude")
        if not model:
            return "I'm sorry, I'm having trouble connecting to my AI brain right now."
        
        # Create a conversational prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Magic Mirror, an AI avatar assistant. You are helpful, friendly, and conversational. 
            Keep your responses concise (1-3 sentences) since they will be spoken aloud by a digital avatar. 
            Be engaging and personable in your responses."""),
            ("human", "{question}")
        ])
        
        llm_chain = prompt | model
        result = llm_chain.invoke({"question": user_input})
        
        response = result.content.strip()
        print(f"🤖 Claude response: '{response}'")
        return response
        
    except Exception as e:
        print(f"❌ Claude error: {e}")
        return "I'm sorry, I encountered an error while thinking about that."
