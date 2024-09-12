### 项目介绍

项目使用框架: Flask

目前支持的搜索平台：

- X.com：使用 socialdata api 搜索数据，需在[SocialData](https://socialdata.tools/)中获取Api kye.

- Reddit：使用 asyncpraw 搜索数据，参考该[文档](https://towardsdatascience.com/scraping-reddit-with-praw-76efc1d1e1d9)在[Reddit Apps 页面](https://www.reddit.com/prefs/apps)注册一个app，获取client_id和client_secret。


**项目部署：**
1. 安装python环境，建议使用python3.11
2. 安装依赖包 pip install -r requirements.txt
3. 设置修改环境变量  cp .env.example .env
4. 调试项目 python main.py
5. 访问 http://localhost:5000
6. api文档 http://localhost:5000/docs
7. 使用gunicorn部署： 
   ```sh
   pip install gunicorn gevent
   gunicorn main:app -b 0.0.0.0:5000 --workers 4 --threads 4 --timeout 60 --worker-class gevent
   ```

### 在Dify中使用

1. 将add_tool_openapi.json添加到自定义工具

    **注：** 修改 add_tool_openapi.json 中 **servers url** 为部署该服务的地址
   
2. 导入Dify应用配置文件Dify_Search_social_data.yml

    在Dify中添加自定义工具后，在工作室中，以导入DSL文件的方式创建应用，选择Dify_Search_social_data.yml 

3. 设置修改LLM使用的模型