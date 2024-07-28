import time
from openai import OpenAI
import streamlit as st
import os

assistant_id = 'asst_gSo5oyon5bH785Wcw59V2obe'
openai_api_key = st.secrets['OPENAPI_KEY']
client = OpenAI(api_key=openai_api_key)
# thread_id = 'thread_dZa3CREaD7kBBtlgZIoALyYb'
thread = client.beta.threads.create()
thread_id = thread.id
st.title("KCC글라스 사내규정 챗봇")

vector_id ='vs_syyWW8UtZcNVf54nyrQxp40G'

assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
)


if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"assistant","content":"안녕하세요, 사내 규정에 대해 질문해주세요."}]
    st.caption("Groupware > 사내정보 > 기타정보 > KCC 사규/매뉴얼 관리시스템에서도 확인 할 수 있습니다.")
    st.success("규정 카테고리 : [인력운영]  [인력개발]  [인사행정]  [전산]  [경영일반]  [정보보호]  [거버넌스]", icon="✔️")
    st.warning(" 사용자가 많을 경우 답변이 느려질 수 있습니다.", icon="⚠️")
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

        thread_messsage = client.beta.threads.messages.list(thread_id)
        msg = thread_messsage.data[0].content[0].text.value
        time.sleep(1)
        st.session_state.messages.append({"role": "assisant", "content": msg})

      
        if run.status == 'completed':
            st.chat_message("assistant").write(msg)
            break
        else:
            st.chat_message("assistant").write("규정을 찾을 수 없습니다.")
            break
            print(run.status)

