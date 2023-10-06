from flask_login import current_user
from models.Recommendation import Recommendation
from models.Thesis import Thesis
from sqlalchemy import text

class ControllerRecommendation():

    @classmethod
    def get_thesis_by_author_advisor(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetThesisByAdvisor(:advisor_id);")
            params = {'advisor_id' : id}
            result = session.execute(sql, params)
            rows=result.fetchall()
            thesiss = []
            if rows != None:
                for row in rows:
                    thesis = Thesis(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    thesiss.append(thesis)
                return thesiss
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_recommendation_by_thesis_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT recommendation_id, recommendation_date, recommendation_text, thesis_id, advisor_id "
                "FROM RECOMMENDATION "
                "WHERE thesis_id = :id"
            )
            result = session.execute(sql, {"id": id})
            session.commit()
            row = result.fetchone()
            if row:
                recommendation = {
                    'recommendation_id': row[0],
                    'recommendation_date': row[1],
                    'recommendation_text' : row[2],
                    'thesis_id' : row[3],
                    'advisor_id': row[4]
                }
                return recommendation
            else:
                return None
        except Exception as ex:
            raise Exception(ex)