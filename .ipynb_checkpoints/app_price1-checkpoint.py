import pandas as pd
import streamlit as st
from io import BytesIO

# 페이지 기본 설정
st.set_page_config(page_title="(TEST)약가 검색", layout="wide")
st.header('약가 검색')
st.text('해당 성분 혹은 제품의 등재 품목 수와 최고가, 최저가를 알려줍니다!')

# 데이터 파일 읽기
df = pd.read_excel("약가.xlsx")

# 검색어 입력받기
search_term = st.text_input("성분명(소문자 영문)을 입력하세요.")

# 검색 기능
if search_term:
    # Spinner 적용
    with st.spinner('검색 중입니다...'):
        # 입력 값이 문자열인지 확인
        if isinstance(search_term, str):
            try:
                # 제품코드 및 제품명 검색
                matching_code_df = df[df["제품코드"].astype(str).str.contains(search_term, na=False)]
                matching_name_df = df[df["제품명"].astype(str).str.contains(search_term, na=False)]

                # 검색 결과 합치기 및 중복 제거
                matching_df = pd.concat([matching_code_df, matching_name_df]).drop_duplicates()

                if not matching_df.empty:
                    result_df = matching_df.copy()
                    main_component_codes = matching_df["주성분코드"].unique()

                    # 새로운 열 추가
                    result_df["같은 주성분코드 개수"] = 0
                    result_df["최고 상한금액"] = 0
                    result_df["최저 상한금액"] = 0

                    # 주성분 코드별 같은 성분 개수, 최고/최저 상한금액 계산
                    for main_component_code in main_component_codes:
                        same_code_count = (df['주성분코드'] == main_component_code).sum() - 1
                        first_matching_index = result_df[result_df['주성분코드'] == main_component_code].index[0]
                        result_df.at[first_matching_index, "같은 주성분코드 개수"] = same_code_count

                        matching_prices = df[df["주성분코드"] == main_component_code]["상한금액"]
                        max_price = matching_prices.max()
                        min_price = matching_prices.min()

                        result_df.at[first_matching_index, "최고 상한금액"] = max_price
                        result_df.at[first_matching_index, "최저 상한금액"] = min_price

                    # 결과 출력
                    st.success("검색이 완료되었습니다!")
                    st.write("검색 결과", result_df)

                    # Excel 파일 생성 및 다운로드 버튼 추가
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False)
                    output.seek(0)

                    st.download_button(
                        label="검색 결과 다운로드",
                        data=output,
                        file_name="성분_약가.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                else:
                    st.warning(f"'제품코드, 제품명' 열에서 '{search_term}'를 포함하는 행을 찾을 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("유효한 문자열 검색어를 입력하세요.")

# 검색어 입력받기
search_term = st.text_input("제품명을 입력하세요.")

# 검색 기능
if search_term:
    # Spinner 적용
    with st.spinner('검색 중입니다...'):
        # 입력 값이 문자열인지 확인
        if isinstance(search_term, str):
            try:
                # 제품코드 및 제품명 검색
                matching_code_df = df[df["제품코드"].astype(str).str.contains(search_term, na=False)]
                matching_name_df = df[df["제품명"].astype(str).str.contains(search_term, na=False)]

                # 검색 결과 합치기 및 중복 제거
                matching_df = pd.concat([matching_code_df, matching_name_df]).drop_duplicates()

                if not matching_df.empty:
                    result_df = matching_df.copy()
                    main_component_codes = matching_df["주성분코드"].unique()

                    # 새로운 열 추가
                    result_df["같은 주성분코드 개수"] = 0
                    result_df["최고 상한금액"] = 0
                    result_df["최저 상한금액"] = 0

                    # 주성분 코드별 같은 성분 개수, 최고/최저 상한금액 계산
                    for main_component_code in main_component_codes:
                        same_code_count = (df['주성분코드'] == main_component_code).sum() - 1
                        first_matching_index = result_df[result_df['주성분코드'] == main_component_code].index[0]
                        result_df.at[first_matching_index, "같은 주성분코드 개수"] = same_code_count

                        matching_prices = df[df["주성분코드"] == main_component_code]["상한금액"]
                        max_price = matching_prices.max()
                        min_price = matching_prices.min()

                        result_df.at[first_matching_index, "최고 상한금액"] = max_price
                        result_df.at[first_matching_index, "최저 상한금액"] = min_price

                    # 결과 출력
                    st.success("검색이 완료되었습니다!")
                    st.write("검색 결과", result_df)

                    # Excel 파일 생성 및 다운로드 버튼 추가
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False)
                    output.seek(0)

                    st.download_button(
                        label="검색 결과 다운로드",
                        data=output,
                        file_name="제품_약가.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                else:
                    st.warning(f"'제품코드, 제품명' 열에서 '{search_term}'를 포함하는 행을 찾을 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("유효한 문자열 검색어를 입력하세요.")

