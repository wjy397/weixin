# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from wechat_sdk.exceptions import WechatAPIException
from wechat_sdk.utils import convert_ext_to_mime,is_allowed_extension
#配置服务器报错打印日志到文件
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/root/wechat_huoyun/logs/exception.log',
                filemode='w')

# #将access_token存储在session中，用于conf初始化参数调用。
# _session_access_token =  request.session.get('access_token',default=None)
# _session_token_expires_at= request.session.get('expires_at',default=None)
#服务器运行执行一次conf初始化，此页面路由功能触发方法不会触发conf初始化
from wechat_sdk import WechatConf
conf = WechatConf(
    token='ebaquan',
    appid='wxd3ec5c736ffdd7c5',#'wx118e7112b523d38c',
    appsecret='498c18cb3f70de1b329980d667b8142d',#1c3333999c59cc873ea8d737c74ed85b
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='TRROyP9RVUSIpeqa8VRHaAt4l9STZKvA6fZZE2N9dmc'  # 如果传入此值则必须保证同时传入 token, appid
    # access_token=_session_access_token,
    # access_token_expires_at=_session_token_expires_at
)
#第一次发送请求设置access_token
conf.access_token
from wechat_sdk import WechatBasic
wechat = WechatBasic(conf=conf)

@csrf_exempt
def WeChat(request):
    # return HttpResponse('teststsuccessful_test')
    try:
        if request.method == 'GET':
            #下面这四个参数是在接入时，微信的服务器发送过来的参数
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)

            #这个token是我们自己来定义的，并且这个要填写在开发文档中的Token的位置
            token = 'ebaquan'

            #把token，timestamp, nonce放在一个序列中，并且按字符排序
            hashlist = [token, timestamp, nonce]
            hashlist.sort()

            #将上面的序列合成一个字符串
            hashstr = ''.join([s for s in hashlist])

            #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
            hashstr = hashlib.sha1(hashstr).hexdigest()

            #把我们生成的字符串和微信服务器发送过来的字符串比较，
            #如果相同，就把服务器发过来的echostr字符串返回去
            if hashstr == signature:
              return HttpResponse(echostr)
        if request.method == 'POST':
            str_xml = request.body
            wechat.parse_data(str_xml)
            # return HttpResponse(str_xml)
            from wechat_sdk.messages import EventMessage,TextMessage,LocationMessage
            if isinstance(wechat.message, EventMessage):
                #自定义菜单click
                if wechat.message.type == 'click' and wechat.message.key == 'V1001_TODAY_JIAOLIU':
                    return HttpResponse(wechat.response_text('这是测试回复！！', escape=False))
                #用户订阅自动回复
                elif wechat.message.type=='subscribe':
                    return HttpResponse(wechat.response_text('欢迎关注！本平台提供专业的美国恶霸犬知识，第一手的资讯，是犬友交流交易的可靠平台，平台陆续会推出各种功能满足犬友的需求，欢迎提供宝贵意见！\n回复：“交流” 进入社区。', escape=False))
                #用户上报地理位置
                elif wechat.message.type=='location':
                    return HttpResponse(wechat.response_text('纬度:'+str(wechat.message.latitude)+'\n经度:'+str(wechat.message.longitude), escape=False))
            elif isinstance(wechat.message, TextMessage):
                #自动回复用户信息
                 if wechat.message.content ==u'交流':
                    return HttpResponse(wechat.response_text('<a href ="http://yunzhijia.com/36FkG">点我进入社区</a>', escape=False))
                 elif wechat.message.content ==u'图片':
                    return HttpResponse(wechat.response_image('7-LSg0N_iFq-s6atji5NWe_i_0ED4_Wioi1vVNUQ1xBoXaVUA0SZGVKM45A09Bpk'))
                 #回复图文消息点击进入永久性素材url
                 elif wechat.message.content ==u'图文':
                    articles=[{'title': u'第一条新闻标题', 'description': u'第一条新闻描述','picurl':u'http://mmbiz.qpic.cn/mmbiz/eqhuUWTCEa1dicEqx71qSDPCMep3U3UoONaqQRmCNGPEfsgFcvj62icnZoYPDZBh21EicnIDbUwQFJM6p4aicnvBJg/0?wx_fmt=jpeg', 'url': u'http://mp.weixin.qq.com/s?__biz=MzI1MTI5MzY1OQ==&mid=100000006&idx=1&sn=6091886e5fbc9a0e24dd427910723ba7#rd',}]
                    return HttpResponse(wechat.response_news(articles))
                 else:
                    return HttpResponse(wechat.response_text('平台正在紧张努力的建设中.....\n欢迎回复建议信息,\n我们会及时更新！', escape=False))
    except WechatAPIException, e:
             logging.exception(e)
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)
    except Exception,e :
               logging.exception(e)

#新增自定义菜单
def create_menu(request):
        try:
            wechat.create_menu({'button':[
                     {
                    'type': 'click',
                    'name': '交流社区',
                    'key': 'V1001_TODAY_JIAOLIU'
                }
                ,{
                    'type': 'view',
                    'name': '用户授权',
                    'url':'http://115.28.148.225/login'
                }
            ]
            })
            return  HttpResponse('create a menu success!')
        except WechatAPIException, e:
             # logging.exception(e)
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#添加临时素材
def add_MT(request):
        try:
            f = open('E://keng.jpg', 'rb')
            json =  wechat.upload_media('image',f )
            f.close()
            return  HttpResponse('add a temporary material success!<br/>media_id:'+str(json['media_id'])+'<br/>created_at:'+str(json['created_at'])+'<br/>type:'+str(json['type']))
        except WechatAPIException, e:
             # logging.exception(e)
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

# 获取临时素材
def get_MT(request):
        try:
            response = wechat.download_media('7-LSg0N_iFq-s6atji5NWe_i_0ED4_Wioi1vVNUQ1xBoXaVUA0SZGVKM45A09Bpk')
            #11.jpg可以是不存在的文件，但是后缀必须要和media_id对应的服务器资源后缀一样，也就是资源类型一样，否则的话如果是11.txt那么从服务器下载的图片资源会写入txt里乱码
            with open('E://11.jpg', 'wb') as fd:
                for chunk in response.iter_content(1024):
                    fd.write(chunk)
            return  HttpResponse('get a temporary material success!')
        except WechatAPIException, e:
             # logging.exception(e)
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#上传永久图片素材插图img返回URL
def addper_imgurl(request):
            try:
                media_file = open('E://eb.jpg', 'rb')
                extension=''
                if isinstance(media_file, file):
                    extension = media_file.name.split('.')[-1].lower()
                    if not is_allowed_extension(extension):
                        raise ValueError('Invalid file type.')
                    filename = media_file.name
                else:
                    extension = extension.lower()
                    filename = 'temp.' + extension

                uplodimg_json = wechat.request.post(
                    url='https://api.weixin.qq.com/cgi-bin/media/uploadimg',
                    files={
                        'media': (filename, media_file, convert_ext_to_mime(extension))
                    }
                  )
                media_file.close()
                return str(uplodimg_json['url'])
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#新增其他类型永久素材
def addper_otherMT(request):
            try:
                media_file = open('E://ee.jpg', 'rb')
                extension=''
                if isinstance(media_file, file):
                    extension = media_file.name.split('.')[-1].lower()
                    if not is_allowed_extension(extension):
                        raise ValueError('Invalid file type.')
                    filename = media_file.name
                else:
                    extension = extension.lower()
                    filename = 'temp.' + extension

                uplodimg_json = wechat.request.post(
            url='https://api.weixin.qq.com/cgi-bin/material/add_material',
            params={
                'type': 'image',
            },
            files={
                'media': (filename, media_file, convert_ext_to_mime(extension))
            }
        )
                media_file.close()
                return str(uplodimg_json['media_id'])
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)



# 新增永久图文素材
def addper_MT(request):
        try:
             #上传永久性图片资源
             image_media_url=addper_imgurl(request)
             thumb_meid = addper_otherMT(request)
             # WechatConf._check_appid_appsecret()
             news=[]
             news_data = [{'title':u'test（恶霸犬交易社区）等你很久了！'
                              ,'thumb_media_id':thumb_meid
                              ,'author':'wjy'
                              ,'digest':u'图文消息的摘要'
                              ,'show_cover_pic':1
                              ,'content':'contentcontentcontentcontentcontent<br/>contentcontent<br/><img src='+image_media_url+' />contentcontentcontentcontentcontent'
                              ,'content_source_url': 'http://www.baidu.com'
                           }]
             for new in news:
                 news_data.append({
                     'title': new['title'],
                     'thumb_media_id': new['thumb_media_id'],
                     'author': new.get('author', ''),
                    'digest': new.get('digest', ''),
                     'show_cover_pic': new.get('show_cover_pic', 0),
                    'content': new['content'],
                    'content_source_url': new.get('content_source_url', '')
               })
             json =  wechat.request.post(
                 url='https://api.weixin.qq.com/cgi-bin/material/add_news',
                 data={
                     'articles': news_data
                 }
             )
             return  HttpResponse('add a persistance material success!<br/>media_id:'+str(json['media_id']))
        except WechatAPIException, e:
              # logging.exception(e)
              return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#获取永久素材
def getper_MT(request):
            try:
                uplodimg_json = wechat.request.post(
            url='https://api.weixin.qq.com/cgi-bin/material/get_material',
            data={
                'media_id': 'xUhxBhgieS0TbuQ3VKqP97ZB6kImKay_-1mjyNlNoXU',
            }
        )
                return HttpResponse(str(uplodimg_json['news_item']))
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#获取素材总数
def get_totalMT(request):
            try:
                total_json = wechat.request.post(
            url='https://api.weixin.qq.com/cgi-bin/material/get_materialcount'
        )
                return HttpResponse('voice_count:'+str(total_json['voice_count'])+'<br/>'+'video_count:'+str(total_json['video_count'])+'<br/>'+'image_count:'+str(total_json['image_count'])+'<br/>'+'news_count:'+str(total_json['news_count'])+'<br/>')
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#获取素材列表
def get_listMT(request):
            try:
                list_json = wechat.request.post(
            url='https://api.weixin.qq.com/cgi-bin/material/batchget_material',
            data={
                   'type':'news',
                   'offset':0,
                   'count':20
            }
        )
                return HttpResponse('total_count:'+str(list_json['total_count'])+'<br/>'+'item_count:'+str(list_json['item_count'])+'<br/>'+'item:'+str(list_json['item']))
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

#获取用户列表
def get_listUser(request):
            try:
                list_json = wechat.request.post(
            url='https://api.weixin.qq.com/cgi-bin/user/get?'
        )
                return HttpResponse('total:'+str(list_json['total'])+'<br/>'+'count:'+str(list_json['count'])+'<br/>'+'data:'+str(list_json['data'])+'<br/>'+'next_openid:'+str(list_json['next_openid']))
            except WechatAPIException, e:
                 # logging.exception(e)
                 return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

from django.shortcuts import render
#wap页首页
def login(request):
    return render(request, 'wechat/index.html', '')