import time
from openai import OpenAI
import streamlit as st
import os

assistant_id = st.secrets['ASSISTANT_ID']
openai_api_key = st.secrets['OPENAPI_KEY']
client = OpenAI(api_key=openai_api_key)
thread_id =st.secrets['THREAD_ID ']
vector_id =st.secrets['VECTOR_ID']

assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
)


if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"assistant","content":"안녕하세요, KCC글라스 사내규정 챗봇입니다. 무엇을 도와드릴까요?"}]
    st.caption("Groupware > 사내정보 > 기타정보 > KCC 사규/매뉴얼 관리시스템에서도 확인 할 수 있습니다.")
    st.info(" 간결하지만 구체적으로 질문해주세요.  :pushpin: 출장규정 알려줘 > 국내 출장 여비 알려줘" , icon="ℹ️" )
    st.info(" 사용자가 많을 경우 답변이 느려질 수 있습니다.", icon="ℹ️")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Check your Open API Key")
        st.stop()

    if not thread_id:
        st.info("Check your Thread ID")
        st.stop()

    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)



    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content= prompt
    )
    while True:
        run = client.beta.threads.runs.create_and_poll(
            thread_id = thread_id,
            assistant_id = assistant.id,
        )

        if run.status == 'completed':
            break
        else:
            break
            print(run.status)



    thread_messsage = client.beta.threads.messages.list(thread_id)
    msg = thread_messsage.data[0].content[0].text.value
    time.sleep(1)
    st.session_state.messages.append({"role": "assisant", "content": msg})
    st.chat_message("assistant").write(msg)


