import sqlalchemy as sa

from util.data.structures import Timetable
from util.logging import LoggerFactory


class Database:
    def __init__(self, url="sqlite:///edupage.db"):
        self.logger = LoggerFactory.create_logger("Database")
        self.engine = sa.create_engine(url)
        self.metadata = sa.MetaData()
        self.metadata.bind = self.engine
        self.connection = self.engine.connect()
        self.logger.info(f"Connected to database at {url}")

    def create_table(self, table_name, columns):
        table = sa.Table(table_name, self.metadata, *columns)
        table.create(bind=self.engine, checkfirst=True)
        self.logger.info(f"Created table {table_name}")

    def insert(self, table_name, values):
        table = sa.Table(table_name, self.metadata, autoload=True)
        self.connection.execute(table.insert(), values)
        self.logger.info(f"Inserted {len(values)} rows into {table_name}")

    def select(self, table_name, columns):
        table = sa.Table(table_name, self.metadata, autoload=True)
        query = sa.select(columns).select_from(table)
        return self.connection.execute(query).fetchall()

    def drop_table(self, table_name):
        table = sa.Table(table_name, self.metadata, autoload=True)
        table.drop()
        self.logger.warning(f"Dropped table {table_name}")

    # TODO: Make this work lol
    def update_timetable(self, timetable: Timetable):
        # Create tables
        self.create_table(
            "classes",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("name", sa.String),
                sa.Column("short", sa.String),
            ],
        )
        self.create_table(
            "groups",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("divisionid", sa.Integer),
                sa.Column("name", sa.String),
                sa.Column("classid", sa.Integer),
                sa.Column("entireclass", sa.Boolean),
            ],
        )
        self.create_table(
            "teachers",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("name", sa.String),
            ],
        )
        self.create_table(
            "periods",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("name", sa.String),
                sa.Column("start", sa.Time),
                sa.Column("end", sa.Time),
            ],
        )
        self.create_table(
            "classrooms",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("name", sa.String),
                sa.Column("short", sa.String),
            ],
        )
        self.create_table(
            "lessons",
            [
                sa.Column("id", sa.Integer, primary_key=True),
                sa.Column("groupids", sa.String),
                sa.Column("subjectid", sa.Integer),
                sa.Column("teacherids", sa.String),
                sa.Column("periodid", sa.Integer),
                sa.Column("duration", sa.Integer),
            ],
        )

        # Insert data
        self.insert(
            "classes",
            [
                {"id": class_.id, "name": class_.name, "short": class_.short}
                for class_ in timetable.classes
            ],
        )
        self.insert(
            "groups",
            [
                {
                    "id": group.id,
                    "divisionid": group.divisionid,
                    "name": group.name,
                    "classid": group.classid,
                    "entireclass": group.entireclass,
                }
                for group in timetable.groups
            ],
        )
        self.insert(
            "teachers",
            [
                {"id": teacher.id, "name": teacher.name}
                for teacher in timetable.teachers
            ],
        )
        self.insert(
            "periods",
            [
                {"name": period.name, "start": period.start, "end": period.end}
                for period in timetable.periods
            ],
        )
        self.insert(
            "classrooms",
            [
                {"id": classroom.id, "name": classroom.name, "short": classroom.short}
                for classroom in timetable.classrooms
            ],
        )
        self.insert(
            "lessons",
            [
                {
                    "id": lesson.id,
                    "groupids": lesson.groupids,
                    "subjectid": lesson.subjectid,
                    "teacherids": lesson.teacherids,
                    "periodid": lesson.periodid,
                    "duration": lesson.duration,
                }
                for lesson in timetable.lessons
            ],
        )
        self.logger.info("Updated timetable data in database")
