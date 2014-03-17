# -*- coding: utf-8 -*-
import sys, os, time
import qiniu.rs, qiniu.resumable_io
from config import *
from subprocess import call

def date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def upload(file_name):
    policy = qiniu.rs.PutPolicy('%s:%s' % (BUCKET_NAME, file_name))
    uptoken = policy.token()
    
    extra = qiniu.resumable_io.PutExtra(BUCKET_NAME)
    extra.mimetype = 'application/x-gzip'

    ret, err = qiniu.resumable_io.put_file(uptoken, file_name, file_name, extra)
    return ret

def backup(db_name):
    dot_sql_file = '%s.sql' % db_name
    dot_tar_file = '%s.%s.sql.gz' % (date(), db_name)

    print 'Dump database: %s' % db_name
    call(['mysqldump', '-u', DB_USER, '-p%s' % DB_PASS, db_name, '--result-file', dot_sql_file])

    print 'Make tar file'
    call(['tar', '-zcf', dot_tar_file, dot_sql_file])

    print 'Upload'
    upload(dot_tar_file)

    print 'Remove tar file'
    os.remove(dot_sql_file)
    os.remove(dot_tar_file)

    print 'Backup complete\n'

for db in DB_NAME:
    backup(db)
