create table "user"
(
    user_id  serial primary key,
    login    text unique not null,
    password char(60)    not null,
    token    char(125)
);

create table function
(
    fn_id   serial primary key,
    "name"  text    not null,
    owner   integer not null references "user" (user_id) on delete cascade,
    code_id char(36),

    unique (owner, name)
);

create table kappalog
(
    log_id  serial primary key,
    "time"  timestamp with time zone default now(),
    "user"  integer references "user" (user_id) on delete cascade,
    fn      integer references "function" (fn_id) on delete cascade,
    content jsonb not null
);
