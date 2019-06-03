from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder import expose

from . import appbuilder, db
from .models import questionModel,answerModel

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


class questionView(ModelView):
    route_base = "/question"
    datamodel = SQLAInterface(questionModel)

    label_columns = {"title":"Question Title", "created_at":"Create", "user":"asker"}

    add_columns = ["title","content"]
    edit_columns = ["title","content"]
    list_columns = ["title","user","user.username", "user.email","content"]

    @expose("/detail/<question_id>/")
    def question_detail(self,question_id):
        question = self.datamodel.get(question_id)
        context = {
            "question_id":question.id,
            "title":question.title,
            "content":question.content,
            "asker":question.user,
            "asktime":question.created_at,
            "edittime":question.updated_at,
            "answers":question.answers,
        }
        return self.render_template("question_detail.html",context= context)

class answerView(ModelView):
    route_base = "/answer"
    datamodel = SQLAInterface(answerModel)

    label_columns = {"content":"answer",
                     "question.user":"asker",
                     "question.content":"question",
                     "question.title":"q title",
                     }

    list_title = "Answers!"
    show_columns = ["question.title","question.content","question.user","content","created_at","updated_at"]

appbuilder.add_view(questionView,"Questions", category="Q&A")
appbuilder.add_view(answerView,"Answers", category="Q&A")

db.create_all()
