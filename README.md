项目使用框架: Flask

项目部署：
1. 安装python环境，建议使用python3.11
2. 安装依赖包 pip install -r requirements.txt
3. 调试项目 python main.py
4. 访问 http://localhost:5000
5. api文档 http://localhost:5000/docs
6. 部署： 
```sh
# 启动gunicorn服务
gunicorn main:app -b 0.0.0.0:5000 --workers 4 --threads 4 --timeout 60 --worker-class gevent
```