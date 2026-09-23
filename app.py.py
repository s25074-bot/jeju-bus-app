import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="제주 버스 노선 검색", page_icon="🚌")

st.title("🚌 제주 버스 목적지 검색 서비스")
st.write("찾으시는 목적지(정류장 또는 주요 경유지)를 입력하시면 관련 버스 노선을 확인하실 수 있습니다.")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("bus_data.csv")

try:
    df = load_data()

    # 목적지 입력창
    destination = st.text_input("목적지(종착지 또는 경유지)를 입력하세요", placeholder="예: 한라병원, 성산, 제주대학교, 공항")

    if destination:
        # 입력한 검색어가 route_info(운행계통)에 포함되어 있는지 검색
        filtered_df = df[df['route_info'].str.contains(destination, case=False, na=False)]

        if not filtered_df.empty:
            st.success(f"'{destination}'(을)를 경유하는 버스가 총 {len(filtered_df)}대 검색되었습니다.")
            
            # 결과 테이블 표시
            st.dataframe(
                filtered_df[['bus_no', 'route_type', 'route_info']],
                column_config={
                    "bus_no": "노선 번호",
                    "route_type": "노선 유형",
                    "route_info": "운행 계통 (주요 경유지)"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning(f"'{destination}'(을)를 경유하는 버스 노선을 찾을 수 없습니다. 다른 검색어를 입력해 보세요.")

except Exception as e:
    st.error("데이터 파일(bus_data.csv)을 불러오는 중 오류가 발생했습니다.")