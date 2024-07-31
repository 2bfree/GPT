import time
from openai import OpenAI
import streamlit as st
import os


assistant_id = st.secrets['ASSISTANT_ID']
openai_api_key = st.secrets['OPENAPI_KEY']
# openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

thread = client.beta.threads.create()
thread_id = thread.id
st.title("KCC글라스 사내규정 챗봇")

vector_id = st.secrets['VECTOR_ID']

assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
)

st.sidebar.title('규정 카테고리')
st.sidebar.header('[경영]')
st.sidebar.text(' - 국내/해외출장')
st.sidebar.text(' - 복리후생')
st.sidebar.text(' - 문서관리/보관')
st.sidebar.text(' - 인증서관리')
st.sidebar.text(' - 동호회지원')
st.sidebar.text(' - 경조금지급')
st.sidebar.text(' - 자가운전보조금 등 ')
st.sidebar.text(' - 개인휴대전화지원')
st.sidebar.text(' - 장학금지급')
st.sidebar.text(' - 주택자금대부')
st.sidebar.text(' - 생활안전자금대부')
st.sidebar.text(' - 의료비지원')
st.sidebar.text(' - 질병위로금')
st.sidebar.text(' - 노하우자료관리')
st.sidebar.text(' - 전자문서결재')
st.sidebar.text(' - 업무매뉴얼관리')
st.sidebar.text(' ')

st.sidebar.header('[인사]')
st.sidebar.text(' - 취업규칙')
st.sidebar.text(' - 촉탁사원관리')
st.sidebar.text(' - 근태관리시행')
st.sidebar.text(' - 해외주재원처우')
st.sidebar.text(' - 연수규정')
st.sidebar.text(' - 자기계발지원')
st.sidebar.text(' - 징계/포상')
st.sidebar.text(' - 신원재정보증업무')
st.sidebar.text(' - 관계사간 전출입시 급여 등 지급규칙')
st.sidebar.text(' - 하자 및 폐기발생에 대한 사후조치')
st.sidebar.text(' - 회수불능채권에 대한 사후조치')
st.sidebar.text(' ')

st.sidebar.header('[안전]')
st.sidebar.text(' - 안전보건관리')
st.sidebar.text(' - 비상시업무')
st.sidebar.text(' - 보안')
st.sidebar.text(' - 당직근무')
st.sidebar.text(' - 안전사고발생에 대한 사후조치')
st.sidebar.text(' ')

st.sidebar.header('[정보보호]')
st.sidebar.text(' - 정보보호관리규정')
st.sidebar.text(' - 정보보호조직운영규칙')
st.sidebar.text(' - 정보자산관리규칙')
st.sidebar.text(' - 인적보안규칙')
st.sidebar.text(' - 어플리케이션보안관리규칙')
st.sidebar.text(' - 물리적보안규칙')
st.sidebar.text(' - 침해사고대응규칙')
st.sidebar.text(' - 외주관리규칙')
st.sidebar.text(' - 개인정보보호내부관리계획')
st.sidebar.text(' - 정보보호감사규칙')
st.sidebar.text(' - 정보보호교육규칙')
st.sidebar.text(' - 개인PC보안규칙')
st.sidebar.text(' - 암호화관리규칙')
st.sidebar.text(' - 개발보안규칙')
st.sidebar.text(' - IT재해복구규칙')
st.sidebar.text(' - IT운영보안규칙(서버)')
st.sidebar.text(' - IT운영보안규칙(DB)')
st.sidebar.text(' - IT운영보안규칙(네트워크)')
st.sidebar.text(' - IT운영보안규칙(정보보호시스템)')
st.sidebar.text(' ')

st.sidebar.header('[자산]')
st.sidebar.text(' - 부동산관리')
st.sidebar.text(' - 차량관리')
st.sidebar.text(' - 자산처분심의')
st.sidebar.text(' - 사택관리')
st.sidebar.text(' - 교통법규위반 및 차량사고처리')
st.sidebar.text(' ')

st.sidebar.header('[대외일반]')
st.sidebar.text(' - 준법규정')
st.sidebar.text(' - 법률자문 및 송무처리규정')
st.sidebar.text(' - 준법규칙')
st.sidebar.text(' - 내부신고제도운영규칙')
st.sidebar.text(' - 내부감사규정')
st.sidebar.text(' ')

st.sidebar.header('[거버넌스]')
st.sidebar.text(' - 감사위원회')
st.sidebar.text(' - 이사회운영')
st.sidebar.text(' - 사외이사후보추천위원회')
st.sidebar.text(' - 내부거래위원회')
st.sidebar.text(' - 내부ESG위원회')
st.sidebar.text(' - 보상위원회')
st.sidebar.subheader(' ')

st.sidebar.header('[전산]')
st.sidebar.text(' - 전산관리규정')
st.sidebar.text(' - 업무전산화규칙')
st.sidebar.text(' - 백업관리규칙')
st.sidebar.text(' - 데이터베이스 및 프로그램관리')
st.sidebar.text(' - 전산기기관리규칙')
st.sidebar.text(' - 소프트웨어관리규칙')



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 사내 규정에 대해 질문해주세요."}]
    st.caption("Groupware > 사내정보 > 기타정보 > KCC 사규/매뉴얼 관리시스템에서도 확인 할 수 있습니다.")
    st.success(" 구체적이고 명확하게 30자 이내로 질문해주세요. ex) 휴대전화 지원 대상하고 금액 알려줘. ", icon="✔️")
    st.caption("  ⚠️사용자가 많을 경우 답변이 느려질 수 있습니다.")

st.divider()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Check your Open API Key")
        st.stop()

    if not thread_id:
        st.info("Check your Thread ID")
        st.stop()

    max_len = 50

    if len(prompt) < max_len:

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )
        while True:
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant.id,
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
    else :
        st.error('입력 단어 개수를 초과했습니다. '+str(max_len)+'자 이내로 입력해주세요!')

