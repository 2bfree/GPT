import time
from openai import OpenAI
import streamlit as st
import os

# API 키 및 Assistant 설정
openai_api_key = st.secrets['OPENAPI_KEY']
assistant_id = 'asst_gSo5oyon5bH785Wcw59V2obe'
client = OpenAI(api_key=openai_api_key)

# 스레드 생성
thread = client.beta.threads.create()
thread_id = thread.id
vector_id = 'vs_syyWW8UtZcNVf54nyrQxp40G'

# Streamlit UI 설정
st.title("SFA 검색")

# 어시스턴트 설정
assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
)

# 사이드바 설정
st.sidebar.title('규정 카테고리')

# 각 카테고리별 규정 리스트 추가
categories = {
    '[경영]': ['국내/해외출장', '복리후생', '문서관리/보관', '인증서관리', '동호회지원', '경조금지급', 
              '자가운전보조금 등', '개인휴대전화지원', '장학금지급', '주택자금대부', '생활안전자금대부', 
              '의료비지원', '질병위로금', '노하우자료관리', '전자문서결재', '업무매뉴얼관리'],
    
    '[인사]': ['취업규칙', '촉탁사원관리', '근태관리시행', '해외주재원처우', '연수규정', '자기계발지원', 
             '징계/포상', '신원재정보증업무', '관계사간 전출입시 급여 등 지급규칙', '하자 및 폐기발생에 대한 사후조치', 
             '회수불능채권에 대한 사후조치'],
    
    '[안전]': ['안전보건관리', '비상시업무', '보안', '당직근무', '안전사고발생에 대한 사후조치'],
    
    '[정보보호]': ['정보보호관리규정', '정보보호조직운영규칙', '정보자산관리규칙', '인적보안규칙', 
                 '어플리케이션보안관리규칙', '물리적보안규칙', '침해사고대응규칙', '외주관리규칙', 
                 '개인정보보호내부관리계획', '정보보호감사규칙', '정보보호교육규칙', '개인PC보안규칙', 
                 '암호화관리규칙', '개발보안규칙', 'IT재해복구규칙', 'IT운영보안규칙(서버)', 'IT운영보안규칙(DB)', 
                 'IT운영보안규칙(네트워크)', 'IT운영보안규칙(정보보호시스템)'],
    
    '[자산]': ['부동산관리', '차량관리', '자산처분심의', '사택관리', '교통법규위반 및 차량사고처리'],
    
    '[대외일반]': ['준법규정', '법률자문 및 송무처리규정', '준법규칙', '내부신고제도운영규칙', '내부감사규정'],
    
    '[거버넌스]': ['감사위원회', '이사회운영', '사외이사후보추천위원회', '내부거래위원회', '내부ESG위원회', '보상위원회'],
    
    '[전산]': ['전산관리규정', '업무전산화규칙', '백업관리규칙', '데이터베이스 및 프로그램관리', '전산기기관리규칙', '소프트웨어관리규칙'],
}

for header, items in categories.items():
    st.sidebar.header(header)
    for item in items:
        st.sidebar.text(f" - {item}")

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 사내 규정에 대해 질문해주세요."}]
    st.caption("Groupware > 사내정보 > 기타정보 > KCC 사규/매뉴얼 관리시스템에서도 확인 할 수 있습니다.")
    st.success("구체적이고 명확하게 30자 이내로 질문해주세요. ex) 휴대전화 지원 대상하고 금액 알려줘.", icon="✔️")
    st.caption("⚠️사용자가 많을 경우 답변이 느려질 수 있습니다.")

st.divider()

# 메시지 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
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
            content=f"{prompt} 참조 빼고 말해줘"
        )

        while True:
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant.id,
            )

            thread_message = client.beta.threads.messages.list(thread_id)
            msg = thread_message.data[0].content[0].text.value

            time.sleep(1)
            st.session_state.messages.append({"role": "assistant", "content": msg})

            if run.status == 'completed':
                st.chat_message("assistant").write(msg)
                break
            else:
                st.chat_message("assistant").write("규정을 찾을 수 없습니다.")
                break
    else:
        st.error(f'입력 단어 개수를 초과했습니다. {max_len}자 이내로 입력해주세요!')
