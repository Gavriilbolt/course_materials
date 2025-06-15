<h2 style="text-align:center;"><span style="color:#a03881;">Часть 2:</span> Хеширование паролей в базе данных&nbsp;</h2>

<h3><span style="color:#a03881;">🎯 Цель:</span></h3>

<p>Устранить риск хранения паролей в открытом виде. Все пароли пользователей должны быть безопасно захэшированы при помощи одного из современных алгоритмов (bcrypt или argon2).</p>

<h3><span style="color:#a03881;">📌 Этап 1: Подключение к базе данных PostgreSQL</span></h3>

<p>Откройте терминал (или PowerShell, если вы работаете в Windows) и выполните команду подключения к базе данных:</p>

<pre><code>psql -h localhost -U bookvault -d bookvault_db -p 5432
</code></pre>

<ul>
	<li>
	<p><code>-h localhost</code> — адрес сервера базы данных</p>
	</li>
	<li>
	<p><code>-U bookvault</code> — имя пользователя</p>
	</li>
	<li>
	<p><code>-d bookvault_db</code> — имя базы данных</p>
	</li>
	<li>
	<p><code>-p 5432</code> — порт, на котором работает PostgreSQL</p>
	</li>
</ul>

<p>После запроса введите пароль для пользователя <code>bookvault</code>. <strong>Пароль&nbsp;<code>secret</code></strong></p>

<h3><span style="color:#a03881;">📌 Этап 2: Проверка хранения паролей</span></h3>

<p>Выполните SQL-запрос для просмотра таблицы пользователей:</p>

<pre><code>SELECT id, username, password FROM users;
</code></pre>

<p>Если вы видите пароли в открытом виде (например, <code>password123</code>), это небезопасно и требует исправления.</p>

<blockquote>
<p><strong>🔒 Примечание:</strong><br>
<strong>Шифрование</strong> — это способ превратить информацию в набор непонятных символов, чтобы никто посторонний не смог её прочитать. Только тот, у кого есть "ключ", сможет вернуть всё обратно.</p>

<p>В отличие от <strong>хеширования</strong>, шифрование можно "расшифровать", а хеш — <strong>нельзя вернуть в исходный пароль</strong>.</p>

<p><strong>Хеширование</strong> — это как односторонний блендер:<br>
ты кидаешь туда пароль, он перемалывает его в "кашу" — набор символов вроде <code>"$2b$12$abc...xyz"</code>.<br>
🔁 <strong>Вернуть обратно пароль уже нельзя.</strong></p>

<h4>Но как же тогда система проверяет пароль при входе?</h4>

<p>Пример:</p>

<ol>
	<li>
	<p>Пользователь вводит пароль: <code>mySecret123</code></p>
	</li>
	<li>
	<p>Система <strong>заново хеширует</strong> этот пароль → получается, например, <code>"$2b$12$abc..."</code></p>
	</li>
	<li>
	<p>Система <strong>сравнивает</strong> этот новый хеш с тем, что хранится в базе.</p>

	<ul>
		<li>
		<p>Если <strong>совпали</strong> — пароль правильный.</p>
		</li>
		<li>
		<p>Если <strong>разные</strong> — доступ не даётся.</p>
		</li>
	</ul>
	</li>
</ol>
</blockquote>

<p>&nbsp;</p>

<h3><span style="color:#a03881;">📌 Этап 3: Хеширование паролей в <code>seed.py</code></span></h3>

<ol>
	<li>
	<p>Откройте файл <code>app/seed.py</code></p>
	</li>
	<li>
	<p>Импортируйте модуль <code>bcrypt</code>:</p>
	</li>
</ol>

<pre><code>import bcrypt
</code></pre>

<ol>
	<li>
	<p>При создании пользователя, замените строку:</p>
	</li>
</ol>

<pre><code>user = User(username='alice', password='password')
</code></pre>

<p>на:</p>

<pre><code>hashed = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
user = User(username='alice', password=hashed.decode('utf-8'))
</code></pre>

<ol>
	<li>
	<p>Убедитесь, что все пользователи создаются с захэшированными паролями.</p>
	</li>
</ol>

<h3><span style="color:#a03881;">📌 Этап 4: Обновление модели пользователя</span></h3>

<p>Откройте файл <code>models.py</code> и удостоверьтесь, что поле <code>password</code> по-прежнему имеет достаточно длины (например, <code>String(128)</code> или больше).</p>

<h3><span style="color:#a03881;">📌 Этап 5: Сравнение хеша при логине</span></h3>

<p>В файле обработки логина (<code>admin/views.py</code>), замените проверку пароля:</p>

<p><strong>Было:</strong></p>

<pre><code>if user and user.password == input_password:
</code></pre>

<p><strong>Стало:</strong></p>

<pre><code>import bcrypt

if user and bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
</code></pre>

<h3><span style="color:#a03881;">✅ Результат:</span></h3>

<p>Теперь пароли в базе данных хранятся в виде хеша. Даже если злоумышленник получит доступ к таблице <code>users</code>, он не узнает настоящие пароли.</p>

<h2>&nbsp;</h2>