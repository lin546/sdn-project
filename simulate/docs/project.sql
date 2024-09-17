-- auto-generated definition
create table user
(
    id    int auto_increment primary key,
    uname varchar(255) null,
    pwd   varchar(255) null,
    root  int          null
);

INSERT INTO mydata.user (id, uname, pwd, root) VALUES (1, 'root', '21232f297a57a5a743894a0e4a801fc3', 1);