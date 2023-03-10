from fastapi import FastAPI,HTTPException
from model import Count
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


session = SessionLocal()
app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


default_count = 0
def is_uuid_exist(uuid : str):
    que = session.query(Count).filter(Count.uuid == uuid)
    if que == {}:
        return False,que
    return True,que


@app.get('/')
def home():
    return {'msg' : 'Hello World'}

@app.post('/create/{uuid}')
def create_count(uuid : str) -> dict:
    que = session.query(Count.uuid).filter(Count.uuid == uuid).all()
    try:
        if uuid in que :
            raise HTTPException(status_code=404, detail='UUID already exists')
        else:
            count = Count(uuid=uuid,count=default_count)
            session.add(count)
            session.commit()
        return {'uuid': uuid, 'count' : default_count}
    except:
        return {'error':'unidentified error', 'server_status': 'working'}
    
@app.put('/update/{uuid}')
def update_count(uuid : str):
    que = session.query(Count.uuid).filter(Count.uuid == uuid).first()
    try:
        if uuid in que:
            session.query(Count).filter(Count.uuid == uuid).update({Count.count: Count.count + 1},synchronize_session=False)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail='UUID does not exists')
        return {'uuid' : uuid , 'status' : 'updated'}
    except:
        return {'error':'unidentified error', 'server_status': 'working'}


@app.delete('/delete/{uuid}')
def delete_count(uuid : str):
    que = session.query(Count.uuid).filter(Count.uuid == uuid).first()
    try:
        if uuid in que:
            session.query(Count).filter(Count.uuid == uuid).delete(synchronize_session=False)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail='UUID does not exists')
        return {'uuid' : uuid, 'status' : 'updated' }
    except:
        return {'error':'unidentified error', 'server_status': 'working'}


@app.get('/all')
def query():
    try:
        q = session.query(Count).all()
        return {'count' : q}
    except:
        return {'error':'unidentified error', 'server_status': 'working'}

@app.get('/get/{uuid}')
def get_count(uuid:str):
    try:
        q = session.query(Count).filter(Count.uuid == uuid).all()
        if q == []:
            count = Count(uuid=uuid,count=default_count)
            session.add(count)
            session.commit()
            return {'uuid': uuid, 'count' : default_count}
            # return  HTTPException(status_code=404, detail='UUID does not exists')
        else:
            return {'uuid' : uuid, 'count' : q[0].count}
            
    except:
        return {'error':'unidentified error', 'server_status': 'working'}

