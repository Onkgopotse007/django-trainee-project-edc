from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_url = '/administration/'
    enable_nav_sidebar = True
    site_header = 'TraineeProject Subject'
    site_title = 'TraineeProject Subject'
    index_title = 'TraineeProject Subject'


traineeproject_admin = AdminSite(name='traineeproject_admin')
