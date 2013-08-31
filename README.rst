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
