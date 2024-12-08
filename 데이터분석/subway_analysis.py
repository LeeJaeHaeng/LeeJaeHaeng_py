import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import requests
import time
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def get_subway_data(service_key):
    """Open API를 통해 지하철 시간대별 승하차 데이터 가져오기"""
    base_url = "http://openapi.seoul.go.kr:8088"
    all_data = []
    
    try:
        # 2023년 9월 p데이터 조회 (최신 데이터가 있는 날짜로 설정)
        date = "202309"
        
        # 데이터를 청크 단위로 가져오기
        start_index = 1
        end_index = 1000
        
        while True:
            # API 요청 URL 구성 - 시간대별 승하차인원 API 사용
            url = f"{base_url}/{service_key}/json/CardSubwayTime/{start_index}/{end_index}/{date}"
            print(f"\n{date} 데이터 조회 중... (인덱스: {start_index}-{end_index})")
            
            response = requests.get(url)
            print(f"응답 상태: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'CardSubwayTime' in data and 'row' in data['CardSubwayTime']:
                    rows = data['CardSubwayTime']['row']
                    total_count = data['CardSubwayTime'].get('list_total_count', 0)
                    print(f"데이터 건수: {len(rows)}")
                    all_data.extend(rows)
                    
                    if end_index >= total_count:
                        break
                        
                    start_index = end_index + 1
                    end_index = min(end_index + 1000, total_count)
                    
                elif 'RESULT' in data:
                    print(f"{date}: {data['RESULT'].get('MESSAGE', '')}")
                    break
            else:
                break
            
            time.sleep(0.5)  # API 호출 간격 조절
        
        if all_data:
            return pd.DataFrame(all_data)
        else:
            print("\n조회 가능한 데이터를 찾지 못했습니다.")
            return None
        
    except Exception as e:
        print(f"데이터 조회 중 오류 발생: {e}")
        return None

def preprocess_data(df):
    """데이터 전처리"""
    try:
        if df is None:
            return None
            
        print("\n=== 원본 데이터 컬럼 ===")
        print(df.columns.tolist())
        
        # 시간대별 데이터를 행으로 변환
        df_melted = pd.melt(df, 
                          id_vars=['USE_MM', 'SBWY_ROUT_LN_NM', 'STTN'],
                          value_vars=[col for col in df.columns if 'GET_' in col],
                          var_name='TIME_TYPE',
                          value_name='PASSENGER_NUM')
        
        # 시간 추출 (HR_4_GET_ON_NOPE -> 4시)
        df_melted['TIME'] = df_melted['TIME_TYPE'].str.extract(r'HR_(\d+)_').astype(str) + '시'
        
        # 승하차 구분
        df_melted['TYPE'] = df_melted['TIME_TYPE'].apply(lambda x: '승차인원' if 'GET_ON' in x else '하차인원')
        
        # 피봇 테이블로 변환
        df_processed = df_melted.pivot_table(
            index=['SBWY_ROUT_LN_NM', 'STTN', 'TIME'],
            columns='TYPE',
            values='PASSENGER_NUM',
            aggfunc='first'
        ).reset_index()
        
        # 컬럼명 한글로 변경
        df_processed = df_processed.rename(columns={
            'SBWY_ROUT_LN_NM': '호선',
            'STTN': '역명',
            'TIME': '시간'
        })
        
        # 숫자형 데이터 변환
        df_processed['승차인원'] = pd.to_numeric(df_processed['승차인원'], errors='coerce')
        df_processed['하차인원'] = pd.to_numeric(df_processed['하차인원'], errors='coerce')
        
        # 결측치 처리
        df_processed = df_processed.fillna(0)
        
        # 총 이용객 계산
        df_processed['총이용객'] = df_processed['승차인원'] + df_processed['하차인원']

        # 서울 지하철 1~9호선만 필터링
        seoul_lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선']
        df_processed = df_processed[df_processed['호선'].isin(seoul_lines)]
        
        print("\n=== 전처리 후 데이터 샘플 ===")
        print(df_processed.head())
        
        return df_processed
        
    except Exception as e:
        print(f"데이터 전처리 중 오류 발생: {e}")
        return None

def analyze_top_stations(df):
    """호선별 상위 10개 역 분석"""
    try:
        # 호선별 역별 총 이용객 계산
        station_stats = df.groupby(['호선', '역명']).agg({
            '승차인원': 'sum',
            '하차인원': 'sum',
            '총이용객': 'sum'
        }).reset_index()
        
        # 호선별로 상위 10개 역 선택
        top_stations_by_line = {}
        for line in station_stats['호선'].unique():
            line_data = station_stats[station_stats['호선'] == line]
            top_10 = line_data.nlargest(10, '총이용객')['역명'].tolist()
            top_stations_by_line[line] = top_10
        
        return top_stations_by_line
        
    except Exception as e:
        print(f"상위 역 분석 중 오류 발생: {e}")
        return None

def create_visualizations(df, top_stations_by_line):
    """시각화 생성"""
    print("\n시각화 생성 중...")
    
    # 서울 지하철 1~9호선만 처리
    seoul_lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선']
    
    # 시간 순서 정의
    time_order = [f"{i}시" for i in range(24)]
    
    for line in seoul_lines:
        if line not in top_stations_by_line:
            continue
            
        top_stations = top_stations_by_line[line]
        line_data = df[df['호선'] == line]
        
        if line_data.empty or not top_stations:
            continue
            
        # 라인 그래프
        plt.figure(figsize=(15, 10))
        
        # 승차 인원 그래프
        plt.subplot(2, 1, 1)
        for station in top_stations:
            station_data = line_data[line_data['역명'] == station].copy()
            station_data['시간순'] = pd.Categorical(station_data['시간'], categories=time_order, ordered=True)
            station_data = station_data.sort_values('시간순')
            plt.plot(station_data['시간'], station_data['승차인원'], label=station, marker='o')
        
        plt.title(f'{line} 상위 10개 역의 시간대별 승차 인원')
        plt.xlabel('시간')
        plt.ylabel('승차 인원')
        plt.xticks(time_order, rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        
        # 하차 인원 그래프
        plt.subplot(2, 1, 2)
        for station in top_stations:
            station_data = line_data[line_data['역명'] == station].copy()
            station_data['시간순'] = pd.Categorical(station_data['시간'], categories=time_order, ordered=True)
            station_data = station_data.sort_values('시간순')
            plt.plot(station_data['시간'], station_data['하차인원'], label=station, marker='o')
        
        plt.title(f'{line} 상위 10개 역의 시간대별 하차 인원')
        plt.xlabel('시간')
        plt.ylabel('하차 인원')
        plt.xticks(time_order, rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'subway_time_stats_{line}.png', bbox_inches='tight')
        plt.close()
        
        # 히트맵 생성
        plt.figure(figsize=(15, 12))
        
        # 승차 히트맵
        plt.subplot(2, 1, 1)
        heatmap_data_on = []
        for station in top_stations:
            station_data = line_data[line_data['역명'] == station].copy()
            station_data['시간순'] = pd.Categorical(station_data['시간'], categories=time_order, ordered=True)
            station_data = station_data.sort_values('시간순')
            heatmap_data_on.append(station_data['승차인원'].values)
        
        sns.heatmap(heatmap_data_on, 
                   xticklabels=time_order,
                   yticklabels=top_stations,
                   cmap='YlOrRd',
                   fmt='.0f',
                   cbar_kws={'label': '승차 인원'})
        
        plt.title(f'{line} 상위 10개 역의 시간대별 승차 인원 히트맵')
        plt.xlabel('시간')
        plt.ylabel('역명')
        
        # 하차 히트맵
        plt.subplot(2, 1, 2)
        heatmap_data_off = []
        for station in top_stations:
            station_data = line_data[line_data['역명'] == station].copy()
            station_data['시간순'] = pd.Categorical(station_data['시간'], categories=time_order, ordered=True)
            station_data = station_data.sort_values('시간순')
            heatmap_data_off.append(station_data['하차인원'].values)
        
        sns.heatmap(heatmap_data_off,
                   xticklabels=time_order,
                   yticklabels=top_stations,
                   cmap='YlOrRd',
                   fmt='.0f',
                   cbar_kws={'label': '하차 인원'})
        
        plt.title(f'{line} 상위 10개 역의 시간대별 하차 인원 히트맵')
        plt.xlabel('시간')
        plt.ylabel('역명')
        
        plt.tight_layout()
        plt.savefig(f'subway_time_heatmap_{line}.png', bbox_inches='tight')
        plt.close()
        
        print(f'\n{line} 시간대별 시각화 파일이 생성되었습니다: subway_time_stats_{line}.png')
        print(f'\n{line} 시간대별 히트맵 파일이 생성되었습니다: subway_time_heatmap_{line}.png')
        
        print(f'\n{line} 상위 10개 역:')
        for i, station in enumerate(top_stations, 1):
            print(f'{i}. {station}')

def perform_hypothesis_testing(df):
    """시간대별 승하차 인원에 대한 가설검정 수행"""
    print("\n=== 가설검정 결과 (신뢰수준: 2시그마/95.45%) ===")
    
    try:
        # 피크시간대 정의
        morning_peak_hours = [str(i) + '시' for i in range(7, 10)]  # 오전 7-9시
        evening_peak_hours = [str(i) + '시' for i in range(17, 20)]  # 오후 5-7시
        peak_hours = morning_peak_hours + evening_peak_hours
        
        # 피크시간대와 비피크시간대 데이터 분리
        peak_data = df[df['시간'].isin(peak_hours)]
        non_peak_data = df[~df['시간'].isin(peak_hours)]
        
        # 2시그마 신뢰수준을 위한 z값 (95.45%)
        z_critical = 2.0
        
        # 1. 피크시간대와 비피크시간대 승차인원 비교
        print("\n1. 피크시간대 vs 비피크시간대 승차인원 분석")
        peak_mean = peak_data['승차인원'].mean()
        non_peak_mean = non_peak_data['승차인원'].mean()
        
        # 표준오차 계산
        peak_std = peak_data['승차인원'].std()
        non_peak_std = non_peak_data['승차인원'].std()
        peak_n = len(peak_data)
        non_peak_n = len(non_peak_data)
        
        pooled_std = np.sqrt((peak_std**2/peak_n + non_peak_std**2/non_peak_n))
        margin_of_error = z_critical * pooled_std
        
        print(f"피크시간대 평균 승차인원: {peak_mean:.2f}")
        print(f"비피크시간대 평균 승차인원: {non_peak_mean:.2f}")
        print(f"차이의 95.45% 신뢰구간: [{abs(peak_mean - non_peak_mean) - margin_of_error:.2f}, "
              f"{abs(peak_mean - non_peak_mean) + margin_of_error:.2f}]")
        
        # 2. 호선별 평균 이용객수 분석
        print("\n2. 호선별 평균 이용객수 분석")
        line_stats = df.groupby('호선')['총이용객'].agg(['mean', 'std', 'count']).reset_index()
        
        for _, row in line_stats.iterrows():
            mean = row['mean']
            std = row['std']
            n = row['count']
            se = std / np.sqrt(n)
            ci = z_critical * se
            print(f"\n{row['호선']}:")
            print(f"평균 이용객: {mean:.2f}")
            print(f"95.45% 신뢰구간: [{mean - ci:.2f}, {mean + ci:.2f}]")
        
        # 3. 시간대별 승하차 비율 분석
        print("\n3. 시간대별 승하차 비율 분석")
        df['승하차비율'] = df['승차인원'] / df['하차인원']
        time_stats = df.groupby('시간')['승하차비율'].agg(['mean', 'std', 'count']).reset_index()
        
        for _, row in time_stats.iterrows():
            if not np.isnan(row['mean']) and not np.isnan(row['std']):
                mean = row['mean']
                std = row['std']
                n = row['count']
                se = std / np.sqrt(n)
                ci = z_critical * se
                print(f"\n{row['시간']}:")
                print(f"평균 승하차비율: {mean:.2f}")
                print(f"95.45% 신뢰구간: [{mean - ci:.2f}, {mean + ci:.2f}]")
        
        return True
        
    except Exception as e:
        print(f"가설검정 중 오류 발생: {e}")
        return False

def main():
    # API 키 설정
    service_key = "7a4b584f5a6c6565373672684c4a67"
    
    try:
        # 데이터 조회
        print("Open API에서 데이터를 조회하는 중...")
        raw_data = get_subway_data(service_key)
        
        if raw_data is None:
            print("데이터를 가져오는데 실패했습니다.")
            return
            
        # 데이터 전처리
        print("\n데이터 전처리 중...")
        df = preprocess_data(raw_data)
        
        if df is None:
            print("데이터 전처리에 실패했습니다.")
            return
            
        # 호선별 상위 10개 역 분석
        print("\n호선별 상위 10개 역 분석 중...")
        top_stations_by_line = analyze_top_stations(df)
        
        if top_stations_by_line is None:
            print("상위 역 분석에 실패했습니다.")
            return
            
        # 가설검정 수행
        print("\n가설검정 수행 중...")
        perform_hypothesis_testing(df)
            
        # 시각화 생성
        print("\n시각화 생성 중...")
        create_visualizations(df, top_stations_by_line)
        
        print("\n분석이 완료되었습니다.")
        
    except Exception as e:
        print(f"Error: 분석 중 오류가 발생했습니다: {str(e)}")

def perform_hypothesis_testing(df):
    """시간대별 승하차 인원에 대한 가설검정 수행"""
    print("\n=== 가설검정 결과 ===")
    
    try:
        from scipy import stats
        
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
        print(f"승차 인원 p-value: {p_value_on:.4e}")
        print(f"피크시간대 평균 승차인원: {peak_data['승차인원'].mean():.2f}")
        print(f"비피크시간대 평균 승차인원: {non_peak_data['승차인원'].mean():.2f}")
        
        # 2. 하차 인원에 대한 t-test
        print("\n2. 하차 인원 분석 (피크시간대 vs 비피크시간대)")
        t_stat_off, p_value_off = stats.ttest_ind(peak_data['하차인원'], 
                                                 non_peak_data['하차인원'])
        
        print(f"하차 인원 t-통계량: {t_stat_off:.4f}")
        print(f"하차 인원 p-value: {p_value_off:.4e}")
        print(f"피크시간대 평균 하차인원: {peak_data['하차인원'].mean():.2f}")
        print(f"비피크시간대 평균 하차인원: {non_peak_data['하차인원'].mean():.2f}")
        
        # 3. 총 이용객에 대한 t-test
        print("\n3. 총 이용객 분석 (피크시간대 vs 비피크시간대)")
        t_stat_total, p_value_total = stats.ttest_ind(peak_data['총이용객'], 
                                                     non_peak_data['총이용객'])
        
        print(f"총 이용객 t-통계량: {t_stat_total:.4f}")
        print(f"총 이용객 p-value: {p_value_total:.4e}")
        print(f"피크시간대 평균 총이용객: {peak_data['총이용객'].mean():.2f}")
        print(f"비피크시간대 평균 총이용객: {non_peak_data['총이용객'].mean():.2f}")
        
        # 가설검정 결과 해석
        alpha = 0.05
        print("\n=== 가설검정 결과 해석 ===")
        for test_type, p_value in [("승차 인원", p_value_on), 
                                 ("하차 인원", p_value_off), 
                                 ("총 이용객", p_value_total)]:
            if p_value < alpha:
                print(f"\n{test_type}: 귀무가설 기각 (p < {alpha})")
                print(f"결론: {test_type}은 출퇴근 시간대와 통계적으로 유의미한 관계가 있음")
            else:
                print(f"\n{test_type}: 귀무가설 채택 (p >= {alpha})")
                print(f"결론: {test_type}은 출퇴근 시간대와 통계적으로 유의미한 관계가 없음")
        
        return True
        
    except Exception as e:
        print(f"가설검정 중 오류 발생: {e}")
        return False
if __name__ == "__main__":
    main()

    