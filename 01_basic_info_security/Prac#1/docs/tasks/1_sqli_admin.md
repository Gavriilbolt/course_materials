<h2 style="text-align:center"><span style="color:#a03881">Часть 1:</span> Дамп базы через SQL-инъекцию&nbsp;</h2>

<p><strong>Цель:</strong> понять механизмы SQL-инъекции и научиться с помощью неё выгружать (дампить) содержимое базы данных.</p>

<p><u>SQL-инъекция </u>&mdash; это приём, при котором злоумышленник &laquo;вклинивает&raquo; свой SQL-код в параметры приложения. Если сервер формирует запрос путём конкатенации строк без должной фильтрации или использования подготовленных выражений, то такие &laquo;payload&raquo; могут:</p>

<ul>
	<li>обойти проверки аутентификации (<code>&#39; OR &#39;1&#39;=&#39;1</code>),</li>
	<li>получить структуру базы (через <code>information_schema</code>),</li>
	<li>выгрузить все таблицы и их данные (<code>UNION SELECT</code>).</li>
</ul>

<h3><span style="color:#a03881">🔍 Шаг 1. Перейдите на страницу входа администратора</span></h3>

<ul>
	<li>
	<p>Запустите приложение (через Docker или локально).</p>
	</li>
	<li>
	<p>Откройте браузер и перейдите по адресу:<br />
	<strong><a href="http://localhost:5000/admin/login" rel="noopener noreferrer nofollow">http://localhost:5000/admin/login</a></strong></p>
	</li>
</ul>

<p>Вы увидите простую форму входа, запрашивающую имя пользователя и пароль.</p>

<h3><span style="color:#a03881">🛠️ Шаг 2. Проанализируйте обработку данных формы</span></h3>

<p>Откройте файл <code>app/admin/views.py</code> и найдите обработчик маршрута <code>/admin/login</code>:</p>

<pre>
<code>@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = db.session.execute(sql).fetchone()

        if result:
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))

    return render_template('admin/login.html')
</code></pre>

<h4>🧨 Уязвимость:</h4>

<p>Обратите внимание &mdash; данные из формы напрямую подставляются в SQL-запрос <strong>без экранирования</strong>. Это делает систему уязвимой к <strong>SQL-инъекциям</strong>.</p>

<blockquote>
<p>Остановитесь и хорошо подумайте: какое изменение в SQL запросе позволит пользователю войти без пароля?</p>
</blockquote>

<p>&nbsp;</p>

<h3>💣 Шаг 3. Обход авторизации с помощью SQL-инъекции</h3>

<p>В поле <strong>Имя пользователя</strong> введите:</p>

<pre>
<code>' OR 1=1 --
</code></pre>

<p>Пароль может быть любым (например, <code>abc</code>), так как он будет проигнорирован частью <code>--</code> (SQL-комментарий).</p>

<p style="text-align:center"><img alt="" height="352" name="image.png" src="https://ucarecdn.com/6a599d0d-ce21-41bc-bf9c-4141c38a3116/" width="519" /></p>

<p style="text-align:center"><em>Ввод данных на странице входа в админ-панель</em></p>

<p>Запрос, который в итоге выполнится:</p>

<pre>
<code>SELECT * FROM users WHERE username = '' OR 1=1 -- ' AND password = 'abc'
</code></pre>

<p>Условие <code>1=1</code> всегда истинно, а остальное после <code>--</code> игнорируется. Таким образом, будет возвращена <strong>первая запись</strong> из таблицы пользователей.</p>

<h3>📥 Шаг 4. Получите дамп всех пользователей</h3>

<p>После успешного входа вы попадёте на <code>/admin</code> &mdash; административную панель.</p>

<p>Посмотрите код маршрута <code>admin/dashboard</code> в <code>app/admin/views.py</code>. Вероятнее всего, он содержит что-то вроде:</p>

<pre>
<code>@admin_bp.route('/')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin.login'))

    users = db.session.execute("SELECT * FROM users").fetchall()
    return render_template('admin/dashboard.html', users=users)
</code></pre>

<p>Теперь вы видите <strong>весь список пользователей</strong>, включая их логины и (пока ещё открытые) пароли.</p>

<h3>✅ Результат выполнения:</h3>

<ul>
	<li>
	<p>Вы успешно вошли в админку, не зная пароля.</p>
	</li>
	<li>
	<p>Получили содержимое таблицы <code>users</code>.</p>
	</li>
	<li>
	<p>Подтвердили наличие <strong>SQL-инъекции</strong> в форме логина.</p>
	</li>
</ul>
