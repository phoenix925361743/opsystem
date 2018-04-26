#!/usr/bin/env python
# coding:utf-8


import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPSystem.settings")
django.setup()


def permission_add():
    """动态获取app下的url列表，并根据url的name值创建权限控制记录"""
    from OPSystem.settings import INSTALLED_APPS
    from UserAccess.models import Permission
    from OPSystem.urls import urlpatterns as root_url
    for app in INSTALLED_APPS:
        try:
            m = __import__(app + ".urls")
            for url in m.urls.urlpatterns:
                if url.name:
                    Permission.objects.get_or_create(permission_name=app + "-" + url.name, permission_value=url.name)
        except ImportError:
            pass
        except AttributeError:
            pass
    for r_url in root_url:
        try:
            if r_url.name:
                Permission.objects.get_or_create(permission_name="opsystem-" + r_url.name, permission_value=r_url.name)
        except AttributeError:
            pass
    Permission.objects.get_or_create(permission_name=u"仪表板", permission_value="Dashboard")  # 仪表板
    Permission.objects.get_or_create(permission_name=u"资产管理", permission_value="AssetManagement")  # 资产管理父菜单
    Permission.objects.get_or_create(permission_name=u"资产管理-机柜管理", permission_value="AssetManagementCabinet")  # 机柜管理
    Permission.objects.get_or_create(permission_name=u"资产管理-设备管理", permission_value="AssetManagementService")  # 设备管理
    Permission.objects.get_or_create(permission_name=u"资产管理-IP管理", permission_value="AssetManagementIPaddress")  # IP管理
    Permission.objects.get_or_create(permission_name=u"资产管理-常用资产管理", permission_value="AssetManagementNormalAsset")  # 常用资产管理
    Permission.objects.get_or_create(permission_name=u"资产管理-机柜管理", permission_value="AssetManagementCabinet")  # 机柜管理
    Permission.objects.get_or_create(permission_name=u"自动灌装", permission_value="Cobbler")  # 自动灌装
    Permission.objects.get_or_create(permission_name=u"自动灌装-灌装管理", permission_value="CobblerInstall")  # 灌装管理
    Permission.objects.get_or_create(permission_name=u"自动灌装-高级设置", permission_value="CobblerAdvanced")  # 高级设置
    Permission.objects.get_or_create(permission_name=u"文档资料", permission_value="Document")  # 文档资料
    Permission.objects.get_or_create(permission_name=u"周报管理", permission_value="WeeklyReport")  # 周报管理
    Permission.objects.get_or_create(permission_name=u"周报管理-周报填写", permission_value="WeeklyReportWrite")  # 周报填写
    Permission.objects.get_or_create(permission_name=u"周报管理-周报汇总", permission_value="WeeklyReportSummary")  # 周报汇总
    Permission.objects.get_or_create(permission_name=u"周报管理-高级设置", permission_value="WeeklyReportAdvancedSetting")  # 高级设置
    Permission.objects.get_or_create(permission_name=u"系统设置", permission_value="SystemSetting")  # 系统设置
    Permission.objects.get_or_create(permission_name=u"系统设置-用户管理", permission_value="SystemSettingUser")  # 用户管理
    Permission.objects.get_or_create(permission_name=u"系统设置-关于", permission_value="SystemSettingAbout")  # 关于
    print u"权限数据初始化完成!"


def create_superuser():
    """创建超级管理员"""
    from UserAccess.models import MyUser, Roles, Permission, Department, UserGroup, UserProfile
    import initial_setting
    role = Roles.objects.get_or_create(role_name=u"超级管理员")[0]  # 创建超级管理员角色
    user_group = UserGroup.objects.get_or_create(group_name=u"超级管理员")[0]  # 创建超级管理员组
    permission = Permission.objects.all()  # 获取所有权限
    role.permission = permission  # 将所有权限赋值给超级管理员角色
    user_group.group_permission = permission
    depart = Department.objects.get_or_create(depart=initial_setting.default_department)[0]
    user = MyUser.objects.filter(username=initial_setting.superuser, email=initial_setting.email)
    if not user:
        super_user = MyUser.objects.create(username=initial_setting.superuser, password=initial_setting.password,
                                           email=initial_setting.email, depart=depart, use=True)
        user_group.group_user = [super_user]  # 添加超级管理员到超级管理员组
        super_user.role = [role]
        UserProfile.objects.get_or_create(user=super_user)
    print u"超级管理员创建完成!"
    from django.contrib.auth.models import User
    from django.db.utils import IntegrityError
    try:
        User.objects.create_superuser(username=initial_setting.superuser, password=initial_setting.password,
                                      email=initial_setting.email)
    except IntegrityError:
        pass
    print u"admin超级管理员创建完成！"


def role_add():
    """初始化角色权限"""
    from UserAccess.models import Roles, Permission
    normal_role = Roles.objects.get_or_create(role_name=u"用户")[0]
    admin_role = Roles.objects.get_or_create(role_name=u"管理员")[0]
    normal_permission = [
        "index", "daily_report", "daily_report_data", "delete_report_data", "daily_report_add", "daily_report_add_form",
        "daily_report_modify", "job_type_get", "username_get", "depart_get", "job_code_get", "job_status_get",
        "date_period_get", "daily_report_delete", "build_type_get", "sub_type_get", "weekly_report_get", "project_get",
        "plan_report_add_form", "plan_report_add", "plan_report_get", "plan_report_delete",
        "login", "logout", "regist", "auth_code", "user_info", "user_setting", "change_pass", "show_record",
        "not_read_notification_number_get", "notification_get", "notification_form", "level_get", "change_read_status",
        "notification_delete", "install", "system_get", "system_add_form", "system_add", "system_modify", "system_delete",
        "profile_get", "install_switch", "privilege_manage", "privilege_get", "privilege_delete", "privilege_add", "privilege_add_form",
        "profile_add_form", "ks_get", "profile_add", "distro_get", "profile_delete", "profile_delete_check", "system_log_get", "listen_get",
        "ks_add_form", "ks_add", "ks_delete_check", "ks_delete", "system_about", "memorandum_add_form", "memorandum_get", 'memorandum_status_get',
        "memorandum_add", "memorandum_edit_form", "memorandum_edit", "export_daily_report", "version_get", "ip_address", "ip_address_get",
        "ip_status_get", "area_get", "depart_asset", "use_type_get", "depart_asset_get", "depart_asset_detail", "apply_add", "apply_add_form"
    ]  # 用户默认的url访问权限
    normal_permission += [
        "Dashboard", "WeeklyReport", "WeeklyReportWrite", "SystemSetting", "SystemSettingAbout"
    ]  # 用户默认的页面菜单可见权限
    admin_permission = normal_permission + [
        "report_summary", "daily_summary_get", "plan_summary_get", "daily_report_audit", "daily_report_audit_batch",
        "sell_project_get", "this_week_get", "summary_status_get", "product_development_add_form", "product_type_get",
        "sub_product_get", "product_development_add", "product_development_get", "product_development_table",
        "product_development_table_get", "product_development_delete", "strategic_deployment_get",
        "strategic_deployment_delete", "strategic_deployment_add_form", "strategic_deployment_add",
        "strategic_deployment_delete_table", "strategic_deployment_table_get", "team_building_get",
        "team_building_add_form", "team_building_add", "team_building_delete_table", "team_building_table_get",
        "team_building_delete", "advanced_setting", "export_weekly_report", "job_code_add_form", "job_code_add",
        "job_code_delete", "product_type_add_form", "sub_product_add_form", "product_type_add", "sub_product_add",
        "product_type_delete", "sub_product_delete", "job_code_upload", "user_manage", "user_get", "user_add_form",
        "role_get", "user_group_get", "use_switch", "user_delete", "user_add", "cobbler_advanced", "system_audit_get",
        "system_audit", "ip_add_form", "ip_address_add", "ip_delete", "ip_add_batch_form", "ip_address_add_batch",
        "depart_asset_add_form", "depart_asset_add", "edit_lifecycle_form", "lifecycle_update", "edit_property_form",
        "property_add", "delete_property_form", "property_get", "edit_property", "property_delete", "asset_record_get",
        "asset_record_switch", "depart_asset_delete"
    ]  # 管理员默认的url访问权限
    admin_permission += [
        "Dashboard", "WeeklyReport", "WeeklyReportWrite", "WeeklyReportSummary", "WeeklyReportAdvancedSetting", "SystemSetting",
        "SystemSettingUser", "SystemSettingAbout", "AssetManagementIPaddress"
    ]  # 管理员默认的页面菜单可见权限
    p1_list = []
    p2_list = []
    for p1 in normal_permission:
        print p1
        p1_list.append(Permission.objects.get(permission_value=p1))
    normal_role.permission = p1_list  # 赋值普通用户权限
    for p2 in admin_permission:
        print p2
        p2_list.append(Permission.objects.get(permission_value=p2))
    admin_role.permission = p2_list  # 赋值管理员权限
    print u"角色权限初始化完成!"


def team_build_add():
    from WeeklyReport.models import BuildType, SubBuildType
    a = BuildType.objects.get_or_create(type_name=u"关键人员补充或培养")[0]
    b = BuildType.objects.get_or_create(type_name=u"能力情况")[0]
    c = BuildType.objects.get_or_create(type_name=u"绩效情况")[0]
    d = BuildType.objects.get_or_create(type_name=u"作风情况")[0]
    SubBuildType.objects.get_or_create(type_name=a, sub_type_name=u"架构师")
    SubBuildType.objects.get_or_create(type_name=a, sub_type_name=u"产品经理")
    SubBuildType.objects.get_or_create(type_name=a, sub_type_name=u"骨干研发/技术")
    SubBuildType.objects.get_or_create(type_name=a, sub_type_name=u"管理人员")
    SubBuildType.objects.get_or_create(type_name=b, sub_type_name=u"能力成长突出人员")
    SubBuildType.objects.get_or_create(type_name=b, sub_type_name=u"能力成长缓慢人员")
    SubBuildType.objects.get_or_create(type_name=c, sub_type_name=u"绩效突出人员")
    SubBuildType.objects.get_or_create(type_name=c, sub_type_name=u"绩效落后人员")
    SubBuildType.objects.get_or_create(type_name=d, sub_type_name=u"作风强悍人员")
    SubBuildType.objects.get_or_create(type_name=d, sub_type_name=u"作风散漫人员")
    print u"团队建设数据表初始化完成!"


def notification_level_add():
    from DashBoard.models import Level
    Level.objects.get_or_create(level="INFO")
    Level.objects.get_or_create(level="WARNING")
    Level.objects.get_or_create(level="DANGER")
    Level.objects.get_or_create(level="CRITICAL")
    print u"消息等级初始化完成!"


def audit_add():
    from WeeklyReport.models import SummaryStatus
    SummaryStatus.objects.get_or_create(status=u"未审")
    SummaryStatus.objects.get_or_create(status=u"通过")
    SummaryStatus.objects.get_or_create(status=u"驳回")
    SummaryStatus.objects.get_or_create(status=u"重提")
    print u"审核状态初始化完成！"


def ks_initial():
    import paramiko
    from Cobbler.models import Kickstart
    from install import initial_setting as ini
    from UserAccess.models import MyUser
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    user = MyUser.objects.get(username="admin")
    try:
        ssh.connect(ini.cobbler_server_ip, 22, "root", ini.cobbler_root_password, timeout=5)  # 创建ssh连接，并设置超时时间为5秒
        command = """ls -l %s | grep -v "^d" | awk '{print $9}'""" % ini.cobbler_ks_dir
        _, stdout, _ = ssh.exec_command(command)
        ks_file = stdout.read().split("\n")
        for f in ks_file:
            if f:
                _, content, _ = ssh.exec_command("cat %s" % ini.cobbler_ks_dir + f)
                Kickstart.objects.get_or_create(name=f, owner=user, content=content.read())
        print u"KS文件初始化完毕!"
    except paramiko.AuthenticationException:
        print u"认证失败，请检查账号密码"


def memorandum_status_add():
    from DashBoard.models import MemorandumStatus
    MemorandumStatus.objects.get_or_create(name=u"未开始")
    MemorandumStatus.objects.get_or_create(name=u"进行中")
    MemorandumStatus.objects.get_or_create(name=u"已完成")
    MemorandumStatus.objects.get_or_create(name=u"作废")
    print u"备忘录状态初始化完毕"


def version_type_add():
    from DashBoard.models import UpdateType
    UpdateType.objects.get_or_create(name=u"Bug修复")
    UpdateType.objects.get_or_create(name=u"功能新增")
    UpdateType.objects.get_or_create(name=u"需求完善")
    print u"版本更新类型初始化完毕"


def ip_status_add():
    from Asset.models import IpStatus
    IpStatus.objects.get_or_create(status=u"占用")
    IpStatus.objects.get_or_create(status=u"空闲")
    IpStatus.objects.get_or_create(status=u"临时")
    IpStatus.objects.get_or_create(status=u"其他")
    print u"ip状态初始化完毕"


def area_add():
    from Asset.models import Area
    Area.objects.get_or_create(name=u"负一楼机房")
    Area.objects.get_or_create(name=u"办公区")
    Area.objects.get_or_create(name=u"虚拟机")
    print u"区域信息初始化完毕"


def use_type():
    from Asset.models import UseType
    UseType.objects.get_or_create(name=u"借出")
    UseType.objects.get_or_create(name=u"归还")
    UseType.objects.get_or_create(name=u"闲置")
    UseType.objects.get_or_create(name=u"领用")
    UseType.objects.get_or_create(name=u"损坏")
    print u"使用类型信息初始化完毕"


if __name__ == "__main__":
    permission_add()
    create_superuser()
    role_add()
    team_build_add()
    notification_level_add()
    audit_add()
    # ks_initial()
    memorandum_status_add()
    version_type_add()
    ip_status_add()
    area_add()
    use_type()


