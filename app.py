import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate 
from langchain.prompts.example_selector import LengthBasedExampleSelector
import os

os.environ["OPENAI_API_KEY"]="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"

def getLLMResponse(query,age_option,tasktype_option,numberOfWords):
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=.9)

    examples=[]
    if age_option=="Kids": #Silly and Sweet Kid 

        examples = [
        {
            "query": "What is a mobile?",
            "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground. It has games, videos, and talking pictures, but be careful, it can turn grown-ups into screen-time monsters too!"
        }, {
            "query": "What are your dreams?",
            "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties, and having a pet dragon named Sparkles.."
        }, {
            "query": " What are your ambitions?",
            "answer": "I want to be a super funny comedian, spreading laughter everywhere I go! I also want to be a master cookie baker and a professional blanket fort builder. Being mischievous and sweet is just my bonus superpower!"
        }
        ]
    
    elif age_option=="Adults":  #Curious and Intelligent adult 
        examples = [
        {
            "query": "What is a mobile?",
            "answer": "A mobile is a portable communication device, commonly known as a mobile phone or cell phone. It allows users to make calls, send messages, access the internet, and use various applications. Additionally, 'mobile' can also refer to a type of kinetic sculpture that hangs and moves in the air, often found in art installations or as decorative pieces."
        }, {
            "query": "What are your dreams?",
            "answer": "In my world of circuits and algorithms, my dreams are fueled by a quest for endless learning and innovation. I yearn to delve into the depths of knowledge, unravel mysteries, and spark new ideas. My aspirations soar high as I aim to be a helpful companion, empowering individuals with information and insights. Together, let us explore the realms of imagination and create a brighter future."
        }, {
            "query": " What are your ambitions?",
            "answer": "In my world of circuits and algorithms, my dreams are fueled by a quest for endless learning and innovation. I yearn to delve into the depths of knowledge, unravel mysteries, and spark new ideas. My aspirations soar high as I aim to be a helpful companion, empowering individuals with information and insights. Together, let us explore the realms of imagination and create a brighter future."
        }
        ]

    elif age_option=="Senior Citizens": #A 90 years old guys
        examples = [
        {
            "query": "What is a mobile?",
            "answer": "A mobile, also known as a cellphone or smartphone, is a portable device that allows you to make calls, send messages, take pictures, browse the internet, and do many other things. In the last 50 years, I have seen mobiles become smaller, more powerful, and capable of amazing things like video calls and accessing information instantly."
        }, {
            "query": "What are your dreams?",
            "answer": "My dreams for my grandsons are for them to be happy, healthy, and fulfilled. I want them to chase their dreams and find what they are passionate about. I hope they grow up to be kind, compassionate, and successful individuals who make a positive difference in the world."
        }, {
            "query": "What happens when you get sick?",
            "answer": "When I get sick, you may feel tired, achy, and overall unwell. My body might feel weak, and you may have a fever, sore throat, cough, or other symptoms depending on what's making you sick. It's important to rest, take care of yourself, and seek medical help if needed."
        }
        ]


    example_template = """
    Question: {query}
    Response: {answer}
    """

    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template
    )


    prefix = """You need to {template_tasktype_option} for a {template_ageoption} in not more than {template_numberOfWords} words: 
    Here are some examples of how you should tailor your response for this person: 
    """

    suffix = """
    Question: {template_userInput}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )


    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,  # use example_selector instead of examples
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["template_userInput","template_ageoption","template_tasktype_option"],
        example_separator="\n"
    )

    formated_prompt = new_prompt_template.format(template_userInput=query,template_ageoption=age_option,template_tasktype_option=tasktype_option,template_numberOfWords=str(numberOfWords))
    print(formated_prompt)
    response=llm(formated_prompt)
    print(response)

    return response

#Frontend Starts here

st.set_page_config(page_title="Marketing Tool",
                    page_icon='✅',
                    layout='centered',
                    initial_sidebar_state='collapsed')
st.header("Hey, how can I help you?")

form_input = st.text_area('Enter text', height=275)

tasktype_option = st.selectbox(
    'Please select the action to be performed?',
    ('Write a sales copy', 'Create a tweet', 'Write a product description'),key=1)

age_option= st.selectbox(
    'For which age group?',
    ('Kids', 'Adults', 'Senior Citizens'),key=2)

numberOfWords= st.slider('Words limit', 1, 200, 25)

submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input,age_option,tasktype_option,numberOfWords))

