from flask import Flask , render_template , request , redirect ,flash , session ,url_for 
#import pymysql as db 
import os 
import random as rd
import sqlite3 

import logging

## generateur de code barre
#import barcode 
#from barcode.writer import ImageWriter


##############
############# database

#sql = db.connect(host='localhost',user = 'root',password= None,db = 'standard')

## 
app = Flask(__name__) 
app.secret_key = "standard_app" 
app.config['UPLOAD_DOC'] = 'static/documents'

################
##############  configuration du fichier logging

# logging.basicConfig(filename = 'archive.log',level = logging.DEBUG, format ="%(levelname)s:%(asctime)s:%(message)s")
# log = logging.getLogger()


################
############### Login 
@app.route('/')
@app.route('/login', methods =['POST','GET'])
def login():
    if request.method == 'GET':

        return render_template('login.html') 
    else:
        user  = request.form['user']  
        login = request.form['pwd']

        #### verification dataBase 
        with sqlite3.connect('archivage.db') as sql :
            cur = sql.cursor()
            cur.execute("select * from users where username = ?  and  password = ? ",(user,login))
            data = cur.fetchone() 

        #### verification dataBase 
            curD = sql.cursor()
            curD.execute("select * from users where phoneUser = ?  and  password = ? ",[user,login])
            dataD = curD.fetchone() 


            if data :
            

                session['okay'] = True
                session['id']   = data[0]
                session['nom']  = data[1]
                session['phone'] = data[4] 

                #session['role'] = role[2]

           
            
                return redirect(url_for('admin'))
            elif dataD:

                session['okay'] = True
                session['id']   = dataD[0]
                session['nom']  = dataD[1]
                session['phone'] = dataD[4] 

            #session['role'] = role[2]

           
            
                return redirect(url_for('admin'))
            
            else:
                flash('mot de passe errone'.title())
                return redirect(url_for('login'))    

##############
############## Deconnexion
@app.route('/deco')
def deco():
    session.clear()
    return redirect(url_for('login'))

##############
############## Admin
@app.route('/admin')
def admin():
    with sqlite3.connect('archivage.db') as sql:
        if 'okay' in session:
        #### permission des voir les utilisateurs 
    

            id = session['id'] 

            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

            ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId =? and permissionId = 3  ",[id])
            create = creation.fetchall()

            ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

            ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

            ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

            ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

            ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

            ##Nombre des archive externe
            ext = sql.cursor()
            ext.execute("select * from archives where natureA = 'externe' ")
            extA = ext.fetchall()

            ## Nombre des archives interne 
            ari = sql.cursor()
            ari.execute("select * from archives where natureA = 'interne' ")
            ariA = ari.fetchall()

            #nombre utilisateurs
            userN = sql.cursor()
            userN.execute("select * from users")
            userNr = userN.fetchall() 
            

            #Totale archives 
            tt = sql.cursor()
            tt.execute('select * from archives')
            ttA = tt.fetchall()


            return render_template('index.html',userNr = userN.rowcount ,ttA = tt.rowcount,ariA = ari.rowcount ,extA = ext.rowcount ,a = session['okay'] , listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU)
        else:
            return redirect(url_for('login'))   
        
##################
################ users liste
@app.route('/users',methods = ['POST','GET'])
def users():
    if 'okay' in session:
        if request.method == 'GET':
            with sqlite3.connect('archivage.db') as sql :
            #### permission des voir les utilisateurs
                id = session['id']
                user = sql.cursor()
                user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
                userL = user.fetchall()

            ##### Permission de la creation des users
                create = sql.cursor()
                create.execute("select * from roles where userId = ? and permissionId = 3",[id])
                createU = create.fetchall()

            ##### Permission de l'acces de donnee les permissions
                permission = sql.cursor()
                permission.execute("select * from roles where userId = ? and permissionId = 6",[id])
                permissionU = permission.fetchall()

            ###### Modifications 
                modification = sql.cursor()
                modification.execute("select * from roles where userId = ? and permissionId = 9",[id])
                modificationU = modification.fetchall()

            ####### suppression 
                delete = sql.cursor()
                delete.execute("select * from roles where userId = ? and permissionId =4",[id])
                deleteU = delete.fetchall() 

            """
                * Pas besoin de double la partie create user vue qu'il se trouve dans une seule page(user.html)
                * Idem mais la partie Permission 
            """

            
            with sqlite3.connect("archivage.db") as sql:

            ### Information des users
                user = sql.cursor()
                user.execute('select idUser,username,password,date(dateE),phoneUser from users')
                users = user.fetchall()


            ### Permission lecture 
                lecture = sql.cursor()
                lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
                lectureUser = lecture.fetchall()

            ### permission ecrire
                ecrit = sql.cursor()
                ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
                read = ecrit.fetchall()

            #### permissions de supprumer une permission
                bloque = sql.cursor()
                bloque.execute("select * from roles where userId = ? and permissionId = 10",[id])
                bloqueU = bloque.fetchall()

            ####Permission d'archive et lecture
                id = session['id']
                archive = sql.cursor()
                archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
                archiveU = archive.fetchall()

            ### Permission type d'archive
                typeA = sql.cursor()
                typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
                typeU = typeA.fetchall()

            ## Permission liste archives 
                listeA = sql.cursor()
                listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
                listeAU = listeA.fetchall()

             ## Permission archivage externe
                externe = sql.cursor()
                externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
                externeU = externe.fetchall()
            

            return render_template('users.html',a = session['okay'], typeU = typeU ,user = users ,listeAU = listeAU ,bloqueU = bloqueU ,userL = userL , externeU = externeU,createU = createU , permissionU = permissionU , modificationU = modificationU,deleteU = deleteU ,lectureUser= lectureUser, read = read, archiveU = archiveU) 
        else:
            ###for add user 

            nom = request.form['nom']
            phone = str(request.form['phone'])
            pwd   = request.form['pwd']
            pwdc  = request.form['pwdc'] 

            with sqlite3.connect("archivage.db") as sql :


            ## condition pour evitee un double  phone 
                tel = sql.cursor()
                tel.execute("select * from users where phoneUser = ?",[phone])
                dataTel = tel.fetchone()

            ## verifier l'utilisateur existant 
                ex = sql.cursor()
                ex.execute('select * from users where username = ? and password = ?',[nom,pwd])
                dataEx = ex.fetchone()

                if dataTel:
                    flash("numero de telephone existe deja ")
                    return redirect(url_for('users'))
                elif pwd != pwdc:
                    flash('Mot de passe doit etre identique')
                    return redirect(url_for('users')) 
                
                elif dataEx:
                    flash("Information existant dans la base de donnee")
                    return redirect(url_for('users')) 

                else:
                    add = sql.cursor()
                    add.execute('insert into users(username,phoneUser,password)values(?,?,?)',[nom,phone,pwd])
                    sql.commit()
                    return redirect(url_for('users'))
                    

    else:
        return redirect(url_for('login')) 
#################
############### Permission user 
@app.route('/permission/<string:idUser>',methods = ['GET','POST'])
def permission(idUser):
    if 'okay' in session:
        if request.method == 'POST':
            id      = request.form['id']
            choix   = request.form['choix'] 
            """
                on va traivalee sur la verification des identifiant 
                Genre verification de id existent dans la session 
            """
            with sqlite3.connect("archivage.db") as sql :
            ###verification de role user database 
                ro = sql.cursor()
                ro.execute('select * from roles where permissionId = ? and userId = ?',[choix,id])
                role = ro.fetchall()
                if role:
                    flash("Information existe")
                #return redirect(url_for('permission'))
                else:
                    cur = sql.cursor()
                    cur.execute('insert into roles(userId,permissionId)values(?,?)',[id,choix])
                    sql.commit()
                    cur.close()

                    flash("Information enregistre avec succee ")
                
        
        with sqlite3.connect("archivage.db") as sql :


            cur = sql.cursor()
            cur.execute('select * from users where idUser = ?',[idUser])
            da = cur.fetchone()

        #####permission database 
            permission = sql.cursor()
            permission.execute('select * from permissions')
            aff = permission.fetchall()

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()  

        #### permission ecrire
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ####
        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()
            


        return render_template('permission.html',data = da ,externeU = externeU,typeU = typeU ,userL = userL ,listeAU = listeAU ,aff = aff , lectureUser = lectureUser, read = read,archiveU = archiveU)
    else:
        return redirect(url_for('login'))   

#################
############### Ecrire user
@app.route('/ecrire',methods =['POST','GET'])
def ecrire():
    if 'okay' in session:
        if request.method == 'POST':

            sujet       = request.form['objet']
            auteur      = request.form['auteur']
            com         = request.form['commentaire']

            expediteur  = session['nom']
            ref         = request.form['ref']
            file        = request.files['document']
            liste       = request.form['liste'] 
            # refM        = request.form['refM']

            fl          = os.path.join(app.config['UPLOAD_DOC'] ,file.filename)
            file.save(fl)
            nature      = 'nouveau document externe'

             

            with sqlite3.connect("archivage.db") as sql :


            ##verification du numero d'enregistrement
                # en = sql.cursor()
                # en.execute('select * from documents where numeroReferenceD = ?',[ref])
                # afR = en.fetchone()

            ### verification d'objet
                obj = sql.cursor()
                obj.execute('select * from documents where titreDocument = ?',[sujet])
                afD = obj.fetchone()

                # if afR:
                #     flash('Le numero de reference existe ')
                #     return redirect(url_for('ecrire'))
           
                
                cur = sql.cursor()
                cur.execute('INSERT INTO documents(titreDocument,documentPdf,indexD,descriptionD,userId,nature,expediteur,auteur)values(?,?,?,?,?,?,?,?)',[sujet,file.filename,ref,com,liste,nature,expediteur,auteur]) 
                sql.commit()
                cur.close()
                flash("document expediee ".title())
                return redirect(url_for('ecrire'))       


                
            
        with sqlite3.connect("archivage.db") as sql :

          
            id = session['id']
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## 
            id = session['id']
            doc = sql.cursor()
            doc.execute('select idDocument,titreDocument,documentPdf,descriptionD,date(localD) , time(localD),username ,userId , nature,localD,expediteur,auteur from documents inner join users on documents.userId = users.idUser where userId = ? order by idDocument desc',[id])
            d = doc.fetchall() 

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()       
            
        ### Liste de useer
        
            us = sql.cursor()
            us.execute("select * from users order by idUser") 
            use = us.fetchall()     

        ### generateur automatique de numero de reference

            alph = "0123456987"
            ref = ''.join(rd.sample(alph,6))          
            
        return render_template('compose.html',use = use , ref = ref,listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU)
    else:
        return redirect(url_for('login'))    

#################
############### Lecture user 
@app.route('/lecture',methods = ['POST','GET'])
def lecture():
    if 'okay' in session:
        if request.method == 'POST':
            pass
        #### permission ecrire
        with sqlite3.connect('archivage.db') as sql :
            id = session['id']
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## 
            id = session['id']
            doc = sql.cursor()
            doc.execute('select idDocument,titreDocument,documentPdf,descriptionD,date(localD) , time(localD),username ,userId , nature,localD,expediteur,auteur from documents inner join users on documents.userId = users.idUser where userId = ? order by idDocument desc',[id])
            d = doc.fetchall() 

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

            return render_template('inbox.html', d = d, listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU)
       
    else:
        return redirect(url_for('login'))
    


#################
############### View user 
@app.route('/view/<string:idDocument>',methods =['GET'])
def view(idDocument):
    if 'okay' in session:
        ####Permission d'archive et lecture
        with sqlite3.connect("archivage.db") as sql:
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()
            ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

        #### permission de supprimee un document
            document = sql.cursor()
            document.execute("select * from roles where userId = {0} and permissionId = 11".format(id))
            documentU = document.fetchall()

            doc = sql.cursor()
            doc.execute('select idDocument,titreDocument,documentPdf,descriptionD,date(localD) , time(localD),username,phoneUser,nature,expediteur,auteur from documents inner join users on documents.userId = users.idUser where idDocument = {0}'.format(idDocument))
            d = doc.fetchone()

           #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()


            return render_template('mail-view.html',aff = d , read = read ,create = create,userL = userL,lectureUser = lectureUser,archiveU = archiveU, documentU = documentU,listeAU = listeAU ,listeA = listeA,typeU = typeU ,externeU = externeU ) 
    else:
        return redirect(url_for('login'))
#################
############### modification du mot de passe
@app.route('/modify',methods =['GET','POST'])
def modify():
    if 'okay' in session:
        if request.method == 'POST':
            id   = session['id']
            
            old  = request.form['old']
            new  = request.form['new']
            conf = request.form['conf']

            #### verification du mot de passe existant
            with sqlite3.connect("archivage.db") as sql:


                ve = sql.cursor()
                ve.execute("select * from users where password = ? and idUser = ?",[old,id]) 
                data_ver = ve.fetchone()

                if data_ver:
                
                    if new != conf:
                        flash('le mot de passe doit etre conforme')  
                        return redirect(url_for('modify'))
                    else:
                        cur = sql.cursor()
                        cur.execute('update users set password = ? where idUser = ?',[new,id])
                        sql.commit()
                        cur.close()

                        return redirect(url_for('login')) 
                else:
                    flash('Ancien mot de passe incorrecte')
                    return redirect(url_for('modify'))   
                
        with sqlite3.connect('archivage.db') as sql :

            id = session['id']

            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

            ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId =? and permissionId = 3  ",[id])
            create = creation.fetchall()

            ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

            ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

            ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

            ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

            ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

            ##Nombre des archive externe
            ext = sql.cursor()
            ext.execute("select * from archives where natureA = 'externe' ")
            extA = ext.fetchall()

            ## Nombre des archives interne 
            ari = sql.cursor()
            ari.execute("select * from archives where natureA = 'interne' ")
            ariA = ari.fetchall()

            #nombre utilisateurs
            userN = sql.cursor()
            userN.execute("select * from users")
            userNr = userN.fetchall() 
            

            #Totale archives 
            tt = sql.cursor()
            tt.execute('select * from archives')
            ttA = tt.fetchall()


            

                         

        return render_template('change-password.html',userNr = userN.rowcount ,ttA = tt.rowcount,ariA = ari.rowcount ,extA = ext.rowcount ,a = session['okay'] , listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU)
    else:
        return redirect(url_for('login'))

#################
###############delete Permission user 
@app.route('/permissionD/<string:idUser>',methods = ['GET','POST'])
def permissionD(idUser):
    if 'okay' in session:
        if request.method == 'POST':
            id      = request.form['id']
            choix   = request.form['choix'] 

            with sqlite3.connect('archivage.db') as sql:


                cur = sql.cursor()
                cur.execute('DELETE FROM roles WHERE permissionId = ? and userId = ?',[choix,id])
                sql.commit()
                cur.close()

                flash("Permission supprimee avec succee ")
          
           


                
        
      
        with sqlite3.connect("archivage.db") as sql :

            cur = sql.cursor()
            cur.execute('select * from users where idUser = ?',[idUser])
            da = cur.fetchone()

        #####suppression role dans la database 
            permission = sql.cursor()
            permission.execute('SELECT idRole,libPermission , permissionId FROM roles inner join permissions ON roles.permissionId = permissions.idPermission  where userId = ? ',[idUser])
            aff = permission.fetchall()

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()  

        #### permission ecrire
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ####
        ####Permission d'archive et lecture
        
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()
            


        return render_template('permissionD.html',data = da , externeU = externeU ,userL = userL , aff = aff , lectureUser = lectureUser, read = read , archiveU = archiveU,listeAU = listeAU)
    else:
        return redirect(url_for('login'))   

#################
###############delete user
@app.route('/delete/<string:idUser>', methods =['GET'])
def delete(idUser):
    if request.method == 'GET':
        with sqlite3.connect('archivage.db') as sql :
            cur = sql.cursor()
            cur.execute("delete from users where idUser = ? ",[idUser])
            sql.commit()
            cur.close()
            flash('user supprimee'.title())

            return redirect(url_for('user'))  
    
#################
############### Archive documents
@app.route('/archive/<string:idDocument>',methods =['POST','GET'])
def archive(idDocument):
    if 'okay' in session:
        if request.method == 'POST':
            archive        = request.form['archive']
            reference      = request.form['ref']
            index          = request.form['index']
            auteur         = request.form['auteur']
            configuration  = request.form['configuration']
            notification   = request.form['notification']
            nature         = 'doc interne'
            titre          = request.form['titre']

            with sqlite3.connect('archivage.db') as sql :


                cur = sql.cursor()
                cur.execute("INSERT INTO archives(titreA,archiveA,indexA,referenceA,auteurA,configurationA,natureA,notificationA)VALUES(?,?,?,?,?,?,?,?)",[titre,archive,index,reference,auteur,configuration,nature,notification])
                sql.commit()
                flash("document archivee")
                return redirect(url_for('admin'))
        else:
            with sqlite3.connect('archivage.db') as sql :


        ## type des archive
                tp = sql.cursor()
                tp.execute('select * from configurations')
                tpA = tp.fetchall()
        #### document
                ar = sql.cursor()
                ar.execute('select * from documents where idDocument = ?',[idDocument])
                arc = ar.fetchone()
        ##### index generator
                mot   = "1234567890"
                index = ''.join(rd.sample(mot,5)) 
            return render_template('archive.html',arc = arc , index = index, listeT = tpA)
    else:
        return redirect(url_for('login'))    
##################3
################  Enregistrement des archives externe
@app.route('/archiveEx',methods = ['POST','GET'])
def archiveEx():
    if 'okay' in session:

        if request.method == 'POST':
            archive        = request.files['archive']
            reference      = request.form['ref']
            index          = request.form['index']
            auteur         = request.form['auteur']
            configuration  = request.form['configuration']
            notification   = request.form['notification']
            nature         = request.form['nature']
            titre          = request.form['titre']

            fl          = os.path.join(app.config['UPLOAD_DOC'] ,archive.filename)
            archive.save(fl)

            with sqlite3.connect('archivage.db') as sql :


                cur = sql.cursor()
                cur.execute("INSERT INTO archives(titreA,archiveA,indexA,referenceA,auteurA,configurationA,natureA,notificationA)VALUES(?,?,?,?,?,?,?,?)",[titre,archive.filename,index,reference,auteur,configuration,nature,notification])
                sql.commit()
                flash(f"document {nature} archivee")
                return redirect(url_for('archiveEx'))
            
            
            
           
        with sqlite3.connect('archivage.db') as sql :
            mot   = "1234567890"
            index = ''.join(rd.sample(mot,5))

            alph = "0123456987"
            ref = ''.join(rd.sample(alph,6))
                

        ## type des archive
            tp = sql.cursor()
            tp.execute('select * from configurations')
            tpA = tp.fetchall()

            id = session['id']
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## 
            id = session['id']
            doc = sql.cursor()
            doc.execute('select idDocument,titreDocument,documentPdf,descriptionD,date(localD) , time(localD),username ,userId , nature,localD,expediteur,auteur from documents inner join users on documents.userId = users.idUser where userId = ? order by idDocument desc',[id])
            d = doc.fetchall() 

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()       
            


        
        return render_template('externe.html',index = index, ref = ref,listeT = tpA,listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU) 
    else:
        return  redirect(url_for('login'))           

#################
############### transfert document
@app.route('/trans/<string:idDocument>',methods = ['POST','GET'])
def trans(idDocument):
    if 'okay' in session:
        if request.method == 'POST':
            sujet = request.form['sujet']
            file   = request.form['document'] 
            liste = request.form['liste']    
            ref = request.form['ref']   
            refM  = request.form['refM'] 
            com   = request.form['com'] 
            nature   = 'Transfert' 
            auteur  = request.form['auteur']  
            expediteur = session['nom']


            with sqlite3.connect("archivage.db") as sql:


                cur = sql.cursor()
                cur.execute('INSERT INTO documents(titreDocument,documentPdf,indexD,descriptionD,userId,nature,expediteur,auteur)values(?,?,?,?,?,?,?,?)',[sujet,file,ref,refM,liste,nature,expediteur,auteur]) 
                sql.commit()
                cur.close()
                flash("document transfert ".title())
                return redirect(url_for('ecrire')) 
        ### Liste de useer
        else:
            with sqlite3.connect('archivage.db') as sql :
        
                us = sql.cursor()
                us.execute("select * from users order by idUser") 
                use = us.fetchall()  

            ## appel du document 
                cal = sql.cursor()
                cal.execute('select idDocument,titreDocument,documentPdf,descriptionD,indexD,nature,expediteur,auteur from documents where idDocument = {0}'.format(idDocument))
            
                call = cal.fetchone()

        ####Permission d'archive et lecture
                id = session['id']
                archive = sql.cursor()
                archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
                archiveU = archive.fetchall()
        ### Permission type d'archive
                typeA = sql.cursor()
                typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
                typeU = typeA.fetchall()

        ## Permission liste archives 
                listeA = sql.cursor()
                listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
                listeAU = listeA.fetchall()

        ## Permission archivage externe
                externe = sql.cursor()
                externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
                externeU = externe.fetchall()

        #### permission de supprimee un document
                document = sql.cursor()
                document.execute("select * from roles where userId = {0} and permissionId = 11".format(id))
                documentU = document.fetchall()

                doc = sql.cursor()
                doc.execute('select idDocument,titreDocument,documentPdf,descriptionD,date(localD) , time(localD),username,phoneUser,nature,expediteur,auteur from documents inner join users on documents.userId = users.idUser where idDocument = {0}'.format(idDocument))
                d = doc.fetchone()

           #### permission des voir les utilisateurs
                id = session['id']
                user = sql.cursor()
                user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
                userL = user.fetchall()

                ecrit = sql.cursor()
                ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
                read = ecrit.fetchall()

        ## creation permission
                creation = sql.cursor()
                creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
                create = creation.fetchall()

        ### Permission lecture 
                lecture = sql.cursor()
                lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
                lectureUser = lecture.fetchall()





            return render_template('tranfert.html', use = use, call = call,read = read , typeU = typeU,lectureUser = lectureUser ,create = create,listeAU = listeAU,userL = userL,archiveU = archiveU,documentU=documentU,externeU = externeU)
    else:
        return redirect(url_for('login')) 



            
#################
############### chat reponse decument
@app.route('/chat',methods = ['POST','GET'])
def chat():
    if 'okay' in session:
        return render_template('chat.html')
    else:

        return redirect(url_for('login'))    
##################3
################  suppression du document 
@app.route('/delete_doc/<string:idDocument>',methods = ['GET'])
def delete_doc(idDocument):
    if 'okay' in session:
        with sqlite3.connect("archivage.db") as sql :
            cur = sql.cursor()
            cur.execute('delete from documents where idDocument = {0}'.format(idDocument))
            sql.commit()
            cur.close()

            return redirect(url_for('lecture'))   
    else:
        return redirect(url_for('login'))  
        
##################3
################  type de archive
@app.route('/type',methods = ['GET','POST'])
def type():
    if 'okay' in session:
        if request.method == 'POST':
            typeA = request.form['typeA']
            dure  = int(request.form['dure'])
            choix = request.form['choix']

            ## si le jour est egale a jour
            if choix == 'jour':
                jr = f"{dure}"

                with sqlite3.connect("archivage.db") as sql :

                    cur = sql.cursor()
                    cur.execute("insert into configurations(libConfiguration,dure,choix)values(?,?,?)",[typeA,jr,choix])
                    sql.commit()
                    flash(f"enregistrement reussi ")
                    return redirect(url_for('type')) 
            elif choix == 'mois':
                ms = f"{dure * 30 + 1 }"

                with sqlite3.connect("archivage.db") as sql :
                    cur = sql.cursor()
                    cur.execute("insert into configurations(libConfiguration,dure,choix)values(?,?,?)",[typeA,ms,choix])
                    sql.commit()
                    flash(f"enregistrement reussi")
                    return redirect(url_for('type')) 
            else:
                an = f'{dure * 365 + 2}' 
                with sqlite3.connect("archivage.db") as sql :

                    cur = sql.cursor()
                    cur.execute("insert into configurations(libConfiguration,dure,choix)values(?,?,?)",[typeA,an,choix])
                    sql.commit()
                    flash(f"enregistrement reussi")
                return redirect(url_for('type'))   





            ### verification des information existant
         

            
          
               
        with sqlite3.connect("archivage.db") as sql : 

            id = session['id']
        #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()  

        #### permission ecrire
            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ####
        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

        return render_template('type.html',typeU = typeU , archiveU = archiveU ,externeU = externeU ,read = read , lectureUser = lectureUser, userL = userL,listeAU = listeAU)
    else:
        return redirect(url_for('login'))  

##################3
################  liste des archive 
@app.route('/listeAr')
def listeAr():
    if 'okay' in session:
       
        with sqlite3.connect("archivage.db") as sql :
        #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall() 

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

        ## Liste des archive avec 
            lst = sql.cursor()
            lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA ,   strftime('%d', dateA) - strftime('%d', date('now'))  from archives inner join configurations on archives.configurationA = configurations.idConfiguration  order by idArchive desc")
            lstU = lst.fetchall()

            # lst = sql.cursor()
            # lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA ,datediff(now(),dateA) from archives inner join configurations on archives.configurationA = configurations.idConfiguration where dure >= datediff(now(),dateA) order by idArchive desc")
            # lstU = lst.fetchall()

        return render_template('listeAr.html' , userL = userL,lstU = lstU , lectureUser = lectureUser , read = read ,create = create ,archiveU = archiveU ,typeU = typeU ,listeAU = listeAU ,externeU = externeU) 
    else:
        return redirect(url_for('login'))                         

####################################
################# Table de recherche
@app.route('/data')
def data():
    if 'okay' in session:
        with sqlite3.connect("archivage.db") as sql :
        ## Liste des archives
            lst = sql.cursor()
            lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA  from archives inner join configurations on archives.configurationA = configurations.idConfiguration  order by idArchive desc")
            lstU = lst.fetchall()

            # lst = sql.cursor()
            # lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA ,datediff(now(),dateA) from archives inner join configurations on archives.configurationA = configurations.idConfiguration where dure >= datediff(now(),dateA) order by idArchive desc")
            # lstU = lst.fetchall()

         #### permission des voir les utilisateurs
            id = session['id']
            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

        ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId = ? and permissionId = 3  ",[id])
            create = creation.fetchall()

        ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

        ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

        ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

        ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

        ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

        ## Liste des archive avec 
            lst = sql.cursor()
            lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA   from archives inner join configurations on archives.configurationA = configurations.idConfiguration  order by idArchive desc")
            lstU = lst.fetchall()

            # lst = sql.cursor()
            # lst.execute("select idArchive,titreA,archiveA,indexA,referenceA,auteurA,libConfiguration,dure,choix,natureA,notificationA,dateA ,datediff(now(),dateA) , dure - datediff(now(),dateA)  from archives inner join configurations on archives.configurationA = configurations.idConfiguration where dure >= datediff(now(),dateA) order by idArchive desc")
            # lstU = lst.fetchall()

        return render_template('data/export-table.html', userL = userL,lstU = lstU , lectureUser = lectureUser , read = read ,create = create ,archiveU = archiveU ,typeU = typeU ,listeAU = listeAU ,externeU = externeU)
    else:
        return redirect(url_for('login'))    

#
#
# MODIFICATION DE L'UTILISATEUR PAR L'ADMIN 
@app.route("/userModify/<string:idUser>", methods = ['GET','POST'])
def userModify(idUser):
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone') 

        with sqlite3.connect('archivage.db') as sql:
            cur = sql.cursor()
            cur.execute("update users set username = ? , phoneUser = ? where idUser = ?",[name,phone,idUser])
            sql.commit() 
            #flash("Information Modifier !!!!")
            cur.close()
            return redirect('/users')
    with sqlite3.connect('archivage.db') as sql:
        if 'okay' in session:
        #### permission des voir les utilisateurs 
    

            id = session['id'] 

            user = sql.cursor()
            user.execute("select * from roles where userId = ? and permissionId = 8 ",[id])
            userL = user.fetchall()

            ecrit = sql.cursor()
            ecrit.execute("select * from roles where userId = ? and permissionId = 2 ",[id])
            read = ecrit.fetchall()

            ## creation permission
            creation = sql.cursor()
            creation.execute("select * from roles where userId =? and permissionId = 3  ",[id])
            create = creation.fetchall()

            ### Permission lecture 
            lecture = sql.cursor()
            lecture.execute("select * from roles where userId = ? and permissionId = 1",[id])
            lectureUser = lecture.fetchall()

            ####Permission d'archive et lecture
            id = session['id']
            archive = sql.cursor()
            archive.execute("select * from roles where userId = ? and permissionId = 5 ",[id])
            archiveU = archive.fetchall()

            ### Permission type d'archive
            typeA = sql.cursor()
            typeA.execute('select * from roles where userId = {0} and permissionId = 12'.format(id))
            typeU = typeA.fetchall()

            ## Permission liste archives 
            listeA = sql.cursor()
            listeA.execute("select * from roles where userId = {0} and permissionId = 14".format(id))
            listeAU = listeA.fetchall()

            ## Permission archivage externe
            externe = sql.cursor()
            externe.execute('select * from roles where userId = {0} and permissionId = 13'.format(id))
            externeU = externe.fetchall()

            ##Nombre des archive externe
            ext = sql.cursor()
            ext.execute("select * from archives where natureA = 'externe' ")
            extA = ext.fetchall()

            ## Nombre des archives interne 
            ari = sql.cursor()
            ari.execute("select * from archives where natureA = 'interne' ")
            ariA = ari.fetchall()

            #nombre utilisateurs
            userN = sql.cursor()
            userN.execute("select * from users")
            userNr = userN.fetchall() 
            

            #Totale archives 
            tt = sql.cursor()
            tt.execute('select * from archives')
            ttA = tt.fetchall()

            ## affichage d'utilisateur 
            md = sql.cursor()
            md.execute("select * from users where idUser = ?",[idUser])
            dataMd  = md.fetchone()


            return render_template('userModify.html',dataMd = dataMd,userNr = userN.rowcount ,ttA = tt.rowcount,ariA = ari.rowcount ,extA = ext.rowcount ,a = session['okay'] , listeAU = listeAU ,userL = userL , lectureUser = lectureUser ,externeU = externeU, read = read,archiveU = archiveU , typeU = typeU)
    
        


## Boucle 
if __name__ == '__main__':
    app.run(debug = True)
#log.info(app()) 
#log.info(admin())   
