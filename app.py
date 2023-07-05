from flask import Flask, render_template, request, redirect, url_for, session
import random, string
import db

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k= 256))
    
    
# レイアウトサンプル
@app.route('/')
def loginTop():
    return render_template('login.html')
    
@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail')
    pw = request.form.get('pw')
    
    user_id, name = db.select_user(mail)  # ユーザー情報を取得
    
    if db.login(mail,pw):
        
        # ログイン成功時にセッションにユーザー情報を登録
        session['user_id'] = user_id  # user_idはログインしたユーザーのID
        session['name'] = name  # nameはログインしたユーザーの名前
        return redirect(url_for('Top'))
    else :
        error = 'ログインに失敗しました。'
        return render_template('login.html', error=error)

#TOPMENU
@app.route('/Top', methods = ['GET'])
def Top():
    return render_template('index.html')


#user登録
@app.route('/RegUser_form')
def RegUser_form():
    return render_template('RegUser_form.html')

@app.route('/RegUser_conf', methods = ['POST'])
def RegUser_conf():
    mail = request.form.get('mail')
    pw = request.form.get('pw')
    name = request.form.get('name')
    gender = request.form.get('gender')
    year_B = request.form.get('year_B')
    month_B = request.form.get('month_B')
    day_B = request.form.get('day_B')
    birthday = year_B + '/' + month_B + '/'+ day_B
    return render_template('RegUser_conf.html',mail=mail, pw=pw, name=name, gender=gender, birthday=birthday)

@app.route('/RegUser_exe' , methods = ['POST'])
def RegUser_exe():
    name = request.form.get('name')
    gender = request.form.get('gender')
    birthday = request.form.get('birthday')
    mail = request.form.get('mail')
    pw = request.form.get('pw')
    print(name)
    print(birthday)
    print(gender)
    print(pw)
    print(mail)

    count = db.insert_user(name,gender,birthday,mail,pw)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('login.html' ,msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('Reguser_form.html', error=error)


@app.route('/list')
def sample_list():
    return render_template('list.html')


#予約登録
@app.route('/register')
def sample_register():
    return render_template('register.html')

@app.route('/RegReserve_conf', methods = ['POST'])
def RegReserve_conf():
    year = request.form.get("year")
    month = request.form.get("month")
    day = request.form.get("day")
    time = request.form.get("time")
    symptoms = request.form.get("symptoms")
    remarks = request.form.get("remarks")
    return render_template("RegReserve_conf.html", year=year,month=month,day=day,time=time,symptoms=symptoms,remarks=remarks)



@app.route('/RegReserve_exe', methods = ['POST'])
def RegReserve_exe():
    user_id = session.get('user_id')  # Retrieve the user ID from the session
    name = session.get('name')  # Retrieve the user name from the session
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    time = request.form.get('time')
    symptoms = request.form.get('symptoms')
    remarks = request.form.get('remarks')
    print(user_id)
    print(name)
    
    count = db.register_reserve(user_id,name,year,month,day,time, symptoms, remarks)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('register.html' ,msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    
if __name__ == "__main__":
    app.run(debug=True)