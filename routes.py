import os
import logging
import pdfkit
import hashlib
import logging
import logging
from flask import render_template, url_for, request, redirect, flash, make_response, session
from . import app, models, db
from .models import mangaForm, Admin
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
@app.route('/accueil')
def accueil():
    message = request.args.get('message', '')
    liste_categories = models.Vue_manga_categorie.query.distinct('nom_categorie')
    return render_template('accueil.html', title='Manga-Shop', liste=type(liste_categories), liste_cat=liste_categories, message=message)


@app.route('/about')
def about():
    return render_template('about.html', title='A propos')


@app.route('/tous_manga')
def tous_manga():
    liste_manga = models.Vue_manga_categorie.query.all()
    return render_template('tous_manga.html', title='Catalogue', liste_manga=liste_manga)


@app.route('/manga_categorie')
def manga_categorie():
    id_categorie = request.args.get('id_categorie')
    liste_manga = models.Vue_manga_categorie.query.filter_by(id_categorie=id_categorie)
    return render_template('manga_categorie.html', title='Nos manga', manga=liste_manga, typemanga=type(liste_manga))


@app.route('/ajout_manga', methods=['GET', 'POST'])
def ajout_manga():
    if 'admin_id' not in session:
        flash('Veuillez vous connecter en tant qu\'administrateur', 'danger')
        return redirect(url_for('connexion'))

    form = mangaForm()
    if form.validate_on_submit():
        nouveau_manga = models.manga(nom_manga=form.nom_manga.data, description=form.description.data,
                                     prix=form.prix.data, id_categorie=form.id_categorie.data, image=form.image.data)
        db.session.add(nouveau_manga)
        db.session.commit()
        flash('Manga ajouté avec succès', 'success')
        logging.info('Manga ajouté avec succès!')
        return redirect(url_for('accueil'))

    return render_template('ajout_manga.html', title='Ajouter un manga', form=form)


@app.route('/catalogue_pdf', methods=['GET'])
def catalogue_pdf():
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf_options = {
        'quiet': '',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf_filename = f"pdf_output/pdf_{len(os.listdir('pdf_output')) + 1}.pdf"

    pdfkit.from_url("http://127.0.0.1:5000/tous_manga", pdf_filename, configuration=config, options=pdf_options)

    success_message = "Le PDF a été généré avec succès."
    return redirect(url_for('accueil', message=success_message))


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')  # Pas de hashage

        admin = Admin.query.filter_by(login=login, password=password).first()

        if admin:
            session['admin_id'] = admin.id_admin
            logging.debug("Connexion réussie pour l'administrateur %s", login)
            return redirect(url_for('accueil'))
        else:
            logging.debug("Échec de la connexion pour l'administrateur %s", login)
            return redirect(url_for('tous_manga'))

    return render_template('connexion.html')




@app.route('/deconnexion')
def deconnexion():
    session.pop('admin_id', None)
    return redirect(url_for('connexion'))

