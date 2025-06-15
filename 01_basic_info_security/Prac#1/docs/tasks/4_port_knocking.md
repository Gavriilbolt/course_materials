<h2 style="text-align:center;"><span style="color:#a03881;">Часть 4: </span>Port Knocking&nbsp;для SSH-доступа</h2>

<h3><span style="color:#a03881;">🎯 Цель:</span></h3>

<p>Настроить доступ к <strong>SSH</strong> через <strong>port knocking</strong> — технику скрытой аутентификации, при которой доступ к порту (в нашем случае <code>22/tcp</code>) открывается <strong>только после правильной последовательности "стуков"</strong> в другие порты.</p>

<ul>
	<li>
	<p><strong>SSH (Secure Shell)</strong> — безопасный способ удалённого входа на сервер через сеть.</p>
	</li>
	<li>
	<p><strong>Порт</strong> — это как "дверь" в сервер, через которую заходят разные сервисы. SSH по умолчанию использует <strong>порт 22</strong>.</p>
	</li>
	<li>
	<p><strong>Port knocking</strong> — метод, при котором "дверь" остаётся закрыта, пока ты не постучишь в другие "двери" в правильной последовательности. Это защищает от сканеров и злоумышленников.</p>
	</li>
</ul>

<h2><span style="color:#a03881;">🛠️ Этап 1: Настройка сервера (Ubuntu)</span></h2>

<blockquote>
<p>Эти шаги выполняются на виртуальной машине или удалённом сервере Linux (Ubuntu). Если это уже готовый контейнер — можно начать с включения <code>knockd</code>.</p>
</blockquote>

<h3>1. Установка knockd:</h3>

<pre><code>sudo apt update
sudo apt install knockd -y
</code></pre>

<h3>2. Настройка последовательности "стуков"</h3>

<p>Откройте конфигурационный файл:</p>

<pre><code>sudo nano /etc/knockd.conf
</code></pre>

<p>Пример конфигурации:</p>

<pre><code>[options]
    UseSyslog

[openSSH]
    sequence    = 7000,8000,9000
    seq_timeout = 15
    command     = /sbin/iptables -A INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

[closeSSH]
    sequence    = 9000,8000,7000
    seq_timeout = 15
    command     = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn
</code></pre>

<h3>3. Отключаем открытый порт SSH:</h3>

<pre><code>sudo iptables -A INPUT -p tcp --dport 22 -j DROP
</code></pre>

<h3>4. Включаем knockd:</h3>

<pre><code>sudo systemctl enable knockd
sudo systemctl start knockd
</code></pre>

<h2>&nbsp;</h2>

<h2><span style="color:#a03881;">🖥️ Этап 2: Настройка клиента Windows (исполняемый .bat-файл)</span></h2>

<h3><br>
Для стуков напишем простой&nbsp;<code>knock.bat</code>&nbsp;, который будет стучать в нужные порты.&nbsp;</h3>

<h3>Пример содержимого <code>knock.bat</code>:</h3>

<pre><code>@echo off
set IP=192.168.1.100

echo Port knocking to %IP%...
nmap -Pn -p 7000 --host-timeout 200ms %IP%
nmap -Pn -p 8000 --host-timeout 200ms %IP%
nmap -Pn -p 9000 --host-timeout 200ms %IP%

echo Done. Try connecting via SSH.
pause
</code></pre>

<blockquote>
<p>💡 Убедись, что <code>nmap</code> установлен и добавлен в PATH. Скачать можно с <a href="https://nmap.org/download.html" rel="noopener noreferrer nofollow">https://nmap.org/download.html</a></p>
</blockquote>

<h2><span style="color:#a03881;">✅ Этап 3: Проверка</span></h2>

<ol>
	<li>
	<p>Запусти <code>knock.bat</code> дважды:</p>

	<ul>
		<li>
		<p>Сначала для последовательности открытия (7000-8000-9000)</p>
		</li>
		<li>
		<p>Позже — обратную (9000-8000-7000) для закрытия</p>
		</li>
	</ul>
	</li>
	<li>
	<p>Сразу после стука подключись по SSH:</p>

	<pre><code>ssh user@192.168.1.100
</code></pre>

	<p>или через <a href="https://www.putty.org/" rel="noopener noreferrer nofollow">PuTTY </a>(если под Windows)&nbsp;</p>
	</li>
</ol>

<h2><span style="color:#a03881;">🧠 Почему это важно для ИБ</span></h2>

<p>Port knocking — <strong>дополнительный слой защиты</strong>, который:</p>

<ul>
	<li>
	<p>Делает SSH-порт <strong>невидимым для сканеров</strong></p>
	</li>
	<li>
	<p>Предотвращает атаки перебора паролей (brute-force)</p>
	</li>
	<li>
	<p>Прост в реализации, но эффективен в условиях ограниченных ресурсов</p>
	</li>
</ul>
<h2 style="text-align:center;">📘 Port Knocking + SSH-доступ к флагу</h2>

<h2><span style="color:#a03881;">🧩 Цель задания</span></h2>

<p>Вы должны:</p>

<ol>
	<li>
	<p>Выполнить <strong>Port Knocking</strong> на сервер, используя определённую последовательность портов (7000, 8000, 9000);</p>
	</li>
	<li>
	<p>Получить <strong>временный доступ по SSH</strong> (открытие порта 2222);</p>
	</li>
	<li>
	<p>Подключиться к контейнеру;</p>
	</li>
	<li>
	<p>Найти <strong>специальный флаг</strong> в файловой системе (<code>/var/secret/flag.txt</code>).</p>
	</li>
</ol>

<p>root пароль: <code>password</code></p>

<blockquote>
<p>Q: Куда стучаться?<br>
A: Учебный контейнер находится в контейнере knockd.</p>

<p>Q: Где взять контейнер?<br>
A: <strong>см. шаг 1.3.8</strong></p>
</blockquote>

<p>&nbsp;</p>

<h2><span style="color:#a03881;">💻 <code>knock.ps1</code> — PowerShell-скрипт для стука</span></h2>

<pre><code class="language-bash">$ports = @(7000,8000,9000)
foreach ($port in $ports) {
&nbsp; try {
&nbsp; &nbsp; $client = New-Object System.Net.Sockets.TcpClient
&nbsp; &nbsp; $client.Connect("localhost", $port)
&nbsp; &nbsp; $client.Close()
&nbsp; &nbsp; Start-Sleep -Milliseconds 500
&nbsp; } catch {}
}
Write-Host "Done. Try connecting via SSH (ssh root@localhost -p 2222)"</code></pre>

<h2>✅ <span style="color:#a03881;">Подсказка</span></h2>

<p>Для полной совместимости с Windows-батниками, лучше использовать <code>telnet</code> или <code>PowerShell TCPClient</code>, а не <code>nmap</code>, потому что он:</p>

<ul>
	<li>
	<p>не гарантирует SYN;</p>
	</li>
	<li>
	<p>может не работать без <code>WinPcap</code>/<code>Npcap</code>;</p>
	</li>
	<li>
	<p>в WSL/WSA или Windows-браузерах может быть ограничен.</p>
	</li>
</ul>

<p><strong>&nbsp;Искомый флаг имеет вид:&nbsp;<code><em>flag{you_have_knocked_the_right_way}</em></code></strong></p>

<blockquote>
<p><span style="color:#000000;">как подключиться по SSH:&nbsp;</span><code><strong style="color:#000000; font-weight:bold;">ssh root@localhost -p 2222</strong></code></p>
</blockquote>