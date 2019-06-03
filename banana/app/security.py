# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask import redirect
from flask_appbuilder.actions import action
from flask_appbuilder.security.views import UserDBModelView

class MyUserDBView(UserDBModelView):
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
            self.datamodel.delete_all(items)
            self.update_redirect()
            return redirect(self.get_redirect())

class MySecurityManager(SecurityManager):
    userdbmodelview = MyUserDBView