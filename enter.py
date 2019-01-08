from urllib import request
import globalStore
from bs4 import BeautifulSoup
import json
from twilio.rest import Client
import itchat



def init_config():
    with open('/Users/hualiao/PycharmProjects/CQUTInformer/config.json') as config:
        config_dict=json.load(config)
        globalStore._kw=config_dict['kw']
        globalStore._account_sid=config_dict['account_sid']
        globalStore._auth_token=config_dict['auth_token']
        globalStore._recieve_number=config_dict['recieve_number']
        globalStore._twilio_number=config_dict['twilio_number']


# 访问部门通知网


def visit_page():
    if len(globalStore._url) == 0:
        return False
    globalStore._data = request.urlopen(globalStore._url).read()
    globalStore._data = globalStore._data.decode('utf8')


# 解析页面


def analyse_page():
    soup = BeautifulSoup(globalStore._data, 'html.parser')
    ul = soup.find_all(id='tzlb')
    links = ul[0].find_all("div", class_='record')
    for row in links:
        title = row.a.get_text().strip()
        link = row.a['href']
        date = row.find_all('div', class_='dept_time')[0].get_text().strip().split('\r')[0][1:-1]

        # if globalStore._kw in title:
        #
        #     print('\033[32;0m >>>>>>>>>>title: %s, link: %s, date: %s<<<<<<<<<<\033[0m' % (title, globalStore._PREFIX + link, date))
        # else:
        globalStore._message_content=globalStore._message_content+('\n%s,%s' % (title, date))
        # print('title: %s, link: %s, date: %s' % (title, globalStore._PREFIX + link, date))
    # print(globalStore._message_content)
    # print(sys.getsizeof(globalStore._message_content))

# 通过短信通知


def smg_inform():
    client=Client(globalStore._account_sid, globalStore._auth_token)
    message=client.messages.create(
        to=globalStore._recieve_number,
        from_=globalStore._twilio_number,
        body=globalStore._message_content
    )
    print(message.sid)


def wechat_inform():
    itchat.auto_login(hotReload=True)
    itchat.send(globalStore._message_content, toUserName='filehelper')


def driver_func():
    try:
        init_config()
        visit_page()
        analyse_page()
        # wechat_inform()
        smg_inform()
        print('Message sent successfully!')
    except Exception:
        print('Exception occured, plz rerun!'+Exception)


if __name__ == '__main__':
    driver_func()
