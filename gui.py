import streamlit as st
from gpt_reader.paper.paper import Paper
from gpt_reader.pdf_reader import PaperReader


class GUI:
    def __init__(self):
        self.api_key = ""
        self.proxy = None  # {'http': xxxx, 'https': xxxx}
        self.session = ""
        self.paper = None

    def analyse(self, api_key, pdf_file, http_proxy):
        if http_proxy:  # if do not provide http_proxy, use the value in __init__ function
            self.proxy = {'http': http_proxy, 'https': http_proxy}
        if api_key:  # if do not provide api_key, use the value in __init__ function
            self.api_key = api_key
        self.session = PaperReader(self.api_key, proxy=self.proxy)
        self.paper = Paper(pdf_file.name)
        return self.session.summarize(self.paper)

    def ask_question(self, question):
        if self.session == "":
            return "Please upload PDF file first!"
        return self.session.question(self.paper, question)


def main():
    st.title("CHATGPT-PAPER-READER")

    with st.sidebar:
        st.markdown("## About this project")
        st.markdown(
            """CHATGPT-PAPER-READER 📝
            This repository provides a simple interface that utilizes the gpt-3.5-turbo
            model to read academic papers in PDF format locally. You can use it to help you summarize papers,
            create presentation slides, or simply fulfill tasks assigned by your supervisor.
            [Github](https://github.com/talkingwallace/ChatGPT-Paper-Reader)"""
        )

    st.markdown("# CHATGPT-PAPER-READER")

    with st.expander("Upload PDF File"):
        pdf_file = st.file_uploader("PDF File")
        api_key = st.text_input("OpenAI API Key, sk-***")
        http_proxy = st.text_input("Proxy, http://***:***, leave blank if you do not need proxy")
        start_analyze = st.button("Start Analyze")

    with st.expander("Ask question about your PDF"):
        question = st.text_input("Your Question", help="Authors of this paper?")
        ask = st.button("Ask")

    result = ""
    answer = ""

    app = GUI()

    if start_analyze:
        if pdf_file:
            result = app.analyse(api_key, pdf_file, http_proxy)
        else:
            result = "Please upload a PDF file."

    if ask:
        if question:
            answer = app.ask_question(question)
        else:
            answer = "Please enter a question."

    st.text_area("PDF Summary", value=result)
    st.text_area("Answer", value=answer)


if __name__ == "__main__":
    main()
