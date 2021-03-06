import logging
from datetime import datetime

from peewee import *
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict

from flywheel.settings import DB_URL
from flywheel.consts import Market

logger = logging.getLogger(__name__)
db = connect(DB_URL)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.now, index=True)

    class Meta:
        database = db
        legacy_table_names = False
        if isinstance(db, MySQLDatabase):
            table_settings = ['ENGINE=InnoDB', 'DEFAULT CHARSET=utf8']

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        with db.atomic() as transaction:
            try:
                return super(BaseModel, self).save(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                transaction.rollback()
                raise

    def to_dict(self):
        ins = model_to_dict(self)
        ins['created_at'] = datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S')
        ins['updated_at'] = datetime.strftime(self.updated_at, '%Y-%m-%d %H:%M:%S')
        return ins

    @classmethod
    def all(cls, *fields, **filters):
        s = cls.select(*fields)
        for field, value in filters.items():
            s = s.where(getattr(cls, field) == value)
        return list(s)


class Stock(BaseModel):
    market = CharField(null=False, default=Market.UNKNOWN)
    ticker = CharField(null=False, default='', index=True)

    class Meta:
        indexes = ((('market', 'ticker'), True),)

    @classmethod
    def get_by_ticker(cls, ticker):
        return cls.get_or_none(ticker=ticker)


class StockPrice(BaseModel):
    stock_id = IntegerField(null=False, default=0)
    date = DateField(null=False, default=datetime.now().date())
    open = FloatField(null=False, default=0.00)
    high = FloatField(null=False, default=0.00)
    low = FloatField(null=False, default=0.00)
    close = FloatField(null=False, default=0.00)
    volume = IntegerField(null=False, default=0)
    dividends = IntegerField(null=False, default=0)
    stock_splits = IntegerField(null=False, default=0)

    class Meta:
        indexes = ((('stock_id', 'date'), True),)
