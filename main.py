import cgi
from http.server import BaseHTTPRequestHandler
import io
import sqlMana
import json


class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 分析提交的表单数据
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # 开始回复
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')

        # 解决跨域问题
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        # 分析表单返回
        # 登录

        data = None

        if "user" in form.keys():
            auth = sqlMana.login(str(form["user"].value), str(form["passwd"].value))
            data = str(auth)
        elif "sqltype" in form.keys():
            sqltype = str(form["sqltype"].value)
            if sqltype == "1":
                data = json.dumps(sqlMana.search_id(str(form["id"].value)))
            elif sqltype == "2":
                data = json.dumps(sqlMana.search_name(str(form["db"].value)))
            elif sqltype == "3":
                sqlMana.insert_course(
                    str(form["id"].value),
                    str(form["name"].value),
                    str(form["hour"].value),
                    str(form["dept"].value),
                    str(form["term"].value),
                    str(form["sum"].value),
                )
                data = True
            elif sqltype == "4":
                if "id" in form.keys():
                    sqlMana.delete_course(str(form["id"].value))
                else:
                    sqlMana.delete_course(str(form["name"].value))
                data = True
            elif sqltype == "5":
                if "cid" in form.keys():
                    sqlMana.insert_exp(
                        eid=str(form["eid"].value),
                        ename=str(form["ename"].value),
                        id=str(form["id"].value),
                        caty=str(form["caty"].value),
                        hard=str(form["hard"].value),
                        hour=str(form["hour"].value),
                        cid=str(form["cid"].value)
                    )
                elif "cname" in form.keys():
                    sqlMana.insert_exp(
                        eid=str(form["eid"].value),
                        ename=str(form["ename"].value),
                        id=str(form["id"].value),
                        caty=str(form["caty"].value),
                        hard=str(form["hard"].value),
                        hour=str(form["hour"].value),
                        cname=str(form["cname"].value)
                    )
                data = True
            elif sqltype == "6":
                if "id" in form.keys():
                    sqlMana.delete_exp(str(form["id"].value))
                elif "name" in form.keys():
                    sqlMana.delete_exp(str(form["name"].value))
            elif sqltype == "7":
                data = json.dumps(sqlMana.search_room(str(form["room"].value)))
            elif sqltype == "8":
                data = json.dumps(sqlMana.search_stu(
                    str(form["na"].value),
                    str(form["teac"].value),
                    str(form["cla"].value)
                ))
            elif sqltype == "9":
                sqlMana.update_grade(
                    str(form["id"].value),
                    str(form["name"].value),
                    str(form["gr"].value)
                )

        print(data)
        out.write(data)

        # 将编码 wrapper 到底层缓冲的连接断开，
        # 使得将 wrapper 删除时，
        # 并不关闭仍被服务器使用 socket 。
        out.detach()


if __name__ == '__main__':
    from http.server import HTTPServer

    server = HTTPServer(("0.0.0.0", 8080), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
