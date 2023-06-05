"""Python file to serve as the frontend"""
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
token = os.environ.get("openai-key")
llm = OpenAI(temperature=1, openai_api_key=token)
def load_chain_loc():
	template = """Your job is to come up with a classic dish from the area that the users suggests.
	% USER LOCATION
	{user_location}

	YOUR RESPONSE:
	"""
	prompt_template = PromptTemplate(input_variables=["user_location"], template=template)

	# Holds my 'location' chain
	location_chain = LLMChain(llm=llm, prompt=prompt_template)
	return location_chain

loc_chain = load_chain_loc()


def  load_chain_meal():
	template = """Given a meal, give a short and simple recipe on how to make that dish at home.
	% MEAL
	{user_meal}

	YOUR RESPONSE:
	"""
	prompt_template = PromptTemplate(input_variables=["user_meal"], template=template)

	# Holds my 'meal' chain
	meal_chain = LLMChain(llm=llm, prompt=prompt_template)
	return meal_chain
	
chain_meal =load_chain_meal()

overall_chain = SimpleSequentialChain(chains=[loc_chain,chain_meal], verbose=True)

	
# From here down is all the StreamLit UI.
st.set_page_config(page_title=" Cook Assistant ", page_icon=":robot:")
st.title("Cook Assitant  Powered By  LLMs")
st.subheader('AI Web App implemented by [Maximilien Kpizingui](https://kpizmax.hashnode.dev)')
'''
The cooking assistant recommends personalized recipes based on your favorite city, provide expert cooking tips, and take your culinary skills to new heights! 
'''
st.image("@maximilien.png")

st.sidebar.markdown("Email: maximilien@tutanota.de")
st.sidebar.markdown("Element: @maximilien:matrix.org")

if "generated" not in st.session_state:
	st.session_state["generated"] = []

if "past" not in st.session_state:
	st.session_state["past"] = []


def get_text():
	st.subheader("Please enter the city to know the best recipe")
	input_text = st.text_input("waiting for input", key="input")
	return input_text


user_input = get_text()

if user_input:
	output = overall_chain.run(input=user_input)

	st.session_state.past.append(user_input)
	st.session_state.generated.append(output)
#	st.write(output)
if st.session_state["generated"]:

	for i in range(len(st.session_state["generated"]) - 1, -1, -1):
		message(st.session_state["generated"][i], key=str(i))
		message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
