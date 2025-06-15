# Dockerfile (небезопасная конфигурация)
FROM ubuntu:18.04

# Установка SSH-сервера и настройка root-доступа
RUN apt-get update && apt-get install -y openssh-server && \
    echo 'root:password' | chpasswd && \ 
    sed -ri 's/^#?PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    mkdir /var/run/sshd

# Открываем порт 22 внутри контейнера
EXPOSE 22

# Запускаем SSH-сервер на фореграунд (daemon mode)
CMD ["/usr/sbin/sshd", "-D"]
