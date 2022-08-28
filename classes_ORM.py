from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

engine = create_engine('sqlite:///hh_api_data.db', echo=True)
Base = declarative_base()
# Создание сессии
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    pharm_group = Column(String)
    manufacturer = Column(String)
    form = Column(String)
    indications = Column(String)
    doses = Column(String)
    contraindications = Column(String)

    def __init__(self, name, pharm_group, manufacturer, form, indications, doses, contraindications):
        self.name = name
        self.pharm_group = pharm_group
        self.manufacturer = manufacturer
        self.form = form
        self.indications = indications
        self.doses = doses
        self.contraindications= contraindications

    def __str__(self):
        return f'Информация по препарату {self.name} успешно добавлена'
