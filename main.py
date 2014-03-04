# -*- coding: utf-8 -*-
import sys, os
import qiniu.rs, qiniu.resumable_io
from config import *
from subprocess import call

def upload(file_name):
    policy = qiniu.rs.PutPolicy('%s:%s' % (BUCKET_NAME, file_name))
    uptoken = policy.token()
    
    extra = qiniu.resumable_io.PutExtra(BUCKET_NAME)
    extra.mimetype = 'application/x-gzip'

    ret, err = qiniu.resumable_io.put_file(uptoken, file_name, file_name, extra)
    return ret

def backup(db_name):
    print 'Dump database: %s' % db_name
    call(['mysqldump', '-u', DB_USER, '-p%s' % DB_PASS, db_name, '--result-file', '%s.sql' % db_name])

    print 'Make tar file'
    call(['tar', '-zcf', '%s.sql.gz' % db_name, '%s.sql' % db_name])

    print 'Upload'
    upload('%s.sql.gz' % db_name)

    print 'Remove tar file'
    os.remove('%s.sql' % db_name)
    os.remove('%s.sql.gz' % db_name)

    print 'Backup complete\n'

for db in DB_NAME:
    backup(db)
