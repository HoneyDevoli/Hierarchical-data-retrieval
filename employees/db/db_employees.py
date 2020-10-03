from typing import List, Optional


class NotFoundError(Exception):
    """Raised than db query return None"""
    pass


class EmployeeDb:
    def __init__(self, conn):
        """Database class for working employees

        :param conn: active connection to the database
        """
        self.conn = conn

    def is_employee_id(self, id_: int) -> bool:
        """Сhecks that the ID belongs to the employee
        :param id_: row id in database
        :return True if row in db is belong to employee"""

        with self.conn.cursor() as curr:
            sql = """select type
                from organization
                where id = %s
            """
            curr.execute(sql, (id_,))
            if not curr.fetchone():
                raise NotFoundError

            type_ = curr.fetchone()[0]
            return type_ == 3

    def get_office_id(self, id_worker: int) -> Optional[int]:
        """Returns the ID of the office to which the employee belongs.

        :param id_worker: worker id in db
        :return: office id in db
        """
        with self.conn.cursor() as curr:
            sql = """with recursive r as (
                        select id,parentid,name,type from organization
                        where id = %s
                            union
                        select org.id,org.parentid,org.name,org.type
                        from organization org
                        join r on org.id = r.parentid
                      )
                      select id from r where type = 1;"""
            curr.execute(sql, (id_worker,))
            row = curr.fetchone()

            return row[0] if row else None

    def get_employees(self, office_id) -> List[str]:
        """Returns a list of the names of employees working in this office.

        :param office_id: id office in db
        :return: a list of employees
        """
        with self.conn.cursor() as curr:
            sql = """with recursive r as (
                          select id,parentid,name,type
                          from organization
                          where id=%s
                            union
                          select org.id, org.parentid, org.name,org.type
                          from organization org
                          join r on org.parentid = r.id
                      )
                      select name from r where type = 3;"""
            curr.execute(sql, (office_id,))

            # load all lines into memory, because there are not many of them
            rows = curr.fetchall()
            return [row[0] for row in rows]
