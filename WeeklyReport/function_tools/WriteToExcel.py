#!/usr/bin/env python
# coding:utf-8

from UserAccess.models import MyUser
from WeeklyReport.models import *
import xlwt


def style_cell_bgcolor(color_code):
    """设置单元格背景颜色，color_code为颜色代码"""
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置类型模式为实型
    pattern.pattern_fore_colour = color_code
    return pattern


def style_cell_font(color_code=0x00, font_name=u"微软雅黑", bold=True, height=220):
    """设置单元格字体样式"""
    font = xlwt.Font()
    font.name = font_name  # 设置字体
    font.colour_index = color_code  # 设置字体颜色
    font.bold = bold  # 是否加粗
    font.height = height  # 除以20之后才是excel的字号
    return font


def style_cell_alignment(horz_obj=xlwt.Alignment.HORZ_CENTER, vert_obj=xlwt.Alignment.VERT_CENTER):
    """设置单元格对齐样式"""
    alignment = xlwt.Alignment()
    alignment.horz = horz_obj  # 设置单元格对齐样式，类似于xlwt.Alignment.HORZ_CENTER(居中对齐)等
    alignment.vert = vert_obj  # 设置单元格字体对齐样式，类似于xlwt.Alignment.VERT_CENTER(居中对齐)等
    return alignment


def style_borders_add(line_code=xlwt.Borders.THIN):
    borders = xlwt.Borders()
    borders.left = line_code
    borders.right = line_code
    borders.top = line_code
    borders.bottom = line_code
    return borders


def write_to_excel(request, dp):
    """写入数据至excel"""
    wbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    summary_sheet = wbook.add_sheet(u"小组工作周报", cell_overwrite_ok=True)
    wr_sheet = wbook.add_sheet(u"个人周报", cell_overwrite_ok=True)
    pr_sheet = wbook.add_sheet(u"个人下周计划", cell_overwrite_ok=True)
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
    #####################################################################################
    # 定义样式
    title_style = xlwt.XFStyle()  # 大标题样式
    subtitle_style = xlwt.XFStyle()  # 行标题样式
    content_style = xlwt.XFStyle()  # 内容样式
    #  初始化样式对象
    title_style_bgcolor = style_cell_bgcolor(22)
    subtitle_style_bgcolor = style_cell_bgcolor(44)
    title_font = style_cell_font(height=240)
    content_font = style_cell_font(bold=False)
    title_alignment = style_cell_alignment(horz_obj=xlwt.Alignment.HORZ_LEFT)
    alignment = style_cell_alignment()
    borders = style_borders_add()
    #  设置一级标题样式
    title_style.pattern = title_style_bgcolor
    title_style.font = title_font
    title_style.alignment = title_alignment
    title_style.borders = borders
    #  设置行标题样式
    subtitle_style.pattern = subtitle_style_bgcolor
    subtitle_style.font = title_font
    subtitle_style.alignment = alignment
    subtitle_style.borders = borders
    #  设置正文数据样式
    content_style.font = content_font
    content_style.alignment = alignment
    content_style.borders = borders
    ######################################################################################################
    # 写入小组工作周报数据到excel
    s_title1 = {
        "2": u"项目编号", "3": u"项目内容简介", "4": u"日期", "5": u"本周进展及得失总结", "6": u"下周计划",
        "7": u"总体阶段性计划", "8": u"特殊说明",
    }  # 小组工作周报标题行内容1
    s_title2 = {
        "0": u"产品", "1": u"子产品", "2": u"工作目标", "3": u"工作内容", "4": u"本周进展及得失总结", "5": u"下周计划",
        "6": u"总体阶段性计划", "7": u"特殊说明",
    }  # 小组工作周报标题行内容2
    s_title3 = {
        "0": u"工作名称", "1": u"工作目标", "2": u"工作内容", "3": u"本周进展及得失总结", "4": u"下周计划",
        "5": u"总体阶段性计划", "6": u"特殊说明",
    }  # 小组工作周报标题行内容3
    s_title4 = {
        "0": u"类型", "1": u"子类型", "2": u"人员", "3": u"本周进展及得失总结", "4": u"下周计划",
        "5": u"总体阶段性计划", "6": u"特殊说明"
    }  # 小组工作周报标题行内容4
    col_width = {
        "0": 256 * 20, "1": 256 * 15, "2": 256 * 20, "3": 256 * 60, "4": 256 * 25, "5": 256 * 20,
        "6": 256 * 20, "7": 256 * 20, "8": 256 * 20,
    }  # 列宽
    for k, v in col_width.items():
        summary_sheet.col(int(k)).width = v
    ss = SummaryStatus.objects.get(status=u"通过")
    project_data = SellProject.objects.filter(date_period=dp, job_type=JobType.objects.get(name=u"项目类"),
                                              depart=user.depart)  # 获取项目类周报数据
    project_study_data = SellProject.objects.filter(date_period=dp, job_type=JobType.objects.get(name=u"科研项目"),
                                                    depart=user.depart)  # 获取科研项目类周报数据
    product_development_data = ProductDevelopment.objects.filter(date_period=dp, depart=user.depart)  # 获取产品开发类周报数据
    strategic_deployment_data = StrategicDeployment.objects.filter(date_period=dp, depart=user.depart)  # 获取公司战略部署周报数据
    team_building_data = TeamBuilding.objects.filter(date_period=dp, depart=user.depart)  # 获取团队建设周报数据
    project_number = len(project_data)
    study_number = len(project_study_data)
    row_index = 0  # 设置行索引初始值
    # 写入项目类数据到excel
    summary_sheet.write_merge(row_index, row_index, 0, 8, u"一、营销支撑及项目执行类工作", title_style)  # 合并第一行并填充内容
    row_index += 1
    summary_sheet.write_merge(row_index, row_index, 0, 1, u"类型", subtitle_style)  # 合并第二行前两列并填充标题
    for k, v in s_title1.items():
        summary_sheet.write(row_index, int(k), v, subtitle_style)  # 填充标题
    row_index += 1
    summary_sheet.write_merge(row_index, project_number + row_index + 1, 0, 0, u"销售支撑\n\r及项目执行", subtitle_style)
    if project_number:
        summary_sheet.write_merge(row_index, row_index + project_number - 1, 1, 1, u"售前期", content_style)
        summary_sheet.write(row_index + project_number, 1, u"售中期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index + project_number, i, "", content_style)  # 填充空白单元格样式
        summary_sheet.write(row_index + project_number + 1, 1, u"售后期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index + project_number + 1, i, "", content_style)  # 填充空白单元格样式
        for d in project_data:
            data1 = {
                "2": d.job_code.code, "3": d.project_content, "4": d.job_date.strftime("%Y%m%d"),
                "5": d.job_status.status, "6": d.next_week_plan or "", "7": d.stage_plan or "", "8": d.remark or "",
            }
            for k, v in data1.items():
                summary_sheet.write(row_index, int(k), v, content_style)  # 迭代数据内容写入excel
            row_index += 1  # 递增行索引值
    else:
        summary_sheet.write_merge(row_index, row_index, 1, 1, u"售前期", content_style)
        summary_sheet.write_merge(row_index + 1, row_index + 1, 1, 1, u"售中期", content_style)
        summary_sheet.write_merge(row_index + 2, row_index + 2, 1, 1, u"售后期", content_style)
        # summary_sheet.write(row_index + 1, 1, u"售中期", content_style)
        # summary_sheet.write(row_index + 2, 1, u"售后期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index, i, "", content_style)
            summary_sheet.write(row_index + 1, i, "", content_style)  # 填充空白单元格样式
            summary_sheet.write(row_index + 2, i, "", content_style)
    # 写入科研项目类数据到excel
    row_index += 2
    summary_sheet.write_merge(row_index, row_index + study_number + 1, 0, 0, u"科研项目", subtitle_style)
    if not study_number:
        for i in range(2, 9):
            summary_sheet.write(row_index + study_number + 1, i, "", content_style)  # 填充空白单元格样式
    if study_number:
        summary_sheet.write_merge(row_index, row_index + study_number - 1, 1, 1, u"售前期", content_style)
        summary_sheet.write(row_index + study_number, 1, u"售中期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index + study_number, i, "", content_style)  # 填充空白单元格样式
        summary_sheet.write(row_index + study_number + 1, 1, u"售后期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index + study_number + 1, i, "", content_style)  # 填充空白单元格样式
        for d in project_study_data:
            data2 = {
                "2": d.job_code.code, "3": d.project_content, "4": d.job_date.strftime("%Y%m%d"),
                "5": d.job_status.status, "6": d.next_week_plan or "", "7": d.stage_plan or "", "8": d.remark or "",
            }
            for k, v in data2.items():
                summary_sheet.write(row_index, int(k), v, content_style)
            row_index += 1
    else:
        summary_sheet.write_merge(row_index, row_index, 1, 1, u"售前期", content_style)
        summary_sheet.write_merge(row_index + 1, row_index + 1, 1, 1, u"售中期", content_style)
        summary_sheet.write_merge(row_index + 2, row_index + 2, 1, 1, u"售后期", content_style)
        # summary_sheet.write(row_index + 1, 1, u"售中期", content_style)
        # summary_sheet.write(row_index + study_number + 1, 1, u"售后期", content_style)
        for i in range(2, 9):
            summary_sheet.write(row_index, i, "", content_style)
            summary_sheet.write(row_index + 1, i, "", content_style)  # 填充空白单元格样式
            summary_sheet.write(row_index + 2, i, "", content_style)
    # 写入产品开发类工作数据到excel
    row_index += 2  # 因为所有数据都填入售前期中，多出一行售中期和一行售后期空白行，所以行索引加2
    summary_sheet.write_merge(row_index, row_index, 0, 8,
                              u"二、产品开发类工作（注：按产品规划填写表格，如本周暂无工作只需要填写产品和子产品名称即可）", title_style)
    row_index += 1
    summary_sheet.merge(row_index, row_index, 7, 8, subtitle_style)
    for k, v in s_title2.items():
        summary_sheet.write(row_index, int(k), v, subtitle_style)
    row_index += 1
    if len(product_development_data):
        for d in product_development_data:
            data3 = {
                "0": d.product.type_name, "1": d.sub_product.sub_type_name, "2": d.job_goal, "3": d.job_content,
                "4": d.summarize, "5": d.next_week_plan or "", "6": d.stage_plan or "", "7": d.remark or "",
            }
            for k, v in data3.items():
                summary_sheet.merge(row_index, row_index, 7, 8, content_style)
                summary_sheet.write(row_index, int(k), v, content_style)
            row_index += 1
    else:
        for i in range(0, 8):
            summary_sheet.merge(row_index, row_index, 7, 8, content_style)
            summary_sheet.write(row_index, i, "", content_style)
        row_index += 1
    # 写入公司战略部署数据到excel
    summary_sheet.write_merge(row_index, row_index, 0, 8, u"三、公司战略部署工作（注：填写公司和集团统一部署的工作及完成情况）", title_style)
    row_index += 1
    summary_sheet.merge(row_index, row_index, 6, 8, subtitle_style)
    for k, v in s_title3.items():
        summary_sheet.write(row_index, int(k), v, subtitle_style)
    row_index += 1
    if len(strategic_deployment_data):
        for d in strategic_deployment_data:
            data4 = {
                "0": d.job_name, "1": d.job_goal, "2": d.job_content, "3": d.summarize, "4": d.next_week_plan or "",
                "5": d.stage_plan or "", "6": d.remark or ""
            }
            for k, v in data4.items():
                summary_sheet.merge(row_index, row_index, 6, 8, content_style)
                summary_sheet.write(row_index, int(k), v, content_style)
            row_index += 1
    else:
        for i in range(0, 7):
            summary_sheet.merge(row_index, row_index, 6, 8, content_style)
            summary_sheet.write(row_index, i, "", content_style)
        row_index += 1
    # 写入团队建设数据到excel
    summary_sheet.write_merge(row_index, row_index, 0, 8, u"四、团队建设（注：非每周必填，但最少两周需总结一次团队建设情况）", title_style)
    row_index += 1
    summary_sheet.merge(row_index, row_index, 6, 8, subtitle_style)
    for k, v in s_title4.items():
        summary_sheet.write(row_index, int(k), v, subtitle_style)
    row_index += 1
    if len(team_building_data):
        for d in team_building_data:
            data4 = {
                "0": d.build_type.type_name, "1": d.sub_type.sub_type_name, "2": d.people, "3": d.summarize,
                "4": d.next_week_plan or "", "5": d.stage_plan or "", "6": d.remark or "",
            }
            for k, v in data4.items():
                summary_sheet.merge(row_index, row_index, 6, 8, content_style)
                summary_sheet.write(row_index, int(k), v, content_style)
            row_index += 1
    else:
        for i in range(0, 7):
            summary_sheet.merge(row_index, row_index, 6, 8, content_style)
            summary_sheet.write(row_index, i, "", content_style)
    ###########################################################################################################
    # 个人周报数据汇总到excel
    wr_title = {
        "0": u"工作类别", "1": u"日期", "2": u"部门", "3": u"姓名", "4": u"工作编号", "5": u"工时(人/日)",
        "6": u"工作内容", "7": u"当前进展",
    }  # 个人周报标题行内容
    wr_col_width = {
        "0": 256 * 20, "1": 256 * 20, "2": 256 * 20, "3": 256 * 20, "4": 256 * 20, "5": 256 * 20,
        "6": 256 * 60, "7": 256 * 20,
    }  # 列宽
    for k, v in wr_col_width.items():
        wr_sheet.col(int(k)).width = v
    personal_project_data = PersonalReport.objects.filter(date_period=dp, depart=user.depart, summary_status=ss,
                                                          job_type=JobType.objects.get_or_create(name=u"项目类")[0])
    personal_product_data = PersonalReport.objects.filter(date_period=dp, depart=user.depart, summary_status=ss,
                                                          job_type=JobType.objects.get_or_create(name=u"产品类")[0])
    personal_depart_data = PersonalReport.objects.filter(date_period=dp, depart=user.depart, summary_status=ss,
                                                         job_type=JobType.objects.get_or_create(name=u"部门事务类")[0])
    wr_row_index = 0  # 初始化个人周报汇总页的行索引值
    for k, v in wr_title.items():
        wr_sheet.write(wr_row_index, int(k), v, subtitle_style)
    # 填充项目类数据
    wr_row_index += 1
    if len(personal_project_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_project_data) - 1, 0, 0, u"项目类", subtitle_style)
        for d in personal_project_data:
            data6 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data6.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"项目类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    # 填充产品类数据
    if len(personal_product_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_product_data) - 1, 0, 0, u"产品类", subtitle_style)
        for d in personal_product_data:
            data7 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data7.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"产品类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    # 填充部门事务类数据
    if len(personal_depart_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_depart_data) - 1, 0, 0, u"部门事务类", subtitle_style)
        for d in personal_depart_data:
            data8 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data8.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"部门事务类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    ############################################################################################################
    # 写入下周计划页数据到excel
    pr_title = {
        "0": u"工作类别", "1": u"日期", "2": u"部门", "3": u"姓名", "4": u"工作编号", "5": u"计划开始日期",
        "6": u"计划完成日期", "7": u"实际开始时间", "8": u"实际完成时间", "9": u"计划任务描述", "10": u"进展情况",
    }  # 个人下周计划标题行内容
    pr_col_width = {
        "0": 256 * 20, "1": 256 * 20, "2": 256 * 20, "3": 256 * 20, "4": 256 * 20, "5": 256 * 20,
        "6": 256 * 20, "7": 256 * 20, "8": 256 * 20, "9": 256 * 60, "10": 256 * 20,
    }  # 列宽
    for k, v in pr_col_width.items():
        pr_sheet.col(int(k)).width = v
    plan_project_data = PlanReport.objects.filter(depart=user.depart, date_period=dp,
                                                  job_type=JobType.objects.get_or_create(name=u"项目类")[0])
    plan_product_data = PlanReport.objects.filter(depart=user.depart, date_period=dp,
                                                  job_type=JobType.objects.get_or_create(name=u"产品类")[0])
    plan_depart_data = PlanReport.objects.filter(depart=user.depart, date_period=dp,
                                                 job_type=JobType.objects.get_or_create(name=u"部门事务类")[0])
    pr_row_index = 0
    for k, v in pr_title.items():
        pr_sheet.write(pr_row_index, int(k), v, subtitle_style)
    # 填充下周计划项目类数据
    pr_row_index += 1
    if len(plan_project_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_project_data) - 1, 0, 0, u"项目类", subtitle_style)
        for d in plan_project_data:
            data9 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data9.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"项目类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    # 填充下周计划产品类数据
    if len(plan_product_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_product_data) - 1, 0, 0, u"产品类", subtitle_style)
        for d in plan_product_data:
            data10 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data10.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"产品类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    # 填充下周计划部门事务类数据
    if len(plan_depart_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_depart_data) - 1, 0, 0, u"部门事务类", subtitle_style)
        for d in plan_depart_data:
            data11 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data11.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"部门事务类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    return wbook


def export_daily_report(request, dp):
    wbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    wr_sheet = wbook.add_sheet(u"个人周报", cell_overwrite_ok=True)
    pr_sheet = wbook.add_sheet(u"个人下周计划", cell_overwrite_ok=True)
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))

    # 定义样式
    title_style = xlwt.XFStyle()  # 大标题样式
    subtitle_style = xlwt.XFStyle()  # 行标题样式
    content_style = xlwt.XFStyle()  # 内容样式
    #  初始化样式对象
    title_style_bgcolor = style_cell_bgcolor(22)
    subtitle_style_bgcolor = style_cell_bgcolor(44)
    title_font = style_cell_font(height=240)
    content_font = style_cell_font(bold=False)
    title_alignment = style_cell_alignment(horz_obj=xlwt.Alignment.HORZ_LEFT)
    alignment = style_cell_alignment()
    borders = style_borders_add()
    #  设置一级标题样式
    title_style.pattern = title_style_bgcolor
    title_style.font = title_font
    title_style.alignment = title_alignment
    title_style.borders = borders
    #  设置行标题样式
    subtitle_style.pattern = subtitle_style_bgcolor
    subtitle_style.font = title_font
    subtitle_style.alignment = alignment
    subtitle_style.borders = borders
    #  设置正文数据样式
    content_style.font = content_font
    content_style.alignment = alignment
    content_style.borders = borders
    # 个人周报数据汇总到excel
    wr_title = {
        "0": u"工作类别", "1": u"日期", "2": u"部门", "3": u"姓名", "4": u"工作编号", "5": u"工时(人/日)",
        "6": u"工作内容", "7": u"当前进展",
    }  # 个人周报标题行内容
    wr_col_width = {
        "0": 256 * 20, "1": 256 * 20, "2": 256 * 20, "3": 256 * 20, "4": 256 * 20, "5": 256 * 20,
        "6": 256 * 60, "7": 256 * 20,
    }  # 列宽
    for k, v in wr_col_width.items():
        wr_sheet.col(int(k)).width = v
    personal_project_data = PersonalReport.objects.filter(date_period=dp, name=user,
                                                          job_type=JobType.objects.get_or_create(name=u"项目类")[0])
    personal_product_data = PersonalReport.objects.filter(date_period=dp, name=user,
                                                          job_type=JobType.objects.get_or_create(name=u"产品类")[0])
    personal_depart_data = PersonalReport.objects.filter(date_period=dp, name=user,
                                                         job_type=JobType.objects.get_or_create(name=u"部门事务类")[0])
    wr_row_index = 0  # 初始化个人周报汇总页的行索引值
    for k, v in wr_title.items():
        wr_sheet.write(wr_row_index, int(k), v, subtitle_style)
    # 填充项目类数据
    wr_row_index += 1
    if len(personal_project_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_project_data) - 1, 0, 0, u"项目类", subtitle_style)
        for d in personal_project_data:
            data6 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data6.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"项目类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    # 填充产品类数据
    if len(personal_product_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_product_data) - 1, 0, 0, u"产品类", subtitle_style)
        for d in personal_product_data:
            data7 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data7.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"产品类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    # 填充部门事务类数据
    if len(personal_depart_data):
        wr_sheet.write_merge(wr_row_index, wr_row_index + len(personal_depart_data) - 1, 0, 0, u"部门事务类", subtitle_style)
        for d in personal_depart_data:
            data8 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.job_time, "6": d.job_content, "7": d.job_status.status,
            }
            for k, v in data8.items():
                wr_sheet.write(wr_row_index, int(k), v, content_style)
            wr_row_index += 1
    else:
        wr_sheet.write_merge(wr_row_index, wr_row_index, 0, 0, u"部门事务类", subtitle_style)
        for i in range(1, 8):
            wr_sheet.write(wr_row_index, i, "", content_style)  # 填充空白单元格样式
        wr_row_index += 1
    ############################################################################################################
    # 写入下周计划页数据到excel
    pr_title = {
        "0": u"工作类别", "1": u"日期", "2": u"部门", "3": u"姓名", "4": u"工作编号", "5": u"计划开始日期",
        "6": u"计划完成日期", "7": u"实际开始时间", "8": u"实际完成时间", "9": u"计划任务描述", "10": u"进展情况",
    }  # 个人下周计划标题行内容
    pr_col_width = {
        "0": 256 * 20, "1": 256 * 20, "2": 256 * 20, "3": 256 * 20, "4": 256 * 20, "5": 256 * 20,
        "6": 256 * 20, "7": 256 * 20, "8": 256 * 20, "9": 256 * 60, "10": 256 * 20,
    }  # 列宽
    for k, v in pr_col_width.items():
        pr_sheet.col(int(k)).width = v
    plan_project_data = PlanReport.objects.filter(name=user, date_period=dp,
                                                  job_type=JobType.objects.get_or_create(name=u"项目类")[0])
    plan_product_data = PlanReport.objects.filter(name=user, date_period=dp,
                                                  job_type=JobType.objects.get_or_create(name=u"产品类")[0])
    plan_depart_data = PlanReport.objects.filter(name=user, date_period=dp,
                                                 job_type=JobType.objects.get_or_create(name=u"部门事务类")[0])
    pr_row_index = 0
    for k, v in pr_title.items():
        pr_sheet.write(pr_row_index, int(k), v, subtitle_style)
    # 填充下周计划项目类数据
    pr_row_index += 1
    if len(plan_project_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_project_data) - 1, 0, 0, u"项目类", subtitle_style)
        for d in plan_project_data:
            data9 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data9.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"项目类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    # 填充下周计划产品类数据
    if len(plan_product_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_product_data) - 1, 0, 0, u"产品类", subtitle_style)
        for d in plan_product_data:
            data10 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data10.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"产品类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    # 填充下周计划部门事务类数据
    if len(plan_depart_data):
        pr_sheet.write_merge(pr_row_index, pr_row_index + len(plan_depart_data) - 1, 0, 0, u"部门事务类", subtitle_style)
        for d in plan_depart_data:
            data11 = {
                "1": d.job_date.strftime("%Y%m%d"), "2": d.depart.depart, "3": d.name.username, "4": d.job_code.code,
                "5": d.start_date.strftime("%Y%m%d") if d.start_date else "",
                "6": d.end_date.strftime("%Y%m%d") if d.end_date else "", "10": d.job_status.status,
                "7": d.start_date_r.strftime("%Y%m%d") if d.start_date_r else "",
                "8": d.end_date_r.strftime("%Y%m%d") if d.end_date_r else "", "9": d.job_content,
            }
            for k, v in data11.items():
                pr_sheet.write(pr_row_index, int(k), v, content_style)
            pr_row_index += 1
    else:
        pr_sheet.write_merge(pr_row_index, pr_row_index, 0, 0, u"部门事务类", subtitle_style)
        for i in range(1, 11):
            pr_sheet.write(pr_row_index, i, "", content_style)  # 填充空白单元格样式
        pr_row_index += 1
    return wbook
