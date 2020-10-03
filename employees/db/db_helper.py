def create_table(conn):
    """Create table organization.
    :param conn: active connection to db
    :return: None
    """
    with conn.cursor() as curr:
        sql = """CREATE TABLE IF NOT EXISTS organization (
                 id serial INT, ParentId INT,
                 Name VARCHAR (150), Type INT);
                 CREATE INDEX
                 IF NOT EXISTS organization_id_idx
                 on organization (id);
                 CREATE INDEX
                 IF NOT EXISTS organization_parentid_idx
                 on organization (parentid);
               """
        curr.execute(sql)
        conn.commit()


def save_data(conn, data: dict) -> None:
    """Save data to db.
    :param conn: Active connection to db
    :param data: list of rows for insert to database
    :return: None
    """
    with conn.cursor() as curr:
        sql = """INSERT INTO organization (
                 id, ParentId, Name, type
                 ) VALUES (%(id)s, %(ParentId)s, %(Name)s, %(Type)s);
        """
        curr.executemany(sql, data)
        conn.commit()
