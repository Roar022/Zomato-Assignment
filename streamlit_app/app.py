import streamlit as st
from src.helper import ZomatoBot
from src.prompt import PROMPT

class FoodieApp:
    def _init_(self):
        self.bot = ZomatoBot()
        self.SYSTEM_INITIAL = PROMPT
        if "strorage" not in st.session_state:
            st.session_state.strorage = []

    def run(self):
        st.set_page_config(page_title="Foodie Bot", page_icon="🍔", layout="wide")
        st.markdown("<h1 style='text-align: center; color: #2D6BF7;'> Welcome to Foodie Bot</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Ask me anything about restaurants, dishes, prices, or recommendations!</p>", unsafe_allow_html=True)
        

        self.render_chat_history()
        

        user_input = st.chat_input("Type your message here...")
        if user_input:
            self.process_user_input(user_input)

    def process_user_input(self, user_input: str):

        if (
            st.session_state.strorage 
            and st.session_state.strorage[-1]["role"] == "user" 
            and st.session_state.strorage[-1]["content"] == user_input
        ):
            return


        messages = st.session_state.strorage + [{"role": "user", "content": user_input}]


        assistant_reply = self.bot.generate_reply(messages, user_input)


        st.session_state.strorage.append({"role": "user", "content": user_input})
        if assistant_reply:
            st.session_state.strorage.append({"role": "assistant", "content": assistant_reply})

        st.rerun()


    def render_chat_history(self):

        for msg in st.session_state.strorage:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-end; margin-bottom: 10px;'>
                        <div style='background-color: #E7EEF9; padding: 10px; border-radius: 10px; max-width: 70%;'>
                            {msg['content']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                #st.markdown(f"<div style='background-color:#E7EEF9;padding:10px;border-radius:10px;margin-bottom:10px;max-width:70%;'>{msg['content']}</div>", unsafe_allow_html=True)
                #st.chat_message("user").write(msg["content"])
            elif msg["role"] == "assistant":
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-start; margin-bottom: 10px;'>
                        <div style='background-color: #F1F0F0; padding: 10px; border-radius: 10px; max-width: 70%;'>
                            {msg['content']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                #st.markdown(f"<div style='background-color:#F1F0F0;padding:10px;border-radius:10px;margin-bottom:10px;max-width:70%;'>{msg['content']}</div>", unsafe_allow_html=True)
                #st.chat_message("assistant").write(msg["content"])

if __name__ == "__main__":
    app = FoodieApp()
    app.run()