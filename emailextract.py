# =================================
# File : emailextract.py
# Description : 
# Author : QinLing
# CREATE TIME : 2024/1/17 19:22
# =================================
import email
from email import policy
import os
import glob
import re
# 处理邮件
def process_part(part,i):
    content_type = part.get_content_type()
    content_disposition = str(part.get("Content-Disposition"))

    if "attachment" in content_disposition:
        # 这是一个附件
        filename = part.get_filename()
        # 这里设置需要添加到的目录

        if filename:
            filedir = "../项目/"
            foldername = filedir + str(i) + ' '+extract_id_and_name(filename)
            os.makedirs(foldername,exist_ok=True)
            # 如果附件有文件名，保存它
            with open(foldername +'/'+ filename, 'wb') as f:
                f.write(part.get_payload(decode=True))
        else:
            print("附件没有文件名!")
    elif content_type == "multipart/mixed":
        # 这是一个多部分邮件，我们需要进一步遍历
        for subpart in part.get_payload():
            process_part(subpart,i)
    elif content_type == "text/plain" or content_type == "text/html":
        # 这是邮件的正文部分，您可以根据需要处理它
        print("邮件正文:", part.get_payload(decode=True).decode())
    else:
        return False
    return True



# 打开邮件
def open_eml(path,i):
    with open(path, 'rb') as f:
        raw_email = f.read()
    msg = email.message_from_bytes(raw_email, policy=policy.default)
    if not process_part(msg,i):
        print('该邮件存在问题:'+path)


#找到所有的eml文件
def find_eml_files(path='.'):
    """递归地查找指定路径及其子目录中的所有.eml文件"""
    eml_files = []
    # 遍历当前目录中的所有文件和文件夹
    for root, dirs, files in os.walk(path):
        # 使用glob来匹配.eml文件
        for file in glob.glob(os.path.join(root, '*.eml')):
            eml_files.append(file)
    return eml_files

#解析学号与姓名
def extract_id_and_name(str):
    #寻找数字
    id = re.findall(r"\d+",str)
    #寻找中文名字
    excluded_phrases = ["嵌入式", "系统", "建模", "模型", "与", "规范", "大", "作业"]
    all_chinese_phrases = re.findall('[\u4e00-\u9fa5]+', str)
    filtered_phrases = [phrase for phrase in all_chinese_phrases if not any(excl in phrase for excl in excluded_phrases)]
    for phrase in filtered_phrases:
        print(phrase)
        if id :
            return id[0] + ' ' + phrase
        else:
            return phrase
    return '无命名'
def main():
     # 调用函数，查找当前目录及其子目录中的所有.eml文件
    eml_files = find_eml_files()
    # 打印找到的.eml文件路径
    i = 0
    for file in eml_files:
        i += 1
        open_eml(file, i)
        
        print('已找到'+ str(i) + '个邮件')
    # extract_id_and_name()


if __name__ == "__main__":
    main()