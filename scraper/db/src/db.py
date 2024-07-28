import copy

from scraper.config import config
from scraper.log import LoggerFactory
from scraper.structures import Timetable

import sqlalchemy as sa
from sqlalchemy import Boolean, Column, Integer, PickleType, String, Time, UUID
from sqlalchemy.ext.mutable import MutableList


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

        # retrieve columns from table
        table = sa.Table(table_name, self.metadata, autoload=True)
        self.logger.debug(
            f"Created table {table_name} with columns {table.columns.keys()}"
        )

    def insert(self, table_name, values):
        table = sa.Table(table_name, self.metadata, autoload=True)
        self.connection.execute(table.insert(), values)
        self.logger.debug(f"Inserted {len(values)} rows into {table_name}")

    def select(self, table_name, columns):
        table = sa.Table(table_name, self.metadata, autoload=True)
        query = sa.select(columns).select_from(table)
        return self.connection.execute(query).fetchall()

    def drop_table(self, table_name):
        self.metadata.reflect(self.engine)
        table = self.metadata.tables.get(table_name)
        if table is None:
            self.logger.warning(f"Table {table_name} does not exist, skipping drop")
            return
        table.drop(bind=self.engine)
        self.connection.commit()
        self.metadata.clear()
        self.logger.debug(f"Dropped table {table_name}")

    def create_tables(self):
        _base_columns = [
            Column("id", UUID, primary_key=True),
            Column("edu_id", String),
            Column("name", String),
        ]

        # Create tables
        self.create_table(
            "classes",
            [*copy.deepcopy(_base_columns), Column("short", String)],
        )
        self.create_table(
            "groups",
            [
                *copy.deepcopy(_base_columns),
                Column("divisionid", String),
                Column("classid", String),
                Column("entireclass", Boolean),
            ],
        )
        self.create_table(
            "teachers",
            [*copy.deepcopy(_base_columns)],
        )
        self.create_table(
            "periods",
            [
                Column("id", UUID, primary_key=True),
                Column("name", String),
                Column("start", Time),
                Column("end", Time),
            ],
        )
        self.create_table(
            "classrooms",
            [*copy.deepcopy(_base_columns), Column("short", String)],
        )

        self.create_table(
            "divisions",
            [
                Column("id", UUID, primary_key=True),
                Column("edu_id", String),
                Column("groupids", MutableList.as_mutable(PickleType)),
            ],
        )

        self.create_table(
            "lessons",
            [
                Column("id", UUID, primary_key=True),
                Column("edu_id", String),
                Column("groupids", MutableList.as_mutable(PickleType)),
                Column("subjectid", MutableList.as_mutable(PickleType)),
                Column("teacherids", MutableList.as_mutable(PickleType)),
                Column("periodid", Integer),
                Column("duration", Integer),
            ],
        )

        self.logger.info("Created all tables")

    # TODO: Make this work lol
    def update_timetable(self, timetable: Timetable):
        # check if tables exist
        self.metadata.reflect(self.engine)
        tables = self.metadata.tables.keys()
        if len(tables) == 0:
            self.create_tables()
        elif config.get("db.drop_tables"):
            self.logger.warning(
                "Dropping all tables due to config setting db.drop_tables"
            )
            self.drop_table("classes")
            self.drop_table("groups")
            self.drop_table("teachers")
            self.drop_table("periods")
            self.drop_table("classrooms")
            self.drop_table("lessons")
            self.drop_table("divisions")
            self.logger.info("Dropped all tables")
            self.create_tables()
        else:
            self.logger.debug("All tables already exist")

        # Insert data
        self.insert(
            "classes",
            [
                {
                    "id": class_.id,
                    "edu_id": class_.edu_id,
                    "name": class_.name,
                    "short": class_.short,
                }
                for class_ in timetable.classes
            ],
        )

        self.insert(
            "groups",
            [
                {
                    "id": group.id,
                    "edu_id": group.edu_id,
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
                {"id": teacher.id, "edu_id": teacher.edu_id, "name": teacher.name}
                for teacher in timetable.teachers
            ],
        )

        self.insert(
            "periods",
            [
                {
                    "id": period.id,
                    "name": period.name,
                    "start": period.start,
                    "end": period.end,
                }
                for period in timetable.periods
            ],
        )

        self.insert(
            "classrooms",
            [
                {
                    "id": classroom.id,
                    "edu_id": classroom.edu_id,
                    "name": classroom.name,
                    "short": classroom.short,
                }
                for classroom in timetable.classrooms
            ],
        )

        self.insert(
            "divisions",
            [
                {
                    "id": division.id,
                    "edu_id": division.edu_id,
                    "groupids": division.groupids,
                }
                for division in timetable.divisions
            ],
        )

        self.insert(
            "lessons",
            [
                {
                    "id": lesson.id,
                    "edu_id": lesson.edu_id,
                    "groupids": lesson.groupids,
                    "subjectid": lesson.subjectid,
                    "teacherids": lesson.teacherids,
                    "periodid": lesson.periodid,
                    "duration": lesson.duration,
                }
                for lesson in timetable.lessons
            ],
        )

        self.connection.commit()

    def update_relationships(self):
        pass
