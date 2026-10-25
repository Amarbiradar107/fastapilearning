from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    print("Connecting to database")
    try:
        yield {"connected": True}
    finally:
        print("Closing database connection")

@app.get("/users")
def read_users(db : dict = Depends(get_db)):
    print("application started")
    return {"message": "List of tasks", "db": db}
# from fastapi import FastAPI, Depends
#
# app = FastAPI()
#
#
# def get_resource():
#     print("1. Setting up resource")
#
#     try:
#         yield {"message": "Resource is ready"}
#     finally:
#         print("3. Cleaning up resource")
#
#
# @app.get("/demo")
# def demo(resource: dict = Depends(get_resource)):
#     print("2. Endpoint is running")
#
#     return {
#         "message": "Request completed",
#         "resource": resource
#     }
