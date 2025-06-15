# 🛠️ Настройка окружения для анализа Docker-образов в Windows

## Введение

В рамках практической работы потребуется настроить контейнеризированную среду внутри операционной системы Windows с использованием WSL (Windows Subsystem for Linux). Все действия производятся в терминале Ubuntu, установленном в WSL. Установка **Docker Desktop** не требуется и не используется.

Настраиваемое программное обеспечение:
- WSL с Ubuntu
- Docker Engine
- Docker Compose
- Trivy (анализатор уязвимостей)
- Dockle (анализатор безопасности Dockerfile и образов)

---

## 1. Установка WSL и Ubuntu

1. Открыть **PowerShell от имени администратора**.
2. Выполнить установку WSL:
   ```powershell
   wsl --install
   ```
   Если WSL уже установлен:
   ```powershell
   wsl --update
   ```

3. Установить Ubuntu:
   ```powershell
   wsl --install -d Ubuntu
   ```

4. Дождаться завершения установки и следовать инструкциям на экране (создать имя пользователя и пароль).

5. Проверить версию:
   ```powershell
   wsl -l -v
   ```
   Если Ubuntu работает не под WSL2:
   ```powershell
   wsl --set-version Ubuntu 2
   ```

---

## 2. Установка Docker внутри Ubuntu

После запуска Ubuntu:

1. Установить зависимости:
   ```bash
   sudo apt update
   sudo apt install -y ca-certificates curl gnupg lsb-release
   ```

2. Добавить GPG-ключ Docker:
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

3. Добавить официальный репозиторий:
   ```bash
   echo      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

4. Установить Docker:
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

5. Проверить:
   ```bash
   sudo docker version
   ```

---

## 3. Установка Docker Compose

Docker Compose устанавливается вместе с плагином `docker-compose-plugin`. Проверка:
```bash
sudo docker compose version
```

Команды выполняются как `docker compose` (через пробел, без дефиса), например:
```bash
sudo docker compose up -d
```

---

## 4. Установка Trivy

1. Добавить репозиторий:
   ```bash
   sudo apt install -y wget apt-transport-https gnupg lsb-release
   wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
   echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
   sudo apt update
   ```

2. Установить Trivy:
   ```bash
   sudo apt install -y trivy
   ```

3. Проверить:
   ```bash
   trivy --version
   ```

---

## 5. Установка Dockle

1. Скачать и установить последнюю версию:
   ```bash
   wget https://github.com/goodwithtech/dockle/releases/download/v0.4.14/dockle_0.4.14_Linux-64bit.deb
   sudo dpkg -i dockle_0.4.14_Linux-64bit.deb
   ```

2. Проверка:
   ```bash
   dockle --version
   ```

---

## 🧠 Шпаргалка: основные команды Docker в Ubuntu (WSL)

Все команды следует выполнять с `sudo`.

| Цель                          | Команда                                                          |
|-------------------------------|-------------------------------------------------------------------|
| Построить образ               | `sudo docker build -t имя_образа .`                              |
| Запустить контейнер           | `sudo docker run -it имя_образа`                                 |
| Показать запущенные контейнеры| `sudo docker ps`                                                 |
| Показать все контейнеры       | `sudo docker ps -a`                                              |
| Удалить контейнер             | `sudo docker rm <ID или имя>`                                   |
| Остановить контейнер          | `sudo docker stop <ID или имя>`                                 |
| Подключиться внутрь контейнера| `sudo docker exec -it <ID> /bin/bash`                            |
| Посмотреть образы             | `sudo docker images`                                             |
| Удалить образ                 | `sudo docker rmi <имя>`                                          |
| Запустить `docker-compose`    | `sudo docker compose up -d`                                      |
| Остановить `docker-compose`   | `sudo docker compose down`                                       |
| Проверить образ через Trivy   | `trivy image имя_образа`                                         |
| Проверить образ через Dockle  | `dockle имя_образа`                                              |

---

Если планируется совместная работа или публикация результатов — рекомендуется использовать `Git` и `GitHub` для управления кодом и настройками.

> Инструкция завершена. В случае ошибок на этапе установки Docker или WSL рекомендуется перезапустить компьютер и повторить действия строго по шагам. Все действия выполняются исключительно в терминале **Ubuntu (WSL)**.