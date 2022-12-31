from flask import Flask, request, jsonify
from sqlalchemy import Column, String, Integer, TEXT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# 连接数据库
Base = declarative_base()
engine = create_engine("mysql+pymysql://root:root@localhost:3306/text")
Session = sessionmaker(bind=engine)
session = Session()


# 创造表单，以及其中的各项
class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(255), default=None, nullable=True, comment="标题")
    content = Column(TEXT, default=None, nullable=True, comment="内容")
    done = Column(String(10), default=0, nullable=False, comment="未完成")
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=True)

    # 查询的函数
    def __repr__(self):
        ID = self.id
        TITLE = self.title
        CONTENT = self.content
        DONE = self.done
        START = self.start
        END = self.end
        return f"Data: id: {ID}, title:{TITLE}, content: {CONTENT}, done: {DONE}, start:{START},end:{END}"


# 新增
@app.route("/increase", methods=["POST"])
def increase():
    # 从json中获取数据
    my_json = request.get_json()
    ID = my_json.get("id")
    TITLE = my_json.get("title")
    CONTENT = my_json.get("content")
    DONE = my_json.get("done")
    START = my_json.get("start")
    END = my_json.get("end")
    # 尝试新增数据，否则报错
    try:
        NewUser = Data(id=ID, title=TITLE, content=CONTENT, done=DONE, start=START, end=END)
        session.add(NewUser)
        session.commit()
    except Exception as e:
        print(e)
        return "输入的数据有问题，请检查后再输入"
    return jsonify(id=ID)


# 查询所有的数据项
@app.route("/look/all")
def look_all():
    payload = []
    i = 0
    # 得到所有的数据项
    try:
        query_result = session.query(Data).all()
        for result in query_result:
            print(f"查询结果为: {result}")
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            # 每五个数据一页，每个数据登入完后加一
            payload.append(conTent)
    except Exception as e:
        print(e)
    return jsonify(payload)


# 查询所有完成事项
@app.route("/look/all_done")
def look_all_done():
    payload = []
    i = 0
    query_result = session.query(Data).filter(Data.done == '已完成')
    for result in query_result:
        print(f"查询结果为: {result}")
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
        i += 1
        payload.append(conTent)
    return jsonify(payload)


# 查询所有未完成事项
@app.route("/look/all_no_done")
def look_all_no_done():
    payload = []
    i = 0
    query_result = session.query(Data).filter(Data.done == '未完成')
    for result in query_result:
        print(f"查询结果为: {result}")
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
        i += 1
        payload.append(conTent)
    return jsonify(payload)


# 按id查询
@app.route("/look/id", methods=["POST", "GET"])
def look_id():
    payload = []
    my_json = request.get_json()
    ID = my_json.get("id")
    if ID is None:
        return "请输入想要查询的id"
    query_result = session.query(Data).filter(Data.id == ID)
    for result in query_result:
        print(f"查询结果为: {result}")
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
    return jsonify(payload)


# 按关键字查询
@app.route("/look/keyword", methods=["POST", "GET"])
def look_keyword():
    payload = []
    i = 0
    my_json = request.get_json()
    KEYWORD = my_json.get("keyword")
    ID = my_json.get("id")
    TITLE = my_json.get("title")
    CONTENT = my_json.get("content")
    DONE = my_json.get("done")
    START = my_json.get("start")
    END = my_json.get("end")

    if KEYWORD is None:
        return "请输入想要查询的关键词"

    if KEYWORD == "id":
        if ID is None:
            return "请输入想要查询的ID"
        query_result = session.query(Data).filter(Data.id == ID)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)

    if KEYWORD == "content":
        if CONTENT is None:
            return "请输入想要查询的CONTENT"
        query_result = session.query(Data).filter(Data.content == CONTENT)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)

    if KEYWORD == "start":
        if START is None:
            return "请输入想要查询的start"
        query_result = session.query(Data).filter(Data.start == START)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)

    if KEYWORD == "title":
        if TITLE is None:
            return "请输入想要查询的title"
        query_result = session.query(Data).filter(Data.title == TITLE)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)

    if KEYWORD == "done":
        if DONE is None:
            return "请输入想要查询的DONE"
        query_result = session.query(Data).filter(Data.done == DONE)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)

    if KEYWORD == "end":
        if END is None:
            return "请输入想要查询的end"
        query_result = session.query(Data).filter(Data.end == END)
        for result in query_result:
            conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                       'start': result.start, 'end': result.end, 'page': int(i / 5) + 1}
            i += 1
            payload.append(conTent)
        return jsonify(payload)


# 删除所有数据
@app.route("/delete/all")
def delete_all():
    payload = []
    results = session.query(Data).all()
    print(results)
    for result in results:
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
    return jsonify(payload)


# 删除所有已经完成的事项
@app.route("/delete/all_done")
def delete_all_done():
    payload = []
    results = session.query(Data).filter(Data.done == "已完成")
    print(results)
    for result in results:
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
    return jsonify(payload)


# 删除所有未完成事项
@app.route("/delete/all_no_done")
def delete_all_no_done():
    payload = []
    results = session.query(Data).filter(Data.done == "未完成")
    print(results)
    for result in results:
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
    return jsonify(payload)


# 删除一条事项,若输入的关键词是id就删除指定的一条，若是其他的就删除第一条
@app.route("/delete/one")
def delete_all_one():
    payload = []
    my_json = request.get_json()
    KEYWORD = my_json.get("keyword")
    ID = my_json.get("id")
    TITLE = my_json.get("title")
    CONTENT = my_json.get("content")
    DONE = my_json.get("done")
    START = my_json.get("start")
    END = my_json.get("end")

    if KEYWORD is None:
        return "请输入想要查询的关键词"

    if KEYWORD == "id":
        if ID is None:
            return "请输入想要查询的ID"
        result = session.query(Data).filter(Data.id == ID).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
        return jsonify(payload)

    if KEYWORD == "content":
        if CONTENT is None:
            return "请输入想要查询的CONTENT"
        result = session.query(Data).filter(Data.content == CONTENT).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
        return jsonify(payload)

    if KEYWORD == "start":
        if START is None:
            return "请输入想要查询的start"
        result = session.query(Data).filter(Data.start == START).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
        return jsonify(payload)

    if KEYWORD == "title":
        if TITLE is None:
            return "请输入想要查询的title"
        result = session.query(Data).filter(Data.title == TITLE).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
        return jsonify(payload)

    if KEYWORD == "done":
        if DONE is None:
            return "请输入想要查询的DONE"
        result = session.query(Data).filter(Data.done == DONE).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
        return jsonify(payload)

    if KEYWORD == "end":
        if END is None:
            return "请输入想要查询的end"
        result = session.query(Data).filter(Data.end == END).first()
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        session.delete(result)
        session.commit()
    return jsonify(payload)


@app.route("/update/all_done", methods=["POST"])
def update_all_done():
    payload = []
    query_result = session.query(Data).filter(Data.done == "已完成")
    for result in query_result:
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        result.done = "未完成"
        session.add(result)
        session.commit()
    return jsonify(payload)


@app.route("/update/all_no_done", methods=["POST"])
def update_all_no_done():
    payload = []
    query_result = session.query(Data).filter(Data.done == "未完成")
    for result in query_result:
        conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
                   'start': result.start, 'end': result.end}
        payload.append(conTent)
        result.done = "已完成"
        session.add(result)
        session.commit()
    return jsonify(payload)


@app.route("/update/one_no_done", methods=["POST"])
def update_one_no_done():
    payload = []
    my_json = request.get_json()
    ID = my_json.get("id")
    END = my_json.get("end")
    if ID is None:
        return "请输入合法ID"
    result = session.query(Data).filter(Data.id == ID).first()
    result.done = "已完成"
    result.end = END
    conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
               'start': result.start, 'end': result.end}
    payload.append(conTent)
    session.add(result)
    session.commit()
    return jsonify(payload)


@app.route("/update/one_done", methods=["POST"])
def update_one_done():
    payload = []
    my_json = request.get_json()
    ID = my_json.get("id")
    if ID is None:
        return "请输入合法ID"
    result = session.query(Data).filter(Data.id == ID).first()
    result.done = "未完成"
    result.end = None
    conTent = {'id': result.id, 'title': result.title, 'content': result.content, 'done': result.done,
               'start': result.start, 'end': result.end}
    payload.append(conTent)
    session.add(result)
    session.commit()
    return jsonify(payload)


app.run(host="0.0.0.0")
