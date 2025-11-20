#!/bin/bash

# 早安新闻助手 - 每日自动推送脚本
# 运行时间：每天早上8:00

# 获取poem和天气数据，并保存到today.md（静音模式，只输出markdown）
python3 /home/spin6lock/opensource/morning_news/main.py --poem --weather -o > /home/spin6lock/opensource/morning_news/today.md

# 发送到RocketChat
python3 /home/spin6lock/opensource/push_to_rocketchat/push_worklog.py /home/spin6lock/opensource/morning_news/today.md '#good_morning'

echo "每日早安推送完成 - $(date)"
