#!/usr/bin/python

import pexpect

exp = pexpect.spawn('ssh hcsdadm@localhost')
i = exp.expect(['\? ', 'password: '])

if i == 0:
   exp.send('yes\n')
   exp.expect('password: ')
   exp.send('d!!\n')
elif i == 1:
   exp.send('^d!!\n')

exp.expect('\]\$')

exp.send('grub2-mkpasswd-pbkdf2\n')
exp.expect('Enter password: ')
exp.send('d!!\n')

exp.expect('Reenter password: ')
exp.send('d!!\n')

exp.expect('\]\$')
print("%s" % exp.before)
exp.send('exit\n')

exp.close()

