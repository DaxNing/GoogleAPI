#!/user/bin/python
# _*_ coding: UTF-8 _*_

import grequests
import logging
from googletrans import Translator
from googletrans.utils import format_json
import io
import time
import random

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
translator = Translator(service_urls=['translate.google.cn'])#调用网站

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename='log.txt')
logger = logging.getLogger()


def exception_handler(request, exception):
    logger.warning('exception when at %s :%s',request.url,exception)


def work(urls):
    reqs = (grequests.get(u,verify=True, allow_redirects=True, timeout=4) for u in urls)#requests向某个url批量发起POST请求
    res = grequests.map(reqs, exception_handler=exception_handler,size=20)#查看返回值的属性值
    return res

def totaltranslate():
    #批量翻译文章

    start=1#需要翻译的起始文章编号
    end=100#需要翻译的末尾文章编号

    for i in range(start,end):
        print(i)
        file2 = io.open('C:/Users/86135/Desktop/id_work/final_data/id_article_translate/id_article_'+str(i)+'.json',mode='a',encoding='utf-8')#追加在文件末尾
        with io.open('C:/Users/86135/Desktop/id_work/final_data/id_article_content/id_article_content_'+str(i)+'.json',mode='r',encoding='utf-8') as f:
            urls = []
            for line in f:

                line = line.strip()#去掉句子开头结尾的符号
                token = translator.token_acquirer.do(line)
                url="https://translate.google.cn/translate_a/single?client=t&sl=id&tl=zh-cn&hl=zh-cn&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=3&tsel=0&kc=1&tk={0}&q={1}".format(token,line)#生成URL
                urls.append(url)

                if len(urls) >= 0:
                    res = work(urls)
                    print(res)
                    for r in res:
                        if hasattr(r,'status_code'):
                            if r.status_code == 200:#网络请求成功
                                try:
                                    a=format_json(r.text)
                                    target = ''.join([d[0] if d[0] else '' for d in a[0]])
                                    print(target)
                                    source = ''.join([d[1] if d[1] else '' for d in a[0]])
                                except Exception as e:
                                    logger.error('when format:%s',e)
                                    logger.error('%s\n%s',r.text)
                                    source = ''
                                    target = ''
                                if len(source) != 0 and len(target) != 0:
                                    file2.write(target+'\n')
                                else:
                                    file2.write('\n')
                            elif r.status_code == 403:
                                line.replace(" #|\\|\"|& ","")
                                list = line.split(",")
                                result=[]
                                for l in range(len(list)):
                                    urls=[] #置空
                                    line = list[l].strip()  # 去掉句子开头结尾的符号
                                    token = translator.token_acquirer.do(line)
                                    url = "https://translate.google.cn/translate_a/single?client=t&sl=id&tl=zh-cn&hl=zh-cn&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=3&tsel=0&kc=1&tk={0}&q={1}".format(token, line)  # 生成URL
                                    urls.append(url)

                                    if len(urls) >= 0:
                                        res = work(urls)
                                        print(res)
                                        for r in res:
                                            if hasattr(r, 'status_code'): #判断r是否存在status_code属性
                                                if r.status_code == 200:  # 网络请求成功
                                                    try:
                                                        a = format_json(r.text)
                                                        target = ''.join([d[0] if d[0] else '' for d in a[0]])
                                                        print(target)
                                                        source = ''.join([d[1] if d[1] else '' for d in a[0]])
                                                    except Exception as e:
                                                        logger.error('when format:%s', e)
                                                        logger.error('%s\n%s', r.text)
                                                        source = ''
                                                        target = ''
                                                    if len(source) != 0 and len(target) != 0:
                                                        result.append(target)
                                                    else:
                                                        result.append(" ")
                                file2.write(",".join(result)+"\n")
                            else:
                                file2.write("\n")
                            time.sleep(random.randint(1, 3)) #设置睡眠时长，防止被封

                    urls = []
                    logger.info('finished articles: %s',i)
                    time.sleep(random.randint(1, 3))
        file2.close()

if __name__ == "__main__":
    totaltranslate()
