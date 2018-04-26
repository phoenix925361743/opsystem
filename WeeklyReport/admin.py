# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from WeeklyReport.models import *

# Register your models here.


@admin.register(PersonalReport)
class PersonalReportAdmin(admin.ModelAdmin):
    list_display = (
        "date_period", "job_type", "job_date", "name", "job_code", "job_status", "summary_status", "delete_status",
    )
    date_hierarchy = "job_date"
    list_filter = ("summary_status", "delete_status", "job_type")


@admin.register(PlanReport)
class PlanReportAdmin(admin.ModelAdmin):
    list_display = (
        "date_period", "job_type", "job_date", "name", "job_code", "job_status",
    )
    date_hierarchy = "job_date"
    list_filter = ("job_type",)


@admin.register(SellProject)
class SellProjectAdmin(admin.ModelAdmin):
    list_display = (
        "s_id", "date_period", "job_code", "job_type", "job_date", "job_status",
    )
    date_hierarchy = "job_date"
    list_filter = ("job_type",)


@admin.register(ProductDevelopment)
class ProductDevelopmentAdmin(admin.ModelAdmin):
    list_display = (
        "date_period", "product", "sub_product",
    )
    list_filter = ("product",)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "desc")


@admin.register(SubProductType)
class SubProductTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "sub_type_name", "desc")


@admin.register(StrategicDeployment)
class StrategicDeploymentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "date_period", "job_name",
    )


@admin.register(TeamBuilding)
class TeamBuildingAdmin(admin.ModelAdmin):
    list_display = (
        "build_type", "sub_type", "date_period", "people",
    )


@admin.register(BuildType)
class BuildTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name", "desc")


@admin.register(SubBuildType)
class SubBuildTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name", "sub_type_name", "desc")


@admin.register(DatePeriod)
class DatePeriodAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "end_date")


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "desc")


@admin.register(JobCode)
class JobCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code", "job_type", "job_name", "old_code", "jf", "jf_name", "person_in_charge",
    )
    list_filter = ("job_type",)
    search_fields = ("code", "job_name", "old_code", "person_in_charge")


@admin.register(JobStatus)
class JobStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "desc")


@admin.register(SummaryStatus)
class SummaryStatusAdmin(admin.ModelAdmin):
    list_display = ("status", "desc")


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "desc")

