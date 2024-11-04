create schema standard;

use standard;
-- table utilisateur 

create table users(
    idUser smallint auto_increment not null ,
    username varchar(50),
    password varchar(100),
    dateR timestamp default current_timestamp(),
    constraint pk_user primary key(idUser)
);

alter table users add phoneUser varchar(15);

insert into users(username,password,phoneUser)values('admin','admin','0995540211');





-- table messages 

create table documents(
    idDocument bigint auto_increment not null ,
    titreDocument varchar(150),
    documentPdf longtext ,
    numeroReferenceD varchar(80),
    descriptionD longtext,
    nomUser varchar(50),
    phoneUser varchar(15),
    localD timestamp default current_timestamp(),
    constraint pk_document primary key(idDocument)


);

alter table documents add indexD varchar(35);

alter table documents add numeroEnregistrement varchar(50), add userId smallint , add constraint fk_u foreign key(userId) references users(idUser) on delete set null on update cascade;
alter table documents drop nomUser , drop phoneUser;
alter table documents drop numeroEnregistrement;
alter table documents add nature varchar(15);
alter table documents add expediteur varchar(40);
alter table documents add auteur varchar(50);



-- table commentaire 

create table commentaires(
    idCommentaire bigint auto_increment primary key,
    commentaire longtext ,
    documentC bigint,
    nomUser varchar(50),
    phoneUser varchar(15),
    localC timestamp default current_timestamp(),
    constraint fk_documentC foreign key(documentC) references documents(idDocument) on delete set null on update cascade
);

-- creation de la table type d'archive
create table configurations(
 idConfiguration tinyint auto_increment not null ,
 
  libConfiguration varchar(80) ,         
  dure             bigint(20)  ,
 choix             varchar(10) ,
 tps  timestamp default current_timestamp(),
 constraint pk_type_archive primary key(idConfiguration) 
 );


-- archivage 

create table archives(
    idArchive bigint auto_increment not null ,
    titreA varchar(50),
    archiveA longtext,
    indexA varchar(25),
    referenceA varchar(20),
    auteurA varchar(50),
    configurationA tinyint ,
    natureA varchar(50),
    notificationA text,
    constraint fk_arc foreign key(configurationA) references configurations(idConfiguration) on delete set null ,
    constraint pk_arc_pk primary key(idArchive) 
  
);

alter table archives add dateA timestamp default current_timestamp();

-- table permission 

create table permissions(
    idPermission tinyint auto_increment primary key,
    libPermission varchar(35)
);

insert into permissions(libPermission)values('Lire Document'),('Scanner Document'),('Creer Utilisateur'),('Supprimer Utilisateur'),('Lire et Archiver courrier');
insert into permissions(libPermission)values('Attribuer Role');
insert into permissions(libPermission)values('recevoir');
insert into permissions(libPermission)values('Afficher Utilisateur');
insert into permissions(libPermission)values('Modifier Utilisateur');
insert into permissions(libPermission)values('Retire Role');
insert into permissions(libPermission)values('Supprime Document'); 
insert into permissions(libPermission)values("Ajout Type Document"); 
insert into permissions(libPermission)values("Service Archivage"); 
insert into permissions(libPermission)values("Archives");  


delete from permissions where idPermission = 7;           

-- role d'utilisateur 

create table roles(
    idRole tinyint auto_increment not null ,
    permissionId tinyint,
    userId smallint,
    constraint fk_userId foreign key(userId) references users(idUser) on delete set null on Update cascade,
    constraint fk_permissionId foreign key(permissionId) references permissions(idPermission)  on delete set null on Update cascade,
    constraint pk_role primary key(idRole)
);




