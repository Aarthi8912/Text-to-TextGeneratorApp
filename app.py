import streamlit as st
import cohere
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Optional, List


# Correct implementation of custom LLM with Cohere
class CohereLLM(LLM):
    def __init__(self, api_key: str):
        super().__init__()
        self._api_key = api_key
        self._client = cohere.Client(self._api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._client.generate(
            model="command",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.generations[0].text.strip()

    @property
    def _llm_type(self) -> str:
        return "cohere"


# Replace this with your real Cohere API key
COHERE_API_KEY = "q2LuTzyDJOwEDn2Uay7I6erj1qIiRn3jPzWnZZRU"

# Initialize the custom LLM
llm = CohereLLM(api_key=COHERE_API_KEY)

# LangChain Prompt and Chain
prompt_template = PromptTemplate(
    input_variables=["input_text"],
    template="Paraphrase the following sentence:\n\n{input_text}"
)
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit App UI
st.set_page_config(page_title="Text-to-Text App", layout="centered")
st.title("📝 Text-to-Text Transformer (Cohere + LangChain)")

user_input = st.text_area("Enter your text to paraphrase", height=150)

if st.button("Paraphrase"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating paraphrased text..."):
            output = chain.run(input_text=user_input)
            st.success("Paraphrased Text:")
            st.write(output)
