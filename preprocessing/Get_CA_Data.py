#-*- coding:utf-8 -*-

import requests
import json
import time

#api密钥：AIzaSyCBJKDBn1bjnfdtQQip5SMK3j5uKeHK7mc
'''
1. Video ID
2. Trending date
3. Title
4. Channel title
5. Category ID
6. Publish time
7. Tags
8. Views
9. Likes
10. Dislikes
11. Comments count
12. Description
'''

class YoutubeCrawler():
    first_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&regionCode=CA&chart=mostPopular&key=AIzaSyCBJKDBn1bjnfdtQQip5SMK3j5uKeHK7mc&maxResults=50{}'
    video_list = []        #原始数据  200条
    video_data_list = []   #我想提取的出来的数据

    #获取视频数据列表
    def first_page(self): #def定义函数
        url = self.first_url.format('') #大括号里面需要拼接的东西 这里是空值  不写这个大括号保留
        response = requests.get(url) #获取http请求
        data = response.content.decode('utf-8') #resonse是实例  转换成编码格式
        response_dict = json.loads(data) #转换成字典形式  字符串是操作不了的
        #获取下一页url的pageToken参数
        pageToken = response_dict.get('nextPageToken') #文档规定只显示50条  需要找下一个就是找到不同页面的pagetoken
        # print('第一页' + pageToken)
        #提取video数据列表
        video_list = response_dict.get('items') #把items一个个抓下来
        self.video_list = video_list  #类变量   后面赋值给前面
        # print(video_list[0])
        # return video_list
        while (True):
            url = self.first_url.format('&pageToken=' + pageToken)
            # print(url)
            response = requests.get(url)
            data = response.content.decode('utf-8')
            response_dict = json.loads(data)
            pageToken = response_dict.get('nextPageToken')
            video_list = response_dict.get('items')
            self.video_list.extend(video_list)
            if pageToken == None:
                break
        # print(len(self.video_list))

    #提取数据
    def parse_data(self):
        # n = 0
        for video in self.video_list:
            video_data = {} #dict的数据格式
            video_data['video_id'] = video.get('id')
            video_data['trending_date'] = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.localtime(time.time()))
            video_data['title'] = video.get('snippet').get('title')
            video_data['channel_tittle'] = video.get('snippet').get('channelTitle')
            video_data['category_id'] = video.get('snippet').get('categoryId')
            video_data['publish_time'] = video.get('snippet').get('publishedAt')
            video_data['views'] = video.get('statistics').get('viewCount')
            video_data['likes'] = video.get('statistics').get('likeCount')
            video_data['dislikes'] = video.get('statistics').get('dislikeCount')
            video_data['comment_count'] = video.get('statistics').get('commentCount')
            video_data['description'] = video.get('snippet').get('description')
            video_data['tags'] = video.get('snippet').get('tags')
            self.video_data_list.append(video_data)

    def start(self): #调度函数
        self.first_page()
        self.parse_data()


if __name__ == '__main__':  #主函数
    YoutubeCrawler().start()
    json_data = json.dumps(YoutubeCrawler().video_data_list) #把字典转换成字符串
    #写入文件
    with open('CAvideos_New.json','w',encoding='utf-8') as f :
        f.write(json_data) #r是读取