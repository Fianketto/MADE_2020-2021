import requests
import time
from bs4 import BeautifulSoup as bs


def get_csrf_token(session, login_url):
    response = session.get(login_url)
    html = response.content
    soup = bs(html)
    head = soup.head
    meta = head.findChildren('meta')
    csrf_token = [
        m for m in meta if 'name' in m.attrs and m['name'] == 'X-Csrf-Token']
    csrf_token = csrf_token[0]["content"]

    return csrf_token


def get_login_payload(csrf_token, login, password):
    return {
        'csrf_token': csrf_token,
        'action': 'enter',
        'ftaa': 'ynbjaoakq75zundkbu',  # dafuq is this
        'bfaa': '280a1c0c6b7a21c90c9c57eeb6edd278',  # dafuq is this
        'handleOrEmail': login,
        'password': password,
        '_tta': 255
    }


def main(login, password, base_url='http://codeforces.com', login_url='http://codeforces.com/enter'):
    contest_ids = [
        294554,
        295519,
        296563,
        297484,
        298483,
        299322,
        300637,
        301445,
        302662,
        303646,
        304481,
        305546,
        306534
    ]

    for i in range(11, len(contest_ids)):
        url_part_1 = "https://codeforces.com/group/zJTwakJcKM/contest/" + str(contest_ids[i]) + "/status/page/"
        url_part_2 = "?order=BY_ARRIVED_DESC"
        file_name = "temp_all_data_" + str(i + 1) + ".txt"
        fout = open(file_name, "w")
        with requests.Session() as session:
            page, page_count = 1, float('inf')
            while page <= page_count:
                print(f"contest {i+1}/{len(contest_ids)}, page {page}/{page_count}")
                url = url_part_1 + str(page) + url_part_2
                csrf_token = get_csrf_token(session, login_url)
                payload = get_login_payload(csrf_token, login, password)
                response = session.post(login_url, data=payload)

                p = session.get(url)
                page_content = p.content.decode('utf-8')

                soup = bs(page_content, 'html.parser')
                html_container = soup.find('html')
                body_container = html_container.find('body')
                div_container = body_container.find('div', id='body')
                div_container_2 = div_container.find_all('div', recursive=False)[4]
                div_container_3 = div_container_2.find('div', id="pageContent")
                div_container_4 = div_container_3.find('div', class_="datatable")
                div_container_5 = div_container_4.find_all('div', recursive=False)[5]
                table_container = div_container_5.find('table', class_="status-frame-datatable")
                tr_tags = table_container.find_all('tr', recursive=False)[1:]
                for tr_tag in tr_tags:
                    td_tags = tr_tag.find_all('td', recursive=False)
                    datetime_string = td_tags[1].find('span')
                    nickname = td_tags[2].find('a')
                    task_name = td_tags[3].find('a')
                    lang = td_tags[4]
                    verdict_container = td_tags[5].find('span')
                    verdict = verdict_container.find('span')
                    if not verdict:
                        verdict = verdict_container
                    time_consumed = td_tags[6]
                    memory_consumed = td_tags[7]

                    print(page, file=fout, end="\t")
                    print(datetime_string.text, file=fout, end="\t")
                    print(nickname.text, file=fout, end="\t")
                    print(task_name.text.strip(), file=fout, end="\t")
                    print(lang.text.strip(), file=fout, end="\t")
                    print(verdict.text, file=fout, end="\t")
                    print(time_consumed.text.strip(), file=fout, end="\t")
                    print(memory_consumed.text.strip(), file=fout)

                if page == 1:
                    div_container_3_1 = div_container_3.find_all('div', recursive=False)[7]
                    div_container_3_2 = div_container_3_1.find('div', class_='pagination')
                    ul_container = div_container_3_2.find('ul')
                    li_container = ul_container.find_all('li', recursive=False)
                    last_page = li_container[-2]
                    page_count = int(last_page.text)

                page += 1
                time.sleep(1)

        fout.close()


if __name__ == '__main__':
    my_login = 'login'
    my_pass = 'password'

    main(my_login, my_pass)