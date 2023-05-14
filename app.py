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
st.set_page_config(page_title=" Cook bot", page_icon=":robot:")
st.title("Cook bot powered with LLMs")
st.write("By Maximilien ")

if "generated" not in st.session_state:
	st.session_state["generated"] = []

if "past" not in st.session_state:
	st.session_state["past"] = []


def get_text():
	st.header("enter the city you want to know the best food")
	input_text = st.text_input("", key="input")
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
