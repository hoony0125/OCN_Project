import crawlFunc
import pandas as pd

# 분야별 뉴스 메인펭지 url
# 메인의 기사 영역
# 기사 리스트 헤더
# 기사 제목
# 기사 업로드 날짜
# 기사 내용 xpath


# 기존 엑셀 파일 읽기
csv = pd.read_csv('articles_in.csv', encoding='cp949')
# data_header = csv.column
datas = csv.values

check_titles = []
# check_titles.append(data_header[0])
for i in range(len(datas)):
    check_titles.append(datas[i][0])


# 기사 페이지 설정
business = ['https://edition.cnn.com/business', '/html/body/div[6]/section[1]/div[2]/div/div[1]/ul', 'cd__headline', '/html/body/div[5]/article/div[1]/h1', '/html/body/div[5]/article/div[1]/div[1]/div/p[3]', '/html/body/div[5]/article/div[1]/div[2]/div[1]/div[2]/section[1]/div[1]']
sport = ['https://edition.cnn.com/sport', '/html/body/div[3]/section[3]/section[1]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div', 'container__headline', '/html/body/div[6]/article/div[1]/h1', '/html/body/div[6]/article/div[1]/div[2]/div/p[3]', '/html/body/div[6]/article/div[1]/div[3]/div[1]/div[2]/section[1]/div[1]']
tech = ['https://edition.cnn.com/business/tech', '/html/body/div[6]/section[2]/div[6]/div/div[1]/ul', 'cd__headline', '/html/body/div[5]/article/div[1]/h1', '/html/body/div[5]/article/div[1]/div[1]/div/p[3]', '/html/body/div[5]/article/div[1]/div[2]/div[1]/div[2]/section[1]/div[1]']
health = ['https://edition.cnn.com/health', '/html/body/div[7]/section[1]/div[2]/div/div[2]', 'cd__headline', '/html/body/div[6]/article/div[1]/h1', '/html/body/div[6]/article/div[1]/div[1]/div/p[3]', '/html/body/div[6]/article/div[1]/div[2]/div[1]/div[2]/section[1]/div[1]']

articleInfoes = []
articleInfoes.append(business)
articleInfoes.append(tech)
articleInfoes.append(health)
articleInfoes.append(sport)

# 필터 생성
filter_check = []
for i in range(4):
    filter_check.append([])

# Null 확인
null_count = 0
# Pass 확인
pass_count = 0
# csv 파일 
csv_In = []

category = 0
for info in articleInfoes:
    csv_In, filter_check, null_count, check_titles, pass_count = crawlFunc.crawling(info, csv_In, filter_check, category, null_count, check_titles, pass_count)
    category = category + 1

# 필터 확인
print('\n\nresult')
num_y = len(filter_check)
for y in range(num_y):
    num_x = len(filter_check[y])
    for x in range(num_x):
        print('y : ' + str(y) + ' ' + filter_check[y][x])
print('null_count : ' + str(null_count))
print('pass_count : ' + str(pass_count))

# csv 출력
df = pd.DataFrame(csv_In, columns=['ATITLE', 'AUPLOAD', 'ACONTENT', 'AFILENAME', 'APRESSCOM', 'ACATEGORY'])
df.to_csv('articles.csv', mode='a', index=False, header=False)



