#!/bin/bash

# 早安新闻助手 - 每日自动推送脚本
# 运行时间：每天早上7:58（提前2分钟执行）

# 设置环境变量（cron 环境缺少这些变量）
export HOME=/home/spin6lock
export PATH=/home/spin6lock/.local/bin:/usr/local/bin:/usr/bin:/bin

# 获取所有数据（新闻、诗歌、天气），并保存到today.md（静音模式，只输出markdown）
python3 /home/spin6lock/opensource/morning_news/main.py --all -o > /home/spin6lock/opensource/morning_news/today.md

# 发送到RocketChat
python3 /home/spin6lock/opensource/push_to_rocketchat/push_worklog.py /home/spin6lock/opensource/morning_news/today.md '#good_morning'

echo "每日早安推送完成 - $(date)"
