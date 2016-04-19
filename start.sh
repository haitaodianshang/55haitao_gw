source ~/env/bin/activate

nohup python apigw_app.py --log-file-prefix=/home/admin/logs/apigw.log --log-rotate-mode=time --log-rotate-when=D &
