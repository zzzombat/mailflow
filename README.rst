mailflow
========

First hackathon project by Eastwood team and others


Postfix configuration
---------------------

/etc/postfix/main.cf:

::

    smtpd_recipient_restrictions =
        permit,
        reject

    virtual_transport = mailflow
    virtual_mailbox_domains = pgsql:/etc/postfix/mailflow/domains.map.cf
    virtual_mailbox_maps = pgsql:/etc/postfix/mailflow/mailboxes.map.cf

/etc/postfix/master.cf:

::

    mailflow     unix -       n       n       -       -       pipe
    flags=R user=nobody argv=/home/kubus/envs/mailflow/bin/mailflow-deliver ${recipient} ${sender}



Database configuration
---------------------

Create database and grant access:

::

    sudo su postgres
    createuser -s username(Ваш логин в ОС)
    createdb mailflow

Init database:

::
    python src/mailflow/front/migrate/init_db.py


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
