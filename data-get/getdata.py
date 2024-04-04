import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
import html2text

web_root = "https://zh.ifixit.com"
visited_urls = set()


#请求主页面
def get_main_web():
    
    url = "https://zh.ifixit.com/Device/PC_Laptop"
    response = requests.get(url)
    html_content = response.text

    #获取网页超链接
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', class_='categoryAnchor')

    #wiki为简要故障的描述，brand为分品牌的购买
    global wikis_href
    global brand_href

    #填充wiki、brand
    for link in links :
        str_tag_a = link.get('href')
        head_judge = str_tag_a.split('/')
        if head_judge[1] == "Device":
            brand_href.append("https://zh.ifixit.com" + str_tag_a)
            brand_name.append(head_judge[2])
        else:
            wikis_href.append("https://zh.ifixit.com" + str_tag_a)
            wikis_name.append(head_judge[2])

#请求单页面重试
async def request_for_web(href,retries = 3):
    url = web_root + href
    retry_count = 0
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    result =  await response.text()
                    if result is not None:
                        return result
        except Exception as e :
            print(f"Attempt {attempt + 1} failed:", e)
            await asyncio.sleep(1)

    print("All attempts failed")
    return None

#控制对于某个页面的生成方式
async def handle_web_genre(href):
    if href in visited_urls:
        return
    visited_urls.add(href)
    genre_judge = href.split('/')[1]
    web_title = href.split('/')[2]
    if genre_judge == "Device":
        await handle_Device(href,web_title)
    elif genre_judge == "Wiki":
        await handle_Wiki(href,web_title)
    elif genre_judge == "Guide":
        await handle_Guide(href,web_title)

#辅助函数
async def process_link(it):
    href_str = str(it.get('href'))
    if href_str is not None:
        length_str = len(href_str.split('/'))
        if length_str > 2:
            genre_judge = href_str.split('/')[1]
            if (genre_judge == "Device" or genre_judge == "Wiki" or genre_judge == "Guide"):
                await handle_web_genre(href_str)
#对于Device页面的分发，类似DFS
async def handle_Device(href,web_title):
    if web_title == "Edit": 
        return
    print(f"""
    we are doing on web : {href},naming {web_title} , Printing Device
    """)
    html_content = await request_for_web(href)
    if html_content is None:
        return
    soup = BeautifulSoup(html_content,'html.parser')
    
    main = soup.find(id="topContent")
    link_list = []
    try:
        link_list = main.find_all('a')
    except:
        print("main is empty"+'\n')
    tasks = [process_link(it) for it in link_list]
    await asyncio.gather(*tasks)


#对于Guide页面的生成
async def handle_Guide(href,web_title):
    print(f"""
    we are doing on web : {href},naming {web_title}, printing Guide
    """)
    html_content = await request_for_web(href)
    if html_content is None:
        return
    soup = BeautifulSoup(html_content,'html.parser')

    # 删除图像，作者栏，团队栏，评论栏，保留纯文本
    for tag in soup.find_all(lambda tag: tag.get('id') == 'embedBox' or tag.name == 'img' or tag.name == 'iframe' or tag.get('class') and any(className in tag['class'] for className in ['author-container','guide-comments-container','guide-complete','translation-credit-container','js-comment-container','completion-container','js-embed-text'])):
        tag.extract()

    # 去除超链接
    for a_tag in soup.find_all('a'):
        new_tag = soup.new_tag('span')
        if a_tag.string is not None:
            new_tag.string = a_tag.string
        a_tag.replace_with(new_tag)

    main_content = soup.find_all(id='contentFloat')

    #输出到文件
    with open(f'Guide/{web_title}.md','w',encoding='utf-8') as file:
        for it in main_content:
            file.write(html2text.html2text(it.prettify()))

#对于wiki页面的生成
async def handle_Wiki(wiki_href,wiki_name):
    print(f"""
    we are doing on web : {wiki_href},naming {wiki_name} , printing Wiki
    """)
    html_content = await request_for_web(wiki_href)
    if html_content is None:
        return

    soup = BeautifulSoup(html_content,'html.parser')
    

    # 删除图像，作者栏，团队栏，评论栏，保留纯文本
    for tag in soup.find_all(lambda tag: tag.name == 'img' or tag.get('class') and any(className in tag['class'] for className in ['author-container', 'team-container','comments'])):
        tag.extract()
    
    # 去除超链接
    for a_tag in soup.find_all('a'):
        new_tag = soup.new_tag('span')
        if a_tag.string is not None:
            new_tag.string = a_tag.string
        a_tag.replace_with(new_tag)
    
    main_content = soup.find_all(id='main')

    #输出到文件
    with open(f'Wiki/{wiki_name}.md','w',encoding='utf-8') as file:
        for it in main_content:
            file.write(html2text.html2text(it.prettify()))

async def main():
    # tasks = [process_link(it) for it in link_list]
    # await asyncio.gather(*tasks)
    link_list = [
        # '/Device/Acer_Laptop',
        # '/Device/Asus_Laptop',
        # '/Device/HP_Laptop',
        # '/Device/Samsung_Laptop',
        # '/Device/Microsoft_Laptop',
        # '/Device/Huawei_Laptop',
        # '/Device/Mac',
        # '/Device/Tablet',
        # '/Device/Asus_Desktop',
        # '/Device/Acer_Desktop',
        # '/Device/Dell_Desktop',
        # '/Device/Game_Console',
        # Camera device
        # '/Device/Camera',
        '/Device/Android_Phone',
        '/Device/iPhone',
    ]
    tasks = [handle_web_genre(it) for it in link_list]
    await asyncio.gather(*tasks)
    print("All tasks completed")


if __name__ == '__main__':
    asyncio.run(main())
