# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from wechat_sdk.exceptions import WechatAPIException

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
            from wechat_sdk.messages import EventMessage,TextMessage
            if isinstance(wechat.message, EventMessage):
                if wechat.message.type == 'click':
                    return HttpResponse(wechat.response_text('这是测试回复！！', escape=False))
            elif isinstance(wechat.message, TextMessage):
                # if wechat.message.content =='交流':
                    return HttpResponse(wechat.response_text('test_jiaoliu', escape=False))
    except WechatAPIException, e:
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)

def init_conf(request):
        try:
            wechat.create_menu({'button':[
                     {
                    'type': 'click',
                    'name': '交流社区',
                    'key': 'V1001_TODAY_JIAOLIU'
                }
            ]
            })
            return  HttpResponse('create a menu success!')
        except WechatAPIException, e:
             return  HttpResponse('errcode:'+str(e.errcode)+'<br/>errmsg:'+e.errmsg)
