create schema kappa;

create table kappa.user
(
    user_id  serial primary key,
    login    text unique not null,
    password char(60)    not null,
    token    char(60)
);

create table kappa.function
(
    fn_id serial primary key,
    "name"  text    not null,
    owner integer not null references kappa.user (user_id) on delete cascade,

    unique (owner, name)
);

create table kappa.kappa_log
(
    log_id  serial primary key,
    "time"    timestamp with time zone default now(),
    "user"    integer references kappa.user (user_id) on delete cascade,
    fn      integer references kappa.function (fn_id) on delete cascade,
    content jsonb not null
);

create
user kappadata;
grant all privileges on schema
kappa to kappadata;
