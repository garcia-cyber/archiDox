import sqlite3 

lite = sqlite3.connect('archivage.db') 

##
# creation de la table 
lite.execute("""
                create table if not exists users(
             idUser integer primary key autoincrement ,
             username varchar(50),
             phoneUser varchar(15),
             password varchar(100),
             dateE timestamp default current_timestamp)
""")


# table configuration 
lite.execute("""
    create table if not exists configurations(
             idConfiguration integer primary key autoincrement ,
             libConfiguration varchar(80),
             dure integer , 
             choix varchar(10),
             tps timestamp default current_timestamp)
""")


#table archive 
# lite.execute("drop table archives") 
# print('drop ')
lite.execute("""
 
create table if not exists archives(
    idArchive integer primary key autoincrement ,
    titreA varchar(50),
    archiveA text,
    indexA varchar(25),
    referenceA varchar(20),
    auteurA varchar(50),
    configurationA integer ,
    natureA varchar(50),
    notificationA text,
    foreign key(configurationA) references configurations(idConfiguration)
 
  
)

""")

# table permissions 
lite.execute("""
        create table if not exists permissions(
             idPermission integer primary key autoincrement ,
             libPermission varchar(35))
""")

# creation de la table role 
lite.execute("""
    create table if not exists roles(
             idRole integer primary key autoincrement ,
             permissionId integer ,
             userId integer , 
             foreign key(permissionId) references permissions(idPermission) ,
             foreign key(userId) references users(idUser)
             )
""")
#role admin 
#lite.execute("insert into roles(permissionId, userId) values(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1)")
# lite.execute("insert into roles(permissionId, userId) values(8,1)")
# lite.execute("insert into roles(permissionId, userId) values(9,1),(6,1),(10,1),(13,1)")
# lite.execute("drop table roles")
# lite.execute('delete from roles')
# lite.execute("insert into roles(permissionId, userId) values(11,1),(12,1)")
# lite.execute("insert into permissions(libPermission) values('liste des achives interne')")
print('add okay')

## table documents 


# lite.execute("drop table documents")

lite.execute("""
                create table if not exists documents(
             idDocument integer primary key autoincrement ,
             titreDocument varchar(50) ,
             documentPdf text ,
             descriptionD text ,
             indexD varchar(35),
             nature varchar(50),
             expediteur varchar(50),
             auteur varchar(50),
             localD timestamp default current_timestamp ,
             userId integer ,
             foreign key(userId) references users(idUser)
             )
""")

# table commentaires 
lite.execute("""
             
            create table if not exists commentaires(
             
            idCommentaire integer primary key autoincrement , 
            commentaire text ,
            documentID  integer , 
            userID integer ,
            localC timestamp default current_timestamp,
            foreign key(documentID) references documents(idDocument) ,
            foreign key(userID) references users(idUser)
             ) 
            
""")


lite.commit()
