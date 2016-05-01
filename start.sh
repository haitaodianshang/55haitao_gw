source ../env/bin/activate

nohup python apigw_app.py --log-file-prefix=/var/55haitao/log/apigw.log --log-rotate-mode=time --log-rotate-when=D &
