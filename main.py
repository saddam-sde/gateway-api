import json
from sqlalchemy import create_engine, text, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import String, JSON
from sqlalchemy.ext.declarative import declarative_base

# Postgres DB connection
username = 'saddam'
password = 'j3TBUcNqQQIQQ46NaDxB'
host = 'bakery.cfajylwbigbf.ap-south-1.rds.amazonaws.com'
database = 'postgres'
port = '5432'
pg_conn_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
# connection_string = "postgresql+psycopg2://username:password@host:port/database_name"

pg_engine = create_engine(pg_conn_string)
Session = sessionmaker(bind=pg_engine)
session = Session()

Base = declarative_base()


class BakeryProduct(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    item = Column(String)
    date = Column(Date)


# Read records
def read_records():
    records = session.query(BakeryProduct).all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'item': record.item,
            'date': record.date.strftime('%Y-%m-%d')
        })
    return result


def create_record(item, date):
    new_record = BakeryProduct(item=item, date=date)
    session.add(new_record)
    session.commit()


# Update a record by ID
def update_record(record_id, item, date):
    record = session.query(BakeryProduct).get(record_id)
    if record:
        record.item = item
        record.date = date
        session.commit()
        return True
    else:
        return False


# Delete a record by ID
def delete_record(record_id):
    record = session.query(BakeryProduct).get(record_id)
    if record:
        session.delete(record)
        session.commit()
        return True
    else:
        return False


# Lambda function handler
def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'GET':
        records = read_records()
        return {
            'statusCode': 200,
            'body': json.dumps(records)
        }
    elif http_method == 'POST':
        json_tmp = json.dumps(event['body'])
        body = json.loads(json_tmp)
        item = body['item']
        date = body['date']
        create_record(item, date)
        return {
            'statusCode': 201,
            'body': 'Record created'
        }
    elif http_method == 'PUT':
        data = json.loads(event['body'])
        record_id = data['id']
        item = data['item']
        date = data['date']
        success = update_record(record_id, item, date)
        if success:
            return {
                'statusCode': 200,
                'body': 'Record updated'
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Record not found'
            }
    elif http_method == 'DELETE':
        data = json.loads(event['body'])
        record_id = data['id']
        success = delete_record(record_id)
        if success:
            return {
                'statusCode': 200,
                'body': 'Record deleted'
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Record not found'
            }
