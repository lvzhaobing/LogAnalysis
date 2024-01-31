# QNX Tracelog + hogs日志解析工具

## hogs解析方案介绍

- Web页面基于 .Net Blazor Server 框架, html标签内嵌C#后端代码，通过基于websocket 的 SignalR 实时刷新前端页面显示
- C# Web前端上传日志文件到Server端，后端执行C#代码对日志文件进行归档，之后后端执行的C#代码调用本机python命令处理日志分析任务
- hogs日志解析脚本 使用python实现 正则匹配log文件中的日志内容，提取log中 进程占用的CPU百分比和内存大小
- python脚本内调用jinjia2 html渲染模板，生成静态html分析报告
- 使用JavaScript调用 ECharts 对从日志中分析得到的每条进程的CPU占用历史数据，进行可视化，绘制折线图
- 生成html报告静态页面链接，返回给前端可点击预览

## QNX Tracelog 解析方案介绍
- 前提是解析tracelog需要Linux桌面环境，双击打开qde分析环境，并进行一系列点击操作，是个人工重复执行的任务
- qde内的一系列点击操作，可以把tracelog文件转换成CSV表格导出；
- 这里的CSV表格中的内容：是各用户线程对系统线程 CPU运行时间的贡献绝对值，可用于分析调用关系，和系统进程CPU占用高的原因
- 这里的解析服务是通过docker内托管的NoVnc服务，把Linux桌面环境搬移到web浏览器端
- 使用python脚本调用linux xdotool 命令来模拟鼠标键盘事件 也包括：打开qde窗口 等待qde窗口获得焦点的等事件 来达到UI自动化的目的
- 对于一些位置不固定的按钮图标，则调用opencv图像模板匹配的方式，以图搜图查找按钮位置，然后模拟鼠标点击
- 最终完成UI操作自动执行并导出CSV文件作为分析报告
