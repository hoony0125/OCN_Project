from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time

driver = webdriver.Chrome()

# 기사 내용 합치기
def make_content(content, content_part, oper_flag):
    content_part = content_part.strip()                 # 양옆 공백 제거
    content_part = content_part.replace('\n','')        # 줄바꿈 제거
    content_part = content_part.replace('"', '^+^')     # 따옴표 치환
    if content_part == '':
        pass
    else:
        # 소제목
        if oper_flag == 0:
            content_part = '<br><br><h3>' + content_part + '</h3>'
            content = content + content_part
        # 일반 내용
        elif oper_flag == 1:
            content_part = '<br>' + content_part + '<br>'
            content = content + content_part
    return content

# 기사 제목 내용에서 쉼표 치환
def trans_comma(str):
    str = str.replace(',','^')
    return str

# 기사 상세 날짜 추출
date_list = ['November', 'December']
def get_date(str, date_list):
    for i in date_list:
        index = str.find(i)
        if index != -1:
            str = str[index:]
            return str
    return str


# 크롤링
def crawling(articleInfo, csv_In, filter_check, category, null_count, check_titles, pass_count):
    # 분야별 뉴스 메인페이지 url
    driver.get(articleInfo[0])
    time.sleep(2)

    # 메인의 기사 영역
    article_tab = driver.find_element_by_xpath(articleInfo[1])
    # 기사 리스트 헤더 - num
    article_num = len(article_tab.find_elements_by_class_name(articleInfo[2]))
    print( '기사 개수 : ' + str(article_num) )
    for index in range(article_num):
        # csv row
        csv_article = ['', '', '', '', 'CNN', category]
        print( '기사 번호 : ' + str(index))

        try:
            # 메인의 기사 영역
            article_tab = driver.find_element_by_xpath(articleInfo[1])
            # 기사 리스트 헤더
            article = article_tab.find_elements_by_class_name(articleInfo[2])[index]
        except NoSuchElementException:
            print('메인기사 list Null')
            null_count = null_count + 1
            # 분야별 뉴스 메인페이지 url
            driver.get(articleInfo[0])
            continue

        try:
            # click 에러 확인
            article.click()
            time.sleep(2)
        except ElementNotInteractableException:
            print('메인기사 list 클릭 Null')
            null_count = null_count + 1
            # 분야별 뉴스 메인페이지 url
            driver.get(articleInfo[0])
            continue

        try:
            # 기사 내용 xpath
            article_content = driver.find_element_by_xpath(articleInfo[5])
            # 기사 제목
            title = driver.find_element_by_xpath(articleInfo[3])
            print('title : ' + title.text)
            csv_article[0] = trans_comma(title.text)
            # 제목 비교
            loof_out = False
            for i in check_titles:
                if csv_article[0] == i:
                    loof_out = True
                    break
            if loof_out:
                print('중복 확인 PASS')
                pass_count = pass_count + 1
                # 분야별 뉴스 메인페이지 url
                driver.get(articleInfo[0])
                continue
            else:
                check_titles.append(csv_article[0])

        except NoSuchElementException:
            print('기사 상세 페이지 Null')
            null_count = null_count + 1
            # 분야별 뉴스 메인페이지 url
            driver.get(articleInfo[0])
            time.sleep(2)
            continue

        try:
            # 기사 업로드 시간
            upload = driver.find_element_by_xpath(articleInfo[4])
            date = get_date(upload.text, date_list)
            print('upload : ' + date)
            csv_article[1] = trans_comma(date)
        except NoSuchElementException:
            print('기사 업로드 Null')
            pass

        # 기사 내용에 포함된 모든 el__image--fullwidth : 이미지 추출
        img_list = article_content.find_elements_by_class_name('el__image--fullwidth')
        print( '이미지 개수 : ' + str(len(img_list)) )
        for img in img_list:
            in_img = img.find_element_by_tag_name("img")
            img_src = in_img.get_attribute("data-src")
            csv_article[3] = img_src
            print(img_src)

        # 필터링 변수
        filter_READ = 0
        filter_QUIZ = 0
        filter_EM = 0
        filter_READ_MORE = 0
        filter_Visit = 0
        # 기사 내용에 포함된 모든 zn-body__paragraph : 문단
        content_list = article_content.find_elements_by_class_name('zn-body__paragraph')
        num1 = len(content_list)
        # 기사 내용 끝 부분 zn-body__footer 파악/제거
        footer_list = article_content.find_elements_by_class_name('zn-body__footer')
        for remove in footer_list:
            content_list.pop()
        num2 = len(content_list)
        print('content_list : ' + str(num1) + ' - ' + str(len(footer_list)) + ' = ' + str(num2))

        # db 에 저장될 기사 내용
        db_content = ''
        # zn-body__paragraph 검사
        for content in content_list:
            # 소제목일 경우
            try:
                paragraph = content.find_element_by_tag_name("h3")
                # print('h3 : ' + content.text)
                db_content = make_content(db_content, content.text, 0)   # 소제목 input
            except NoSuchElementException:
                # 기사 상단의 em 확인
                try:
                    paragraph = content.find_element_by_tag_name('em')
                    # em 안의 Sign up, sign up, CNN, here 문구 포함 확인
                    if 'Sign up' in content.text or 'sign up' in content.text or 'CNN' in content.text or 'here' in content.text:
                        # print('em FIND ' + paragraph.text)
                        filter_EM = filter_EM + 1
                    else:
                        db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
                        # print(content.text)
                except NoSuchElementException:
                    # link 검사 / READ: / QUIZ / READ MORE / Visit CNN.com
                    try:
                        link = content.find_element_by_tag_name("a")
                        if 'READ:' in content.text:
                            # print('READ_FIND ' + content.text)
                            filter_READ = filter_READ + 1
                        elif 'QUIZ' in content.text:
                            # print('QUIZ_FIND ' + content.text)
                            filter_QUIZ = filter_QUIZ + 1
                        elif 'READ MORE:' in content.text:
                            # print('READ_MORE_FIND : ' + content.text)
                            filter_READ_MORE = filter_READ_MORE + 1
                        elif 'Visit CNN.com' in content.text:
                            # print('Visit_FIND : ' + content.text)
                            filter_Visit = filter_Visit + 1
                        else:
                            db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
                            # print(content.text)
                    # 일반 텍스트일 경우
                    except NoSuchElementException:
                        db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
                        # print(content.text)
            # print('\n')
        time.sleep(2)
        if filter_READ > 0 or filter_QUIZ > 0 or filter_EM > 0 or filter_READ_MORE > 0 or filter_Visit > 0:
            filter_string = '기사 : ' + str(index) + ' READ : ' + str(filter_READ) + ' QUIZ : ' + str(filter_QUIZ) + ' EM : '\
                            + str(filter_EM) + ' READ_MORE : ' + str(filter_READ_MORE) + ' Visit CNN : ' + str(filter_Visit)
            filter_check[category].append(filter_string)

        db_content = trans_comma(db_content)
        csv_article[2] = db_content
        print(db_content + '\n')
        csv_In.append(csv_article)

        # 분야별 메인 페이지
        driver.get(articleInfo[0])
        time.sleep(2)
    return csv_In, filter_check, null_count, check_titles, pass_count




# health
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# driver.get("https://edition.cnn.com/health")
# time.sleep(2)
#
# # 메인의 기사 영역 1
# try:
#     article_tab = driver.find_element_by_xpath(
#         '/html/body/div[7]/section[1]/div[2]/div/div[2]')
# except NoSuchElementException:
#     # 메인의 기사 영역 2
#     article_tab = driver.find_element_by_xpath(
#         '/html/body/div[8]/section[1]/div[2]/div/div[2]')
#
# # 기사 리스트 헤더 - num
# article_num = len(article_tab.find_elements_by_class_name('cd__headline'))
# print( '기사 개수 : ' + str(article_num) )
# for index in range(article_num):
#     # csv row
#     csv_article = [ '' , '', '' , 'CNN', 3]
#     print( '기사 번호 : ' + str(index))
#     # 메인기사 영역 1
#     try:
#         article_tab = driver.find_element_by_xpath(
#             '/html/body/div[7]/section[1]/div[2]/div/div[2]')
#     except NoSuchElementException:
#         # 메인의 기사 영역 2
#         article_tab = driver.find_element_by_xpath(
#             '/html/body/div[8]/section[1]/div[2]/div/div[2]')
#     # 기사 리스트 헤더
#     article = article_tab.find_elements_by_class_name('cd__headline')[index]
#     article.click()
#     time.sleep(2)
#
#     # 기사 형식 첫번쨰
#     try:
#         # 기사 제목
#         title = driver.find_element_by_xpath('/html/body/div[6]/article/div[1]/h1')
#         print('title 1 : ' + title.text)
#         csv_article[0] = trans_comma(title.text)
#         # 기사 내용 xpath 1
#         article_content = driver.find_element_by_xpath(
#             '/html/body/div[6]/article/div[1]/div[2]/div[1]/div[2]/section[1]/div[1]')
#     except NoSuchElementException:
#         # 기사 형식 두번째
#         try:
#             title = driver.find_element_by_xpath('/html/body/div[6]/article/div/div[2]/div[2]/h1')
#             print('title 2 : ' + title.text)
#             # 기사 내용 xpath 2
#             article_content = driver.find_element_by_xpath(
#                 '/html/body/div[6]/article/div/div[2]/div[2]/section[1]/div[1]')
#         except NoSuchElementException:
#             driver.get("https://edition.cnn.com/health")
#             print('NULL')
#             continue
#
#     # 기사 내용에 포함된 모든 el__image--fullwidth : 이미지
#     img_list = article_content.find_elements_by_class_name('el__image--fullwidth')
#     print( '이미지 개수 : ' + str(len(img_list)) )
#     for img in img_list:
#         in_img = img.find_element_by_tag_name("img")
#         img_src = in_img.get_attribute("data-src")
#         csv_article[2] = img_src
#         print(img_src)
#
#     # 필터링 변수
#     filter_READ = 0
#     filter_QUIZ = 0
#     filter_EM = 0
#     filter_READ_MORE = 0
#     filter_Visit = 0
#     # 기사 내용에 포함된 모든 zn-body__paragraph : 문단
#     content_list = article_content.find_elements_by_class_name('zn-body__paragraph')
#     num1 = len(content_list)
#     # 기사 내용 끝 부분 zn-body__footer 파악/제거
#     footer_list = article_content.find_elements_by_class_name('zn-body__footer')
#     for remove in footer_list:
#         content_list.pop()
#     num2 = len(content_list)
#     print('content_list : ' + str(num1) + ' - ' + str(len(footer_list)) + ' = ' + str(num2))
#
#     # db 에 저장될 기사 내용
#     db_content = ''
#     # zn-body__paragraph 검사
#     for content in content_list:
#         # 소제목일 경우
#         try:
#             paragraph = content.find_element_by_tag_name("h3")
#             # print('h3 : ' + content.text)
#             db_content = make_content(db_content, content.text, 0)   # 소제목 input
#         except NoSuchElementException:
#             # 기사 상단의 em 확인
#             try:
#                 paragraph = content.find_element_by_tag_name('em')
#                 # em 안의 Sign up, sign up, CNN, here 문구 포함 확인
#                 if 'Sign up' in content.text or 'sign up' in content.text or 'CNN' in content.text or 'here' in content.text:
#                     # print('em FIND ' + paragraph.text)
#                     filter_EM = filter_EM + 1
#                 else:
#                     db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
#                     # print(content.text)
#             except NoSuchElementException:
#                 # link 검사 / READ: / QUIZ / READ MORE / Visit CNN.com
#                 try:
#                     link = content.find_element_by_tag_name("a")
#                     if 'READ:' in content.text:
#                         # print('READ_FIND ' + content.text)
#                         filter_READ = filter_READ + 1
#                     elif 'QUIZ' in content.text:
#                         # print('QUIZ_FIND ' + content.text)
#                         filter_QUIZ = filter_QUIZ + 1
#                     elif 'READ MORE:' in content.text:
#                         # print('READ_MORE_FIND : ' + content.text)
#                         filter_READ_MORE = filter_READ_MORE + 1
#                     elif 'Visit CNN.com' in content.text:
#                         # print('Visit_FIND : ' + content.text)
#                         filter_Visit = filter_Visit + 1
#                     else:
#                         db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
#                         # print(content.text)
#                 # 일반 텍스트일 경우
#                 except NoSuchElementException:
#                     db_content = make_content(db_content, content.text, 1)  # 일반 기사 input
#                     # print(content.text)
#         # print('\n')
#     time.sleep(2)
#     if filter_READ > 0 or filter_QUIZ > 0 or filter_EM > 0 or filter_READ_MORE > 0 or filter_Visit > 0:
#         filter_string = '기사 : ' + str(index) + ' READ : ' + str(filter_READ) + ' QUIZ : ' + str(filter_QUIZ) + ' EM : '\
#                         + str(filter_EM) + ' READ_MORE : ' + str(filter_READ_MORE) + ' Visit CNN : ' + str(filter_Visit)
#         filter_check[3].append(filter_string)
#
#     db_content = trans_comma(db_content)
#     csv_article[1] = db_content
#     print(db_content + '\n')
#     csv_In.append(csv_article)
#
#     driver.get("https://edition.cnn.com/health")
#     time.sleep(2)
#
#