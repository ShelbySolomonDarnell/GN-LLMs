#FROM python:3.9
FROM python:latest

# install preferred tools
RUN apt update  && apt -y upgrade
RUN apt install -y zsh vim-gtk3 curl 
RUN useradd -m -s /bin/zsh coder

#RUN git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime
#RUN sh ~/.vim_runtime/install_awesome_vimrc.sh
#RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt

WORKDIR /opt
# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
