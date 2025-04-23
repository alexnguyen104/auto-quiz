Hướng dẫn sử dụng:
-----
<br/>
0. Lấy source code về máy

‼ Nên dùng python phiên bản 3.9.x trở xuống

```
git clone https://github.com/alexnguyen104/auto-quiz.git
cd auto-quiz/
```
- Hoặc tải file zip rồi giải nén
<br/>
1. Tạo môi trường ảo (Virtual Environment)

- Tải thư viện <b>virtualenv</b>

```
// MAC OS
pip3 install virtualenv

// WINDOWS
pip install virtualenv
```

- Khởi tạo môi trường ảo với tên tùy thích (trong ví dụ này là "env")
```
// MAC OS
python3 -m venv env

// WINDOWS
python -m venv env
```
- Khởi động môi trường ảo
```
// MAC OS
source env/bin/activate

// WINDOWS (chạy trong cmd)
env\Scripts\activate.bat

hoặc

env\Scripts\activate
```
‼ Nếu <b>cần tắt</b> môi trường ảo thì chạy
```
deactivate
```
<br/>
2. Tạo file <b>.env</b>

- Cấu trúc file <b>.env</b>:
```
OPENAI-API-KEY=...
```
- Tự sử dụng OPENAI API KEY cá nhân hoặc liên hệ với nhóm để lấy nội dung file <b>.env</b> (vì lý do bảo mật nên không đưa lên github được)

<br/>
3. Tải thư viện cần thiết:

```
// MAC OS
pip3 install -r requirements.txt

// WINDOWS
pip install -r requirements.txt
```

4. Chạy file server.py:
```
// MAC OS
python3 server.py

// WINDOWS
python server.py
```
