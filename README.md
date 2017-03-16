# vn.py - 基于python的开源交易平台开发框架

---
### Quick Start

对于大部分用户来说，无需自行编译API接口，可以直接使用vn.trader进行交易和策略开发：

1. 准备一台Windows 7 64位系统的电脑

2. 安装[Anaconda](http://www.continuum.io/downloads)：下载**Anaconda 4.0.0** Python 2.7 32位版本，**注意必须是32位**

3. 安装[MongoDB](https://www.mongodb.org/downloads#production)：下载Windows 64-bit 2008 R2+版本

4. 安装pymongo：在cmd中运行pip install pymongo

5. 参考[这里](http://jingyan.baidu.com/article/6b97984dbeef881ca2b0bf3e.html)，将MongoDB注册为Windows服务并启动

6. 安装[Visual C++  Redistributable Packages for VS2013](https://www.microsoft.com/en-gb/download/details.aspx?id=40784)，中英文随意

7. 在本页面选择Download ZIP下载项目代码，并解压到C:\vnpy

8. 在[SimNow](http://simnow.com.cn/)注册CTP仿真账号，记下你的**账号、密码、经纪商编号**，然后下载快期查询你的**交易和行情服务器地址**

9. 把C:\vnpy\vn.trader\ctpGateway\CTP_connect.json中的账号、密码、服务器等修改为上一步注册完成后你的信息（注意使用专门的编程编辑器，如Sublime Text等，防止json编码出错）

10. 双击运行C:\vnpy\vn.trader\vtMain.py，开始交易！


其他
============================

*   `TODO`_