from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ, Reservation, Destination, BudgetEstimate
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
from datetime import datetime, date
from decimal import Decimal

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').lower().strip()
        language = data.get('language', 'fr')
        response = {}

        # Initialiser la session
        if 'reservation_step' not in request.session:
            request.session['reservation_step'] = None
            request.session['reservation_data'] = {}
        if 'guide_step' not in request.session:
            request.session['guide_step'] = None
        if 'budget_step' not in request.session:
            request.session['budget_step'] = None
            request.session['budget_data'] = {}

        # Commande globale pour annuler toutes les étapes
        if user_input in ['annuler', 'fanafoana']:
            request.session['reservation_step'] = None
            request.session['reservation_data'] = {}
            request.session['guide_step'] = None
            request.session['budget_step'] = None
            request.session['budget_data'] = {}
            if language == 'fr':
                response['answer'] = "Toutes les actions ont été annulées. Posez une question, tapez 'guide', 'budget', ou 'réserver'."
            else:
                response['answer'] = "Najanona ny zava-drehetra. Mametraha fanontaniana, soraty 'toerana', 'teti-bola', na 'mampandray'."
            return JsonResponse(response)

        # Logique FAQ (placée en premier pour priorité)
        faqs = FAQ.objects.filter(language=language)
        best_match = None
        max_score = 0
        for faq in faqs:
            keywords = [k.strip().lower() for k in faq.keywords.split(',')]
            score = sum(1 for word in user_input.split() if word in keywords)
            if score > max_score:
                max_score = score
                best_match = faq

        if best_match and max_score > 0:
            response['answer'] = best_match.answer
            return JsonResponse(response)

        # Commandes pour le calculateur de budget
        budget_commands = ['budget', 'calculateur', 'teti-bola', 'tombana vidiny']
        if user_input in budget_commands:
            request.session['budget_step'] = 'destination'
            request.session['budget_data'] = {'language': language}
            destinations = Destination.objects.filter(language=language).values_list('name', flat=True)
            if destinations:
                dest_list = ", ".join(destinations)
                if language == 'fr':
                    response['answer'] = f"Commençons l'estimation de votre budget. Quelle est votre destination ? Choisissez parmi : {dest_list}."
                else:
                    response['answer'] = f"Andao hanomboka ny tombana ny teti-bolanao. Aiza ny toerana halehanao ? Mifidiana amin'ireto : {dest_list}."
            else:
                if language == 'fr':
                    response['answer'] = "Aucune destination disponible pour le moment."
                else:
                    response['answer'] = "Tsy misy toerana misy amin'izao fotoana izao."
            return JsonResponse(response)

        # Gestion du calculateur de budget
        budget_step = request.session.get('budget_step')
        budget_data = request.session.get('budget_data', {})

        if budget_step == 'destination':
            available_destinations = Destination.objects.filter(language=language).values_list('name', flat=True)
            if user_input in [d.lower() for d in available_destinations]:
                budget_data['destination'] = next(d for d in available_destinations if d.lower() == user_input)
                request.session['budget_step'] = 'duration'
                if language == 'fr':
                    response['answer'] = "Combien de jours resterez-vous ? (ex. 7)"
                else:
                    response['answer'] = "Firy andro no hijanonanao ? (ohatra: 7)"
            else:
                if language == 'fr':
                    response['answer'] = f"Destination non reconnue. Choisissez parmi : {', '.join(available_destinations)} ou dites 'annuler'."
                else:
                    response['answer'] = f"Toerana tsy fantatra. Mifidiana amin'ireto : {', '.join(available_destinations)} na lazao 'fanafoana'."
            request.session['budget_data'] = budget_data
            return JsonResponse(response)

        elif budget_step == 'duration':
            try:
                duration = int(user_input)
                if duration < 1 or duration > 30:
                    if language == 'fr':
                        response['answer'] = "La durée doit être entre 1 et 30 jours. Essayez encore."
                    else:
                        response['answer'] = "Ny faharetana dia tsy maintsy eo anelanelan'ny 1 sy 30 andro. Andramo indray."
                else:
                    budget_data['duration_days'] = duration
                    request.session['budget_step'] = 'num_people'
                    if language == 'fr':
                        response['answer'] = "Combien de personnes voyagent ? (1 à 50)"
                    else:
                        response['answer'] = "Firy ny olona handeha ? (1 hatramin'ny 50)"
            except ValueError:
                if language == 'fr':
                    response['answer'] = "Veuillez entrer un nombre valide."
                else:
                    response['answer'] = "Ampidiro isa marina."
            request.session['budget_data'] = budget_data
            return JsonResponse(response)

        elif budget_step == 'num_people':
            try:
                num_people = int(user_input)
                if num_people < 1 or num_people > 50:
                    if language == 'fr':
                        response['answer'] = "Le nombre de personnes doit être entre 1 et 50. Essayez encore."
                    else:
                        response['answer'] = "Ny isan'ny olona dia tsy maintsy eo anelanelan'ny 1 sy 50. Andramo indray."
                else:
                    budget_data['num_people'] = num_people
                    request.session['budget_step'] = 'accommodation_type'
                    if language == 'fr':
                        response['answer'] = "Quel type d'hébergement préférez-vous ? (économique, standard, luxe)"
                    else:
                        response['answer'] = "Karazana trano hipetrahana inona no tianao ? (mora, antonony, mihaja)"
            except ValueError:
                if language == 'fr':
                    response['answer'] = "Veuillez entrer un nombre valide."
                else:
                    response['answer'] = "Ampidiro isa marina."
            request.session['budget_data'] = budget_data
            return JsonResponse(response)

        elif budget_step == 'accommodation_type':
            accommodation_types = {'économique': 'economique', 'standard': 'standard', 'luxe': 'luxe', 'mora': 'economique', 'antonony': 'standard', 'mihaja': 'luxe'}
            if user_input in accommodation_types:
                budget_data['accommodation_type'] = accommodation_types[user_input]
                request.session['budget_step'] = 'email'
                if language == 'fr':
                    response['answer'] = "Veuillez entrer votre adresse email pour recevoir l'estimation (ou tapez 'non' pour continuer sans email)."
                else:
                    response['answer'] = "Ampidiro ny adiresy mailakao mba handraisana ny tombana (na soraty 'tsy misy' raha tsy mila mailaka)."
            else:
                if language == 'fr':
                    response['answer'] = "Type d'hébergement invalide. Choisissez : économique, standard, luxe."
                else:
                    response['answer'] = "Karazana trano tsy mety. Mifidiana : mora, antonony, mihaja."
            request.session['budget_data'] = budget_data
            return JsonResponse(response)

        elif budget_step == 'email':
            if user_input == 'non' or user_input == 'tsy misy' or ('@' in user_input and '.' in user_input):
                budget_data['email'] = user_input if '@' in user_input else None

                # Calculer le budget
                prices = {
                    'Nosy Be': {'economique': 50, 'standard': 100, 'luxe': 200},
                    'Allée des Baobabs': {'economique': 30, 'standard': 60, 'luxe': 120},
                    'Parc de l\'Isalo': {'economique': 40, 'standard': 80, 'luxe': 160},
                }
                dest_prices = prices.get(budget_data['destination'], {'economique': 50, 'standard': 100, 'luxe': 200})
                accommodation_cost = dest_prices[budget_data['accommodation_type']] * budget_data['duration_days'] * budget_data['num_people']
                transport_cost = 100 * budget_data['num_people']  # Vol ou transport indicatif
                activities_cost = 50 * budget_data['duration_days'] * budget_data['num_people']  # Activités indicatives
                total_cost = Decimal(accommodation_cost + transport_cost + activities_cost)

                # Enregistrer l'estimation
                estimation = BudgetEstimate.objects.create(
                    destination=budget_data['destination'],
                    duration_days=budget_data['duration_days'],
                    num_people=budget_data['num_people'],
                    accommodation_type=budget_data['accommodation_type'],
                    estimated_cost=total_cost,
                    language=budget_data['language'],
                    email=budget_data['email']
                )

                # Envoyer l'email si fourni
                if budget_data['email']:
                    send_budget_email(estimation)

                # Afficher le résultat
                if language == 'fr':
                    response['answer'] = (
                        f"<b>Estimation de budget pour {budget_data['destination']}</b><br>"
                        f"Durée : {budget_data['duration_days']} jours<br>"
                        f"Nombre de personnes : {budget_data['num_people']}<br>"
                        f"Hébergement : {budget_data['accommodation_type']}<br><br>"
                        f"<b>Répartition :</b><br>"
                        f"- Hébergement : €{accommodation_cost}<br>"
                        f"- Transport : €{transport_cost}<br>"
                        f"- Activités : €{activities_cost}<br>"
                        f"<b>Total : €{total_cost}</b><br><br>"
                        "Voulez-vous réserver ce voyage ? Dites 'réserver' ou tapez 'non' pour continuer."
                    )
                else:
                    response['answer'] = (
                        f"<b>Tombana teti-bola ho an'i {budget_data['destination']}</b><br>"
                        f"Faharetana : {budget_data['duration_days']} andro<br>"
                        f"Isan'ny olona : {budget_data['num_people']}<br>"
                        f"Trano : {budget_data['accommodation_type']}<br><br>"
                        f"<b>Fizarana :</b><br>"
                        f"- Trano : €{accommodation_cost}<br>"
                        f"- Fitaterana : €{transport_cost}<br>"
                        f"- Hetsika : €{activities_cost}<br>"
                        f"<b>Total : €{total_cost}</b><br><br>"
                        "Te-hamandry an'io dia io ve ianao ? Lazao 'mampandray' na soraty 'tsy misy' raha tsy mila."
                    )

                # Pré-remplir les données pour la réservation
                request.session['reservation_data'] = {
                    'language': language,
                    'destination': budget_data['destination'],
                    'num_people': budget_data['num_people']
                }
                request.session['budget_step'] = 'reservation_prompt'
            else:
                if language == 'fr':
                    response['answer'] = "Adresse email invalide. Entrez un email valide ou tapez 'non'."
                else:
                    response['answer'] = "Adiresy mailaka tsy mety. Ampidiro mailaka marina na soraty 'tsy misy'."
            request.session['budget_data'] = budget_data
            return JsonResponse(response)

        elif budget_step == 'reservation_prompt':
            if user_input in ['réserver', 'mampandray']:
                request.session['budget_step'] = None
                request.session['reservation_step'] = 'start_date'
                if language == 'fr':
                    response['answer'] = "Parfait ! Quelle est la date de début de votre voyage ? (format : JJ/MM/AAAA)"
                else:
                    response['answer'] = "Tsara ! Rahoviana ny daty hanombohana ny dianao ? (endrika : DD/MM/YYYY)"
            elif user_input in ['non', 'tsy misy']:
                request.session['budget_step'] = None
                request.session['budget_data'] = {}
                if language == 'fr':
                    response['answer'] = "D'accord, que puis-je faire pour vous ? Tapez 'guide', 'budget', ou 'réserver'."
                else:
                    response['answer'] = "Tsara, inona no azoko atao ho anao ? Soraty 'toerana', 'teti-bola', na 'mampandray'."
            else:
                if language == 'fr':
                    response['answer'] = "Veuillez répondre par 'réserver' ou 'non'."
                else:
                    response['answer'] = "Valio amin'ny 'mampandray' na 'tsy misy'."
            return JsonResponse(response)

        # Logique du guide
        guide_commands = ['guide', 'destinations', 'toerana', 'toerana malaza']
        if user_input in guide_commands:
            request.session['guide_step'] = 'list_destinations'
            destinations = Destination.objects.filter(language=language)
            if destinations.exists():
                dest_list = ", ".join([d.name for d in destinations])
                if language == 'fr':
                    response['answer'] = f"Voici nos destinations : {dest_list}. Dites le nom d'une destination pour en savoir plus (ex. 'Nosy Be') ou 'annuler' pour arrêter."
                else:
                    response['answer'] = f"Ireto ny toerana misy antsika : {dest_list}. Lazao ny anaran'ny toerana iray raha mila fanazavana fanampiny (ohatra: 'Nosy Be') na 'fanafoana' raha hijanona."
            else:
                if language == 'fr':
                    response['answer'] = "Aucune destination disponible pour le moment."
                else:
                    response['answer'] = "Tsy misy toerana misy amin'izao fotoana izao."
            return JsonResponse(response)

        guide_step = request.session.get('guide_step')
        if guide_step == 'list_destinations':
            destination = Destination.objects.filter(language=language, name__iexact=user_input).first()
            if destination:
                image_url = destination.image.url if destination.image else ''
                if language == 'fr':
                    image_link = f'<a href="{image_url}" target="_blank" class="text-amber-500 underline">Voir l\'image</a><br>' if image_url else ''
                    response['answer'] = (
                        f"<b>{destination.name}</b><br>{destination.description}<br><br>"
                        f"<b>Activités :</b> {destination.activities}<br>"
                        f"{image_link}"
                        "Voulez-vous réserver pour cette destination ? Dites 'réserver' ou continuez avec une autre destination."
                    )
                else:
                    image_link = f'<a href="{image_url}" target="_blank" class="text-amber-500 underline">Jereo ny sary</a><br>' if image_url else ''
                    response['answer'] = (
                        f"<b>{destination.name}</b><br>{destination.description}<br><br>"
                        f"<b>Hetsika :</b> {destination.activities}<br>"
                        f"{image_link}"
                        "Te-hamandry an'io toerana io ve ianao ? Lazao 'mampandray' na tohizo amin'ny toerana haja."
                    )
                request.session['reservation_data'] = {'language': language, 'destination': destination.name}
                request.session['guide_step'] = None
            else:
                destinations = Destination.objects.filter(language=language)
                dest_list = ", ".join([d.name for d in destinations])
                if language == 'fr':
                    response['answer'] = f"Destination non trouvée. Choisissez parmi : {dest_list} ou dites 'annuler'."
                else:
                    response['answer'] = f"Tsy hita ny toerana. Mifidiana amin'ireto : {dest_list} na lazao 'fanafoana'."
            return JsonResponse(response)

        # Logique de réservation
        if user_input in ['réserver', 'réservation', 'mampandray', 'famandrihana']:
            request.session['reservation_step'] = 'destination'
            request.session['reservation_data'] = request.session.get('reservation_data', {'language': language})
            if language == 'fr':
                response['answer'] = "Super ! Commençons votre réservation. Quelle est votre destination ? (ex. Nosy Be, Allée des Baobabs, Parc de l'Isalo)"
            else:
                response['answer'] = "Tsara ! Andao hanomboka ny famandrihanao. Aiza ny toerana halehanao ? (ohatra: Nosy Be, Allée des Baobabs, Parc de l'Isalo)"
            return JsonResponse(response)

        # Étapes de réservation
        step = request.session.get('reservation_step')
        reservation_data = request.session.get('reservation_data', {})

        if step == 'destination':
            available_destinations = Destination.objects.filter(language=language).values_list('name', flat=True)
            if user_input in [d.lower() for d in available_destinations]:
                reservation_data['destination'] = next(d for d in available_destinations if d.lower() == user_input)
                request.session['reservation_step'] = 'start_date'
                if language == 'fr':
                    response['answer'] = "Parfait ! Quelle est la date de début de votre voyage ? (format : JJ/MM/AAAA)"
                else:
                    response['answer'] = "Tsara ! Rahoviana ny daty hanombohana ny dianao ? (endrika : DD/MM/YYYY)"
            else:
                if language == 'fr':
                    response['answer'] = f"Destination non reconnue. Choisissez parmi : {', '.join(available_destinations)} ou dites 'annuler'."
                else:
                    response['answer'] = f"Toerana tsy fantatra. Mifidiana amin'ireto : {', '.join(available_destinations)} na lazao 'fanafoana'."
            request.session['reservation_data'] = reservation_data
            return JsonResponse(response)

        elif step == 'start_date':
            try:
                start_date = datetime.strptime(user_input, '%d/%m/%Y').date()
                if start_date < date.today():
                    if language == 'fr':
                        response['answer'] = "La date de début doit être dans le futur. Essayez encore (JJ/MM/AAAA)."
                    else:
                        response['answer'] = "Ny daty hanombohana dia tsy maintsy ho amin'ny ho avy. Andramo indray (DD/MM/YYYY)."
                else:
                    reservation_data['start_date'] = start_date.strftime('%Y-%m-%d')
                    request.session['reservation_step'] = 'end_date'
                    if language == 'fr':
                        response['answer'] = "Bien noté ! Quelle est la date de fin de votre voyage ? (format : JJ/MM/AAAA)"
                    else:
                        response['answer'] = "Voapetraka ! Rahoviana ny daty hifarana ny dianao ? (endrika : DD/MM/YYYY)"
            except ValueError:
                if language == 'fr':
                    response['answer'] = "Format de date invalide. Utilisez JJ/MM/AAAA."
                else:
                    response['answer'] = "Endrika daty tsy mety. Ampiasao DD/MM/YYYY."
            request.session['reservation_data'] = reservation_data
            return JsonResponse(response)

        elif step == 'end_date':
            try:
                end_date = datetime.strptime(user_input, '%d/%m/%Y').date()
                start_date = datetime.strptime(reservation_data['start_date'], '%Y-%m-%d').date()
                if end_date <= start_date:
                    if language == 'fr':
                        response['answer'] = "La date de fin doit être après la date de début. Essayez encore (JJ/MM/AAAA)."
                    else:
                        response['answer'] = "Ny daty farany dia tsy maintsy aorian'ny daty fanombohana. Andramo indray (DD/MM/YYYY)."
                else:
                    reservation_data['end_date'] = end_date.strftime('%Y-%m-%d')
                    request.session['reservation_step'] = 'num_people'
                    if language == 'fr':
                        response['answer'] = "Combien de personnes voyagent ? (1 à 50)"
                    else:
                        response['answer'] = "Firy ny olona handeha ? (1 hatramin'ny 50)"
            except ValueError:
                if language == 'fr':
                    response['answer'] = "Format de date invalide. Utilisez JJ/MM/AAAA."
                else:
                    response['answer'] = "Endrika daty tsy mety. Ampiasao DD/MM/YYYY."
            request.session['reservation_data'] = reservation_data
            return JsonResponse(response)

        elif step == 'num_people':
            try:
                num_people = int(user_input)
                if num_people < 1 or num_people > 50:
                    if language == 'fr':
                        response['answer'] = "Le nombre de personnes doit être entre 1 et 50. Essayez encore."
                    else:
                        response['answer'] = "Ny isan'ny olona dia tsy maintsy eo anelanelan'ny 1 sy 50. Andramo indray."
                else:
                    reservation_data['num_people'] = num_people
                    request.session['reservation_step'] = 'email'
                    if language == 'fr':
                        response['answer'] = "Veuillez entrer votre adresse email."
                    else:
                        response['answer'] = "Ampidiro ny adiresy mailakao."
            except ValueError:
                if language == 'fr':
                    response['answer'] = "Veuillez entrer un nombre valide."
                else:
                    response['answer'] = "Ampidiro isa marina."
            request.session['reservation_data'] = reservation_data
            return JsonResponse(response)

        elif step == 'email':
            if '@' in user_input and '.' in user_input:
                reservation_data['email'] = user_input
                reservation = Reservation.objects.create(
                    destination=reservation_data['destination'],
                    start_date=reservation_data['start_date'],
                    end_date=reservation_data['end_date'],
                    num_people=reservation_data['num_people'],
                    email=reservation_data['email'],
                    language=reservation_data['language']
                )
                send_confirmation_email(reservation)
                pdf_url = f"/api/reservation/pdf/{reservation.id}/"
                if language == 'fr':
                    response['answer'] = f"Votre réservation a été enregistrée ! Téléchargez votre devis ici : <a href='{pdf_url}' target='_blank' class='text-amber-500 underline'>Télécharger le devis</a>"
                else:
                    response['answer'] = f"Ny famandrihanao dia voarakitra ! Alaina eto ny devis-nao : <a href='{pdf_url}' target='_blank' class='text-amber-500 underline'>Alaina ny devis</a>"
                request.session['reservation_step'] = None
                request.session['reservation_data'] = {}
            else:
                if language == 'fr':
                    response['answer'] = "Adresse email invalide. Essayez encore."
                else:
                    response['answer'] = "Adiresy mailaka tsy mety. Andramo indray."
            request.session['reservation_data'] = reservation_data
            return JsonResponse(response)

        # Réponse par défaut si aucune condition n’est remplie
        if language == 'fr':
            response['answer'] = "Désolé, je n'ai pas trouvé de réponse. Essayez une autre question, tapez 'guide' pour explorer les destinations, 'budget' pour estimer un budget, ou 'réserver' pour une réservation !"
        else:
            response['answer'] = "Miala tsiny, tsy nahita valiny aho. Andramo fanontaniana hafa, soraty 'toerana' mba hijery ny toerana, 'teti-bola' ho an'ny tombana, na 'mampandray' ho an'ny famandrihana !"

        return JsonResponse(response)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def send_budget_email(estimation):
    subject = 'Estimation de budget - MadaVoyage'
    message = (
        f"Bonjour,\n\n"
        f"Votre estimation de budget a été générée avec succès.\n\n"
        f"Détails :\n"
        f"- Destination : {estimation.destination}\n"
        f"- Durée : {estimation.duration_days} jours\n"
        f"- Nombre de personnes : {estimation.num_people}\n"
        f"- Type d'hébergement : {estimation.accommodation_type}\n"
        f"- Coût estimé : €{estimation.estimated_cost}\n\n"
        f"Contactez-nous pour planifier votre voyage !\n\n"
        f"Équipe MadaVoyage"
    )
    if estimation.language == 'mg':
        subject = 'Tombana teti-bola - MadaVoyage'
        message = (
            f"Miarahaba,\n\n"
            f"Ny tombana teti-bolanao dia vita soa aman-tsara.\n\n"
            f"Antsipiriany :\n"
            f"- Toerana : {estimation.destination}\n"
            f"- Faharetana : {estimation.duration_days} andro\n"
            f"- Isan'ny olona : {estimation.num_people}\n"
            f"- Karazana trano : {estimation.accommodation_type}\n"
            f"- Vidiny tombana : €{estimation.estimated_cost}\n\n"
            f"Mifandraisa aminay mba hikarakara ny dianao !\n\n"
            f"Ekipa MadaVoyage"
        )
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [estimation.email],
        fail_silently=False,
    )

@csrf_exempt
def reservation_pdf(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="devis_madavoyage_{reservation.id}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Adapter le contenu selon la langue
        if reservation.language == 'mg':
            story.append(Paragraph("MadaVoyage - Tombana ny famandrihana", styles['Title']))
            story.append(Spacer(1, 12))
            content = f"""
            <b>Toerana :</b> {reservation.destination}<br/>
            <b>Daty manomboka :</b> {reservation.start_date}<br/>
            <b>Daty mifarana :</b> {reservation.end_date}<br/>
            <b>Isan'ny olona :</b> {reservation.num_people}<br/>
            <b>Email :</b> {reservation.email}<br/>
            <b>Tombana vidiny :</b> €{reservation.num_people * 100} (fanondroana)<br/>
            """
            story.append(Paragraph(content, styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("Misaotra anao mifandray aminay mba hanamafisana ny famandrihanao.", styles['Normal']))
        else:  # Français par défaut
            story.append(Paragraph("MadaVoyage - Devis de Réservation", styles['Title']))
            story.append(Spacer(1, 12))
            content = f"""
            <b>Destination :</b> {reservation.destination}<br/>
            <b>Date de début :</b> {reservation.start_date}<br/>
            <b>Date de fin :</b> {reservation.end_date}<br/>
            <b>Nombre de personnes :</b> {reservation.num_people}<br/>
            <b>Email :</b> {reservation.email}<br/>
            <b>Prix estimé :</b> €{reservation.num_people * 100} (indicatif)<br/>
            """
            story.append(Paragraph(content, styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("Merci de nous contacter pour confirmer votre réservation.", styles['Normal']))
        
        doc.build(story)
        return response
    except Reservation.DoesNotExist:
        return HttpResponse("Réservation non trouvée.", status=404)

def send_confirmation_email(reservation):
    subject = 'Confirmation de votre demande de réservation - MadaVoyage'
    message = (
        f"Bonjour,\n\n"
        f"Votre demande de réservation a été reçue avec succès.\n\n"
        f"Détails :\n"
        f"- Destination : {reservation.destination}\n"
        f"- Date de début : {reservation.start_date}\n"
        f"- Date de fin : {reservation.end_date}\n"
        f"- Nombre de personnes : {reservation.num_people}\n"
        f"- Email : {reservation.email}\n\n"
        f"Un devis PDF a été généré. Merci de nous contacter pour finaliser.\n\n"
        f"Équipe MadaVoyage"
    )
    if reservation.language == 'mg':
        subject = 'Fanamafisana ny fangatahanao - MadaVoyage'
        message = (
            f"Miarahaba,\n\n"
            f"Ny fangatahanao ho an'ny famandrihana dia voaray soa aman-tsara.\n\n"
            f"Antsipiriany :\n"
            f"- Toerana : {reservation.destination}\n"
            f"- Daty manomboka : {reservation.start_date}\n"
            f"- Daty mifarana : {reservation.end_date}\n"
            f"- Isan'ny olona : {reservation.num_people}\n"
            f"- Email : {reservation.email}\n\n"
            f"Ny devis PDF dia efa vita. Mifandraisa aminay mba hamita ny famandrihana.\n\n"
            f"Ekipa MadaVoyage"
        )
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reservation.email],
        fail_silently=False,
    )

def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')