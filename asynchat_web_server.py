# -*- coding:UTF-8 -*-
"""
使用 asynchat 实现的简易异步HTTP服务器
基于 asyncore ,该模块目前在python3.6中已被弃用
"""

import asynchat, asyncore, socket
import os
import mimetypes
import urllib.parse as urlparse

from http.client import responses  # python3

class async_http(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4协议，TCP套接字
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置socket地址复用
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):  # 收到新链接时对监听的套接字调用该方法
        client, addr = self.accept()
        return async_http_handler(client)

class async_http_handler(asynchat.async_chat):
    """处理异步HTTP请求的类"""
    def __init__(self, conn = None):
        asynchat.async_chat.__init__(self, conn)
        self.data = []  # 数据缓冲区
        self.got_header = False
        self.set_terminator(b"\r\n\r\n")  # 设置空白行表示到达终止符

    def collect_incoming_data(self, data):
        """必须要实现的方法，处理传入的数据"""
        if not self.got_header:
            self.data.append(data)  # 获取传入的数据并将其添加到数据缓冲区

    def found_terminator(self):
        """必须实现的的方法，出现终止符时，实现某种功能"""
        self.got_header = True
        header_data = b"".join(self.data)
        # 将报头数据解码为文本以便进一步处理
        head_text = header_data.decode('utf-8')
        header_lines = head_text.splitlines()
        request = header_lines[0].split()  # [method url HTTP/1.1]
        op = request[0]  # 请求方法
        url = request[1][1:]  # 把/去了
        url = urlparse.unquote(url)  # encoding 参数仅适用于 Python3 ,默认utf-8
        self.process_request(op, url)

    def process_request(self, op, url):
        """处理请求"""
        if op == "GET":
            if not os.path.exists(url):
                self.send_error(404, "File %s not found\r\n" % url)
            else:
                type, encoding = mimetypes.guess_type(url)  # 猜测 url 的 MIME 类型
                size = os.path.getsize(url)
                self.push_text("HTTP/1.0 200 OK\r\n")
                self.push_text("Content-length: %s\r\n" % size)
                self.push_text("Content-type: %s;charset=UTF-8\r\n" % type)
                self.push_text("\r\n")
                self.push_with_producer(file_producer(url))  # 放入可调用 more() 方法的生产者对象
        else:
            self.send_error(501, "%s method not implemented" % op)
        self.close_when_done()  # 关闭通道

    def push_text(self, text):
        """将文本加入到传出流中，首先需要编码"""
        self.push(text.encode("utf-8"))

    def send_error(self, code, message):
        """处理错误请求"""
        self.push_text("HTTP/1.0 %s %s\r\n" % (code, responses[code]))
        self.push_text("Content-type: text/plain\r\n")
        self.push_text("\r\n")
        self.push_text(message)

class file_producer(object):
    def __init__(self, filename, buffer_size = 512):
        self.f = open(filename, "rb")  # 默认文件编码为 UTF-8
        self.buffer_size = buffer_size

    def more(self):
        data = self.f.read(self.buffer_size)
        if not data:
            self.f.close()
        return data

if __name__ == '__main__':
    a = async_http(8080)
    asyncore.loop()