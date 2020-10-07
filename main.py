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

        #开始回复
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        if "sql" in form.keys():
            data = json.dumps(sqlMana.Search(form["sql"].value))
            out.write(data)
        elif "user" in form.keys():
            user = form["user"].value
            passwd = form["passwd"].value
            print(user)
            print(passwd)
            if str(user) == "joklr" and str(passwd) == "123":
                out.write('login succeed')
            else:
                out.write('login fail')

        # out.write('Client: {}\n'.format(self.client_address))
        # out.write('User-agent: {}\n'.format(
        #     self.headers['user-agent']))
        # out.write('Path: {}\n'.format(self.path))
        # out.write('Form data:\n')

        # for field in form.keys():
        #     field_item = form[field]
        #     if field_item.filename:
        #         file_data = field_item.file.read()
        #         file_len = len(file_data)
        #         del file_data
        #         out.write(
        #             '\tUploaded {} as {!r} ({} bytes)\n'.format(
        #                 field, field_item.filename, file_len)
        #         )
        #     else:
        #         out.write('\t{}={}\n'.format(
        #             field, form[field].value))

        # 将编码 wrapper 到底层缓冲的连接断开，
        # 使得将 wrapper 删除时，
        # 并不关闭仍被服务器使用 socket 。
        out.detach()


if __name__ == '__main__':
    from http.server import HTTPServer

    server = HTTPServer(('localhost', 8080), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
