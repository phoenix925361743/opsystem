# opsystem 
Automatic ops system for department

### 项目说明
*基于python2.7+django1.11.6+layui2.2构建；
*包含周报管理模块、资产管理模块、cobbler接口整合模块、用户控制模块；
*项目主要用于日常办公及自动化运维。
  
 ### 项目部署
 *下载源码至本地；
 *修改settings.py中的数据库连接设置；
 *按照README中的第三方库记录，预先准备好项目运行环境；
 *进入/OPSystem/下，执行python manage.py makemigrations && python manage.py migrate进行数据库结构的初始化；
 *进入/install目录，执行python initialization.py进行数据库初始化，初始化完毕后会创建默认的超级管理员账号：admin/antiy?test;
 *执行python manage.py runserver 0.0.0.0:80，即可运行项目；
 *打开浏览器，访问http://x.x.x.x:80.
