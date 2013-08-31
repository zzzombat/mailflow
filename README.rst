mailflow
========

First hackathon project by Eastwood team and others.


Installation on Ubuntu 12.04
----------------------------

Create and activate virtualenv:

::

    mkdir ~/envs/
    virtualenv --system-site-packages ~/envs/mailflow
    . ~/envs/mailflow/bin/activate

Install mailflow package:

::

    pip install git+https://github.com/zzzombat/mailflow.git


Install and configure postgresql server:

::

    sudo aptitude install postgresql -y
    sudo su - postgres -c "createuser -S -R -D mailflow -P"
    sudo su - postgres -c "createdb mailflow -O mailflow"

Create mailflow database:

::

    mailflow-initdb


Postfix configuration
~~~~~~~~~~~~~~~~~~~~~

Installation:

::

    sudo aptitude install libsasl2-modules-sql libsasl2-2 sasl2-bin  libsasl2-modules postfix


Configure authentication over mailflow database. /etc/postfix/sasl/smtpd.conf:

::

    pwcheck_method: auxprop
    auxprop_plugin: sql
    mech_list: PLAIN LOGIN
    sql_engine: pgsql
    sql_user: mailflow
    sql_hostnames: 127.0.0.1
    sql_password: secret
    sql_database: mailflow
    sql_select: SELECT password FROM "inbox" WHERE login = '%u'


Custom mailflow delivery agent. /etc/postfix/master.cf:

::

    mailflow     unix -       n       n       -       -       pipe
        flags=R user=kubus argv=/home/kubus/envs/mailflow/bin/mailflow-deliver ${sasl_username} ${recipient} ${sender}

    2525      inet  n       -       -       -       -       smtpd
        -o smtpd_sasl_auth_enable=yes
        -o broken_sasl_auth_clients=yes
        -o smtpd_sasl_type=cyrus
        -o smtpd_sasl_security_options=noanonymous
        -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject
        -o virtual_transport=mailflow
        -o virtual_mailbox_domains=pgsql:/etc/postfix/mailflow/domains.map.cf
        -o virtual_mailbox_maps=pgsql:/etc/postfix/mailflow/mailboxes.map.cf

/etc/postfix/mailflow/domains.map.cf

::

    hosts = 127.0.0.1
    user = mailflow
    password = secret
    dbname = mailflow
    query = SELECT '%s'


/etc/postfix/mailflow/mailboxes.map.cf

::

    hosts = 127.0.0.1
    user = mailflow
    password = secret
    dbname = mailflow
    result_format = mailflow/%s/
    query = SELECT '%s'


RabbitMQ setup
---------------------

Install RabbitMQ:

::
   sudo echo "deb http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list
   wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
   sudo apt-key add rabbitmq-signing-key-public.asc
   sudo apt-get update
   sudo apt-get install rabbitmq-server -y

Start and add admin user:

::
   sudo service rabbitmq-server start
   sudo rabbitmq-plugins enable rabbitmq_management
   sudo rabbitmqctl add_user admin password
   sudo rabbitmqctl set_user_tags admin administrator
   sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
   sudo rabbitmqctl delete_user guest
   sudo service rabbitmq-server restart

Add user:

::
   sudo rabbitmqctl add_user mailflow youneverguess
   sudo rabbitmqctl add_vhost /mail
   sudo rabbitmqctl set_permissions -p /mail mailflow ".*" ".*" ".*"

Testing
-------

Start web interface:

::

    mailflow-front

Go to the /admin url and create new inbox with login 'test' and password 'test'. To send a test
message you could use the following code:

::

    #!/usr/bin/env python

    import smtplib

    def main():
        conn = smtplib.SMTP('localhost', 2525)
        conn.login('test', 'test')
        conn.sendmail('sender@example.com', 'recipient@example.com', "Hello!")

    if __name__ == '__main__':
        main()

