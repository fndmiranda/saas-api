from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, inspect


class ModelMixin(object):
    id = Column(Integer, primary_key=True)

    def to_dict(self):
        """Return a dictionary representation of this model."""
        data = {}

        for column in inspect(self).mapper.column_attrs:
            data[column.key] = getattr(self, column.key)

        return data


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
