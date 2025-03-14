# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import os
import uuid
import configparser
import markdown
from bs4 import BeautifulSoup

"""
@brief 获取文件配置信息
@param file_name 配置文件名称
@param section 节点名称
@param option Item
"""
def fetch_conf(file_name = '', section = '', option = ''):
    file = os.path.abspath(os.path.join(os.getcwd(), 'conf', file_name))

    config = configparser.ConfigParser()
    config.read(file, encoding='utf-8')
    result = config.get(section, option)

    return result

"""
@brief Markdown转文本
"""
def markdown2text(text):
	html = markdown.markdown(text)
	soup = BeautifulSoup(html, 'html.parser')
	return soup.get_text()

"""
@brief 滑动窗口切分chunk
"""
def sliding_window_chunk(text, window_size = 20, step_size = 10):
	"""
	使用滑动窗口切分文本。
	参数:
	text (str): 要切分的文本。
	window_size (int): 窗口大小（字符数或词数）。
	step_size (int): 滑动步长（字符数或词数）。
	返回:
	list: 切分后的文本块列表。
	"""
	chunks = []
	for i in range(0, len(text), step_size):
		chunk = text[i:i + window_size]
		chunks.append(chunk)
	return chunks

"""
@brief uuid
"""
def unique_id():
	return str(uuid.uuid4())
