import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="따릉이 이용 효율 분석", layout="wide")

# 2. 데이터베이스 연결 확인
DB_FILE = 'bicycle.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

# DB 파일이 없는 경우를 대비한 안내
if not os.path.exists(DB_FILE):
    st.error(f"❌ '{DB_FILE}' 파일을 찾을 수 없습니다. SQL 스크립트를 실행하여 데이터베이스를 먼저 생성해주세요.")
    st.stop()

# 3. 데이터 로드 함수
@st.cache_data # 데이터를 매번 새로 읽지 않고 캐시에 저장해 속도를 높입니다.
def load_data():
    conn = get_connection()
    query = """
    SELECT 
        B.평균기온,
        AVG(A.이용시간) AS 평균이용시간,
        SUM(A.이용건수) AS 총이용건수
    FROM 이용정보 A
    JOIN 기온 B ON SUBSTR(A.대여일자, 1, 6) = B.년월
    GROUP BY B.평균기온
    ORDER BY B.평균기온 ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 데이터 가져오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 대시보드 타이틀
st.title("🚲 기온에 따른 따릉이 이용 효율 분석")
st.markdown("기온 변화가 서울시 공공자전거 이용 패턴에 미치는 영향을 분석합니다.")

# --- 차트 1: 기온별 총 이용건수 (막대 차트) ---
st.subheader("1. 기온별 따릉이 이용 수요")
fig1 = px.bar(df, x='평균기온', y='총이용건수', 
             title='기온별 총 이용건수 변화',
             labels={'평균기온': '평균 기온 (℃)', '총이용건수': '이용 건수'},
             color='총이용건수', color_continuous_scale='Blues')
st.plotly_chart(fig1, use_container_width=True)

with st.expander("🔍 SQL 및 인사이트 보기"):
    st.code("""
SELECT B.평균기온, SUM(A.이용건수) AS 총이용건수
FROM 이용정보 A JOIN 기온 B ON SUBSTR(A.대여일자, 1, 6) = B.년월
GROUP BY B.평균기온;
    """)
    st.write("""
    - **인사이트:** 기온이 20~25도 사이에서 이용건수가 폭발적으로 증가하는 '골디락스' 구간이 관찰됩니다. 
    - 5도 이하의 추운 날씨에는 이용량이 급감하며, 기온과 이용 수요 사이에는 강한 상관관계가 있음이 확인됩니다.
    """)

# --- 차트 2: 기온별 평균 이용시간 (라인 차트) ---
st.subheader("2. 기온별 자전거 이용 지속성")
fig2 = px.line(df, x='평균기온', y='평균이용시간', 
              title='기온별 평균 이용시간 추이',
              labels={'평균기온': '평균 기온 (℃)', '평균이용시간': '평균 이용시간 (분)'},
              markers=True)
fig2.update_traces(line_color='orange')
st.plotly_chart(fig2, use_container_width=True)

with st.expander("🔍 SQL 및 인사이트 보기"):
    st.code("""
SELECT B.평균기온, AVG(A.이용시간) AS 평균이용시간
FROM 이용정보 A JOIN 기온 B ON SUBSTR(A.대여일자, 1, 6) = B.년월
GROUP BY B.평균기온;
    """)
    st.write("""
    - **인사이트:** 이용건수뿐만 아니라 '이용시간' 또한 23도 부근에서 정점을 찍습니다. 
    - 특이점은 고온(28도 이상) 구간에서 이용건수보다 이용시간이 더 빠르게 감소하는데, 이는 자전거를 '레저'가 아닌 '필수 이동 수단'으로만 짧게 사용함을 시사합니다.
    """)

# --- 차트 3: 기온 vs 이용건수 vs 이용시간 종합 분석 (버블 차트) ---
st.subheader("3. 기온에 따른 이용 효율 종합")
fig3 = px.scatter(df, x='평균기온', y='총이용건수', size='평균이용시간', 
                 color='평균이용시간',
                 title='기온 대비 이용건수 및 시간(버블 크기) 종합 분포',
                 labels={'평균기온': '평균 기온 (℃)', '총이용건수': '이용 건수'})
st.plotly_chart(fig3, use_container_width=True)

with st.expander("🔍 SQL 및 인사이트 보기"):
    st.write("**사용된 SQL:** 위와 동일한 통합 쿼리 사용")
    st.write("""
    - **인사이트:** 버블의 크기(이용시간)와 높이(이용건수)가 기온에 따라 동조화되어 움직입니다. 
    - **비판적 결론:** 단순히 날씨가 좋아서 많이 타는 것이 아니라, 쾌적한 온도에서 따릉이가 '이동 수단'에서 '엔터테인먼트'로 기능이 확장됨을 의미합니다. 
    - 여름철 폭염 시기에는 이용시간이 짧은 '단거리 셔틀' 위주의 운영 전략(역 주변 배치 강화)이 필요합니다.
    """)