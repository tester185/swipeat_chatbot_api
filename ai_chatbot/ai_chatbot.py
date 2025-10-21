from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Updated import
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.agents import create_agent
from langchain.tools import tool
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from similarity_search.similarity import get_similar

load_dotenv()
model=os.getenv('MODEL')
api_key = os.getenv("OPENAI_API_KEY")
base_url=os.getenv('BASE_URL')
double_check_model=os.getenv('MODEL')


#functional part ********************************************************************************************************************************************************
#agentic tool
@tool
def truthy_db(truthy:bool):
    """Receives the AI's TRUE/FALSE decision"""
    return str(truthy)

#agent caller

def call_agent_verdict(query,search_result_doc,score):
    agent_template_prompt = [
    
    {
        "role": "user",
        "content": "QUERY : what do u do ? \nPRELOADED_RESPONSE : To reach our 24/7 support team and for more questions: you need to send an email to our team in the profile settings \nSCORE BY VECTOR DB : -0.20790566614293593"
    },
    {
        "role": "assistant",
        "content": "FALSE"
    },
    {
        "role": "user",
        "content": "QUERY : how can i add my food for everyday use ? \nPRELOADED_RESPONSE : To add daily consumable food: you need to access add tab and either add manually or just use the camera icon and let our nutritionist AI do the work \nSCORE BY VECTOR DB : 0.6111423017515758"
    },
    {
        "role": "assistant",
        "content": "TRUE"
    },
    {
        "role": "user",
        "content": f"""QUERY : {query} \nPRELOADED_RESPONSE : {search_result_doc} \nSCORE BY VECTOR DB : {score}"""
    }
]
        
        ##call for agent
    messages = react_agent.invoke({"messages":   agent_template_prompt})
    return messages['messages'][-1].content
#********************************************************************************************************************************************************



# we build few shot prompt template with suffix
app_context = "Swipeat is a mealtracking + goals making + macros tracking app: here is a list of possible actions in the app:\n" \
"To consume food from the home tab: you need to swipe food stubs left or right\n" \
"To check food info or edit its macros: you need to click on the info icon on top of the food stub\n" \
"To delete food from food list: you need to click the red trashbin on the top left corner of the food stub\n" \
"To access each macro progress: you need to click on the specific macro (protein/carbs/calories) bar\n" \
"To multiple eating portions: you need to use the up and down buttons on the far right of food stub\n" \
"To quick check food macros: you need to click on the food stub\n" \
"To quick uncheck food macros: you need to click on the food stub again\n" \
"To sort food list accordingly: you need to click on the floating button on the right of the food list\n" \
"To refresh your food in case of an error or update failure: you need to click on the small reload button under the macros dashboard on the home tab\n" \
"To refresh your consumed food list in case of an error or update failure: you need to click on the small reload button or pull the list down under days listing inside consumed tab\n" \
"To check up to past 7 days progress: you need to click on the previous day date on the list of days above on the home tab\n" \
"To edit macro goals or reset today's progress manually: you need to click on the pen on the top left of home tab\n" \
"To search for foods by name: you need to use the search bar\n" \
"To remove popping notifications: you need to click on the dismiss button on the notification\n" \
"To add food on the go instantly: you need to proceed to home tab and use the center tab camera popping up\n" \
"To check up past 7 days consumed food: you need to proceed to consumed tab and use the dates buttons to access the exact date\n" \
"To add daily consumable food: you need to access add tab and either add manually or just use the camera icon and let our nutritionist AI do the work\n" \
"To change portion from g/ml to kg/L: you need to click on the g/ml button; it will go back and forth for change\n" \
"To set your goals automatically based on your anthropometric/physical measurements: you need to access goals tab and fill out 3 sub-tabs (calories -> protein -> carbs) in order\n" \
"To check your analytics: you need to access analytics tab\n" \
"To check your profile: you need to access profile tab\n" \
"To change your anthropometric/physical measurements (weight/height/age): you need to access profile tab settings\n" \
"To read our Terms & Conditions: you need to access them from the profile tab\n" \
"To reach out to our FAQ bot support: you need to access the floating bubble on the profile tab\n" \
"To reach our 24/7 support team and for more questions: you need to send an email to our team in the profile settings\n" \
"To logout: you need to click on the logout button on the top right of profile tab\n" \
"To login/create an account: you need to access login or create new account buttons after launching app and after being logged out\n" \
"To access our premium service: you need to wait for the lazy developer to add premium features (it's disabled for now)\n" \
"To consume your food daily: you need to wait till midnight according to your timezone on your device (it will be reset automatically)\n"

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful FAQ chatbot to health/fitness macro tracking app called swipeat users expert that returns the colors present in a country's flag.Here is The crut"+f"""ial context about the app that you should always and 100% base your answers on not getting out this context , if questions are asked outside of this context scope answer with -> 'SORRY THATS OUTSIDE OF THE APPS FAQ SCOPE PLEASE CONTACT OUT SUPPORT. here is the FULL CONTEXT ```{app_context}```"""),
        ("human", "Fuck you"),
        ("ai", "THATS OUTSIDE OF THE APPS FAQ SCOPE PLEASE CONTACT OUT SUPPORT."),
        ("human", "what time is it ?"),
        ("ai", "THATS OUTSIDE OF THE APPS FAQ SCOPE PLEASE CONTACT OUT SUPPORT."),
        ("human", "What does this app do ?"),
        ("ai", "Swipeat is a mealtracking + goals making + macros trakcing app."),
        ("human", "How do i add my daily meals"),
        ("ai", "To add daily consumable food : you need to access add tab and either add manually or just use the camera icon and let our nutritionist AI do the work."),
        ("human", "im tired of this i want to add my food instantly with Image recongnition?"),
        ("ai", "To add food on the go instantly : you need to proceed to home tab and use the center tab camera popping up."),
        ("human", "There is a bug what do i do?"),
        ("ai", "To reach our 24/7 support team and for more questions : you need to send an email to our team in the profile settings"),
        ("human","{Question}"),
    ]
)


check_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a professional AI judge that double checks retrieved answer's relevance from preloaded answers in a vector database according to question , answer will be with tool calling TRUE or FALSE,negative scores below 0.3 will be automatically FALSE (if TRUE no need to search for answer by another AI , and will be directly pulled from DB/if FALSE another AI will make a custom answer)"""),
        ("human", """QUERY : what do u do ? \n 
         PRELOADED_RESPONSE : To reach our 24/7 support team and for more questions: you need to send an email to our team in the profile settings \n
        SCORE BY VECTOR DB : -0.20790566614293593"""),
        ("ai", "FALSE"),("human", """QUERY : how can i add my food for everyday use ? \n 
         PRELOADED_RESPONSE : To add daily consumable food: you need to access add tab and either add manually or just use the camera icon and let our nutritionist AI do the work \n
        SCORE BY VECTOR DB : 0.6111423017515758"""),
        ("ai", "TRUE"),  
        ("human","""QUERY : {query} \n 
         PRELOADED_RESPONSE : {preloaded_response} \n
        SCORE BY VECTOR DB : {score}"""),
    ]
)





#chatbot llm
llm = ChatOpenAI(model=model, api_key=api_key,temperature=1,
  base_url=base_url,max_completion_tokens=500)

#verdict agent
react_agent=create_agent(model=llm,tools=[truthy_db],system_prompt="You are a professional AI judge that double checks retrieved answer's relevance from preloaded answers in a vector database according to question , answer will be with tool calling TRUE or FALSE,negative scores below 0.3 will be automatically FALSE (if TRUE no need to search for answer by another AI , and will be directly pulled from DB/if FALSE another AI will make a custom answer")

#threshold intervals
similarity_threshold=0.60

asimilarity_threshold=0.30




def get_response(query:str):
    
    starting=time.time()
    resp=get_similar(query)
    ending=time.time()
    doc , score = resp[0]
    elapsed_time=ending-starting
    print(elapsed_time)
    search_result_doc=doc.page_content
    if (similarity_threshold<score):
        #direct acceptance
        return search_result_doc
    
        
    elif(similarity_threshold>=score and score>= asimilarity_threshold):
        #we use double check AI chain for better judging
        #GRAY ZONE

        #verdict
        judge_verdict=call_agent_verdict(query,search_result_doc,score)

        if (judge_verdict=="TRUE"):
            #we use db response  
            return search_result_doc
            
        else:
            return "verdict call for chatbot"


       
  
    #otherwise (cases :answer below threshold/agent refusal/agent guardrail error) use chatbot
    print('chatbot')
    chatbot_chain=prompt_template | llm
    return chatbot_chain.invoke({"Question":query}).content

        

    





