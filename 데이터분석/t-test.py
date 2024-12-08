import pandas as pd
import numpy as np
from scipy import stats
import warnings
import requests
import time
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

def get_subway_data(file_path):
    """CSV 파일에서 지하철 시간대별 승하차 데이터 가져오기"""
    try:
        # 다양한 인코딩 시도
        encodings = ['utf-8', 'cp949', 'euc-kr']
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"데이터 건수: {len(df)}")
                return df
            except UnicodeDecodeError:
                continue
        raise Exception("적절한 인코딩을 찾을 수 없습니다.")
    except Exception as e:
        print(f"데이터 읽기 중 오류 발생: {e}")
        return None

def preprocess_data(df):
    """데이터 전처리"""
    try:
        if df is None:
            return None
            
        print("\n=== 원본 데이터 컬럼 ===")
        print(df.columns.tolist())
        
        # 시간대별 데이터를 행으로 변환
        time_cols = [col for col in df.columns if '시' in col]
        base_cols = ['호선명', '지하철역']
        
        # 승차, 하차 데이터 분리
        ride_cols = [col for col in time_cols if '승차' in col]
        alight_cols = [col for col in time_cols if '하차' in col]
        
        # 승차 데이터 처리
        ride_df = df[base_cols + ride_cols].melt(
            id_vars=base_cols,
            var_name='시간',
            value_name='승차인원'
        )
        
        # 하차 데이터 처리
        alight_df = df[base_cols + alight_cols].melt(
            id_vars=base_cols,
            var_name='시간',
            value_name='하차인원'
        )
        
        # 시간 정보 추출 (예: "04시-05시 승차인원" -> "04시")
        ride_df['시간'] = ride_df['시간'].str.extract(r'(\d+)시-').astype(str) + '시'
        alight_df['시간'] = alight_df['시간'].str.extract(r'(\d+)시-').astype(str) + '시'
        
        # 승하차 데이터 병합
        df_processed = pd.merge(
            ride_df,
            alight_df,
            on=base_cols + ['시간']
        )
        
        # 컬럼명 변경
        df_processed = df_processed.rename(columns={
            '호선명': '호선',
            '지하철역': '역명'
        })
        
        # 숫자형 데이터 변환 및 결측치 처리
        df_processed['승차인원'] = pd.to_numeric(df_processed['승차인원'], errors='coerce').fillna(0)
        df_processed['하차인원'] = pd.to_numeric(df_processed['하차인원'], errors='coerce').fillna(0)
        
        # 총 이용객 계산
        df_processed['총이용객'] = df_processed['승차인원'] + df_processed['하차인원']
        
        # 서울 지하철 1~9호선만 필터링
        seoul_lines = [str(i) + '호선' for i in range(1, 10)]
        df_processed = df_processed[df_processed['호선'].isin(seoul_lines)]
        
        return df_processed
        
    except Exception as e:
        print(f"데이터 전처리 중 오류 발생: {e}")
        return None

def perform_ttest_analysis(df):
    """시간대별 승하차 인원에 대한 독립표본 t-검정 수행"""
    print("\n=== T-검정 결과 ===")
    
    try:
        # 유의수준 설정
        alpha = 0.05
        
        # 피크시간대 정의
        morning_peak_hours = [str(i) + '시' for i in range(7, 10)]  # 오전 7-9시
        evening_peak_hours = [str(i) + '시' for i in range(17, 20)]  # 오후 5-7시
        peak_hours = morning_peak_hours + evening_peak_hours
        
        # 피크시간대와 비피크시간대 데이터 분리
        peak_data = df[df['시간'].isin(peak_hours)]
        non_peak_data = df[~df['시간'].isin(peak_hours)]
        
        # 1. 승차 인원에 대한 t-test
        print("\n1. 승차 인원 분석 (피크시간대 vs 비피크시간대)")
        t_stat_on, p_value_on = stats.ttest_ind(peak_data['승차인원'], 
                                               non_peak_data['승차인원'])
        
        print(f"승차 인원 t-통계량: {t_stat_on:.4f}")
        print(f"승차 인원 p-value: {p_value_on:.20f}")
        print(f"피크시간대 평균 승차인원: {peak_data['승차인원'].mean():.2f}")
        print(f"비피크시간대 평균 승차인원: {non_peak_data['승차인원'].mean():.2f}")
        print(f"차이: {peak_data['승차인원'].mean() - non_peak_data['승차인원'].mean():.2f}")
        
        # 효과 크기(Cohen's d) 계산 추가
        pooled_std = np.sqrt((peak_data['승차인원'].var() + non_peak_data['승차인원'].var()) / 2)
        cohens_d = abs(peak_data['승차인원'].mean() - non_peak_data['승차인원'].mean()) / pooled_std
        print(f"효과 크기(Cohen's d): {cohens_d:.4f}")
        
        if p_value_on < alpha:
            print("결론: 승차 인원은 출퇴근 시간대와 통계적으로 유의미한 관계가 있음")
            if cohens_d > 0.8:
                print("(효과 크기가 큼)")
            elif cohens_d > 0.5:
                print("(효과 크기가 중간)")
            else:
                print("(효과 크기가 작음)")
        else:
            print("결론: 승차 인원은 출퇴근 시간대와 통계적으로 유의미한 관계가 없음")
        
        # 호선별 분석 추가
        print("\n=== 호선별 T-검정 결과 ===")
        for line in df['호선'].unique():
            print(f"\n{line} 분석")
            line_data = df[df['호선'] == line]
            peak_line = line_data[line_data['시간'].isin(peak_hours)]
            non_peak_line = line_data[~line_data['시간'].isin(peak_hours)]
            
            t_stat, p_value = stats.ttest_ind(peak_line['총이용객'], 
                                            non_peak_line['총이용객'])
            
            print(f"t-통계량: {t_stat:.4f}")
            print(f"p-value: {p_value:.20f}")
            print(f"피크시간대 평균: {peak_line['총이용객'].mean():.2f}")
            print(f"비피크시간대 평균: {non_peak_line['총이용객'].mean():.2f}")
            print(f"차이: {peak_line['총이용객'].mean() - non_peak_line['총이용객'].mean():.2f}")
            
            # 효과 크기 계산
            pooled_std = np.sqrt((peak_line['총이용객'].var() + non_peak_line['총이용객'].var()) / 2)
            cohens_d = abs(peak_line['총이용객'].mean() - non_peak_line['총이용객'].mean()) / pooled_std
            print(f"효과 크기(Cohen's d): {cohens_d:.4f}")
            
            if p_value < alpha:
                print("결론: 출퇴근 시간대와 통계적으로 유의미한 관계가 있음")
                if cohens_d > 0.8:
                    print("(효과 크기가 큼)")
                elif cohens_d > 0.5:
                    print("(효과 크기가 중간)")
                else:
                    print("(효과 크기가 작음)")
            else:
                print("결론: 출퇴근 시간대와 통계적으로 유의미한 관계가 없음")
        
        return True
        
    except Exception as e:
        print(f"T-검정 분석 중 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    # CSV 파일 경로 설정
    file_path = r"C:\astudy12\데이터분석\서울시 지하철 호선별 역별 시간대별 승하차 인원 정보.csv"
    
    try:
        # CSV 파일에서 데이터 가져오기
        print("CSV 파일에서 데이터를 읽는 중...")
        raw_data = get_subway_data(file_path)
        
        if raw_data is None:
            print("데이터를 가져오는데 실패했습니다.")
            return
        
        # 데이터 전처리
        print("\n데이터 전처리 중...")
        df = preprocess_data(raw_data)
        
        if df is None:
            print("데이터 전처리에 실패했습니다.")
            return
            
        # T-검정 수행
        print("\nT-검정 수행 중...")
        perform_ttest_analysis(df)
        
        print("\n분석이 완료되었습니다.")
        
    except Exception as e:
        print(f"Error: 분석 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()