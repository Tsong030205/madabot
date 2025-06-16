from django.core.management.base import BaseCommand
from chatbot.models import FAQ

class Command(BaseCommand):
    help = 'Populate the FAQ database with 50 entries (25 French, 25 Malagasy)'

    def handle(self, *args, **kwargs):
        # Liste des FAQs
        faqs = [
            # Français
            {"question": "Quelle est la meilleure période pour visiter Madagascar ?", "answer": "La saison sèche (avril à novembre) est idéale, avec septembre et octobre offrant des températures douces.", "keywords": "période, visiter, saison", "language": "fr"},
            {"question": "Ai-je besoin d'un visa pour Madagascar ?", "answer": "Oui, un visa est requis pour la plupart des nationalités, obtainable à l'arrivée ou en ligne.", "keywords": "visa, entrée, passeport", "language": "fr"},
            {"question": "Quels sont les vaccins recommandés ?", "answer": "Hépatite A, typhoïde, et un traitement antipaludéen sont conseillés.", "keywords": "vaccins, santé, malaria", "language": "fr"},
            {"question": "Combien coûte un voyage à Madagascar ?", "answer": "Cela dépend du circuit, mais comptez entre 1500€ et 3000€ pour 2 semaines.", "keywords": "coût, prix, budget", "language": "fr"},
            {"question": "Quelles sont les destinations populaires ?", "answer": "Nosy Be, Allée des Baobabs, et Parc de l'Isalo sont très prisés.", "keywords": "destinations, populaires, visiter", "language": "fr"},
            {"question": "Est-il sécuritaire de voyager à Madagascar ?", "answer": "Oui, avec des précautions normales comme éviter les zones isolées la nuit.", "keywords": "sécurité, voyage, danger", "language": "fr"},
            {"question": "Quelle est la monnaie locale ?", "answer": "L'Ariary (MGA). Les euros sont acceptés dans certains endroits touristiques.", "keywords": "monnaie, ariary, paiement", "language": "fr"},
            {"question": "Puis-je louer une voiture ?", "answer": "Oui, mais un chauffeur-guide est recommandé pour les routes difficiles.", "keywords": "location, voiture, chauffeur", "language": "fr"},
            {"question": "Quels sont les plats traditionnels ?", "answer": "Le romazava (bouillon de viande et légumes) et le ravitoto (porc avec manioc) sont populaires.", "keywords": "cuisine, plats, nourriture", "language": "fr"},
            {"question": "Y a-t-il du Wi-Fi dans les hôtels ?", "answer": "Oui, dans les grandes villes et hôtels touristiques, mais la connexion peut être lente.", "keywords": "wifi, internet, connexion", "language": "fr"},
            {"question": "Comment se déplacer à Madagascar ?", "answer": "Par vols intérieurs, taxis-brousse, ou voitures avec chauffeur.", "keywords": "transport, déplacement, taxi", "language": "fr"},
            {"question": "Quels animaux peut-on voir ?", "answer": "Lémuriens, caméléons, et baleines (en saison) sont emblématiques.", "keywords": "animaux, faune, lémuriens", "language": "fr"},
            {"question": "Quel est le climat à Nosy Be ?", "answer": "Tropical, avec des températures entre 25°C et 30°C toute l'année.", "keywords": "climat, nosy be, météo", "language": "fr"},
            {"question": "Puis-je faire de la plongée ?", "answer": "Oui, Nosy Be et Sainte-Marie offrent d'excellents spots de plongée.", "keywords": "plongée, mer, activités", "language": "fr"},
            {"question": "Quelles langues sont parlées ?", "answer": "Le malgache et le français sont les langues officielles.", "keywords": "langues, parler, communication", "language": "fr"},
            {"question": "Y a-t-il des festivals à Madagascar ?", "answer": "Oui, comme le Donia à Nosy Be ou les fêtes traditionnelles.", "keywords": "festivals, événements, culture", "language": "fr"},
            {"question": "Comment réserver un circuit ?", "answer": "Via notre chatbot, tapez 'réserver' pour commencer !", "keywords": "réserver, circuit, réservation", "language": "fr"},
            {"question": "Quels sont les parcs nationaux ?", "answer": "Isalo, Andasibe, et Tsingy de Bemaraha sont incontournables.", "keywords": "parcs, nationaux, nature", "language": "fr"},
            {"question": "Puis-je voir des baobabs ?", "answer": "Oui, à l'Allée des Baobabs près de Morondava.", "keywords": "baobabs, allée, morondava", "language": "fr"},
            {"question": "Quel est le décalage horaire ?", "answer": "Madagascar est à GMT+3, soit +1h par rapport à Paris en été.", "keywords": "décalage, horaire, temps", "language": "fr"},
            {"question": "Quels souvenirs ramener ?", "answer": "Artisanat, vanille, et pierres précieuses sont populaires.", "keywords": "souvenirs, artisanat, achats", "language": "fr"},
            {"question": "Y a-t-il des restrictions douanières ?", "answer": "Oui, l'exportation de certains produits comme le bois précieux est interdite.", "keywords": "douanes, restrictions, exportation", "language": "fr"},
            {"question": "Puis-je payer par carte ?", "answer": "Dans les grands hôtels oui, mais l'espèce (Ariary) est préférable.", "keywords": "paiement, carte, espèces", "language": "fr"},
            {"question": "Quels vêtements emporter ?", "answer": "Vêtements légers, chaussures de marche, et un imperméable pour la saison des pluies.", "keywords": "vêtements, packing, bagages", "language": "fr"},
            {"question": "Comment contacter MadaVoyage ?", "answer": "Par email (contact@madavoyage.mg) ou via notre chatbot.", "keywords": "contact, madavoyage, support", "language": "fr"},

            # Malgache
            {"question": "Oviana ny fotoana tsara indrindra hitsidika an'i Madagasikara ?", "answer": "Ny vanim-potoana maina (aprily ka hatramin'ny novambra) no tsara, indrindra ny septambra sy oktobra.", "keywords": "fotoana, fitsidihana, vanim-potoana", "language": "mg"},
            {"question": "Mila visa ve aho raha hitsidika an'i Madagasikara ?", "answer": "Eny, ilaina ny visa ho an'ny ankamaroan'ny firenena, azo alaina rehefa tonga na an-tserasera.", "keywords": "visa, fidirana, pasipaoro", "language": "mg"},
            {"question": "Inona ny vaksiny soso-kevitra ?", "answer": "Hepatitis A, typhoid, ary fitsaboana manohitra ny tazomoka no soso-kevitra.", "keywords": "vaksiny, fahasalamana, tazomoka", "language": "mg"},
            {"question": "Ohatrinona ny vidin'ny dia mankany Madagasikara ?", "answer": "Miankina amin'ny fitsangatsanganana, fa eo anelanelan'ny 1500€ sy 3000€ ho an'ny 2 herinandro.", "keywords": "vidiny, sarany, teti-bola", "language": "mg"},
            {"question": "Inona ny toerana malaza ?", "answer": "Nosy Be, Allée des Baobabs, ary Parc de l'Isalo no tena malaza.", "keywords": "toerana, malaza, fitsidihana", "language": "mg"},
            {"question": "Azo antoka ve ny mandeha any Madagasikara ?", "answer": "Eny, raha mitandrina tsara toy ny fialana amin'ny toerana mitokana amin'ny alina.", "keywords": "filaminana, dia, loza", "language": "mg"},
            {"question": "Inona ny vola ampiasaina ?", "answer": "Ariary (MGA). Ny euro dia ekena amin'ny toerana fizahan-tany sasany.", "keywords": "vola, ariary, fandoavana", "language": "mg"},
            {"question": "Afaka manofa fiara ve aho ?", "answer": "Eny, fa soso-kevitra ny manofa mpamily-mpitarika noho ny lalana sarotra.", "keywords": "fanofana, fiara, mpamily", "language": "mg"},
            {"question": "Inona ny sakafo nentin-drazana ?", "answer": "Romazava (ron-kena sy legioma) sy ravitoto (hena kisoa miaraka amin'ny ravim-bazaha) no malaza.", "keywords": "sakafo, nentin-drazana, hanina", "language": "mg"},
            {"question": "Misy Wi-Fi ve any amin'ny hotely ?", "answer": "Eny, any amin'ny tanàna lehibe sy hotely fizahan-tany, fa mety miadana ny fifandraisana.", "keywords": "wifi, internet, fifandraisana", "language": "mg"},
            {"question": "Ahoana ny fandehanana any Madagasikara ?", "answer": "Amin'ny sidina anatiny, taxi-brousse, na fiara miaraka amin'ny mpamily.", "keywords": "fitaterana, fandehanana, taxi", "language": "mg"},
            {"question": "Inona ny biby azo jerena ?", "answer": "Varika, bongolava, ary trozona (amin'ny vanim-potoana) no tena misongadina.", "keywords": "biby, fauna, varika", "language": "mg"},
            {"question": "Ahoana ny toetr'andro any Nosy Be ?", "answer": "Tropikaly, miaraka amin'ny hafanana eo anelanelan'ny 25°C sy 30°C mandritra ny taona.", "keywords": "toetr'andro, nosy be, hafanana", "language": "mg"},
            {"question": "Afaka mitsoraka ve aho ?", "answer": "Eny, Nosy Be sy Sainte-Marie dia manolotra toerana tsara hitsorakana.", "keywords": "mitsoraka, ranomasina, hetsika", "language": "mg"},
            {"question": "Inona ny teny ampiasaina ?", "answer": "Malgache sy frantsay no teny ofisialy.", "keywords": "teny, miresaka, fifandraisana", "language": "mg"},
            {"question": "Misy fetibe ve any Madagasikara ?", "answer": "Eny, toy ny Donia any Nosy Be na ny fety nentin-drazana.", "keywords": "fetibe, hetsika, kolontsaina", "language": "mg"},
            {"question": "Ahoana ny fomba famandrihana fitsangatsanganana ?", "answer": "Amin'ny chatbot antsika, soraty 'mampandray' hanombohana !", "keywords": "mampandray, fitsangatsanganana, famandrihana", "language": "mg"},
            {"question": "Inona ny valan-javaboary nasionaly ?", "answer": "Isalo, Andasibe, ary Tsingy de Bemaraha no tsy tokony ho diso.", "keywords": "valan-javaboary, nasionaly, natiora", "language": "mg"},
            {"question": "Afaka mahita baobab ve aho ?", "answer": "Eny, any amin'ny Allée des Baobabs akaikin'i Morondava.", "keywords": "baobab, allée, morondava", "language": "mg"},
            {"question": "Ohatrinona ny elanelam-potoana ?", "answer": "Madagasikara dia amin'ny GMT+3, izany hoe +1h raha oharina amin'i Paris amin'ny fahavaratra.", "keywords": "elanelam-potoana, ora, fotoana", "language": "mg"},
            {"question": "Inona ny fahatsiarovana azo entina ?", "answer": "Asa tanana, vanila, ary vato soa no malaza.", "keywords": "fahatsiarovana, asa tanana, fividianana", "language": "mg"},
            {"question": "Misy fandrarana amin'ny douane ve ?", "answer": "Eny, voarara ny manondrana vokatra sasany toy ny hazo sarobidy.", "keywords": "douane, fandrarana, fanondranana", "language": "mg"},
            {"question": "Afaka mandoa amin'ny carte ve aho ?", "answer": "Any amin'ny hotely lehibe eny, fa ny vola (Ariary) no tsara kokoa.", "keywords": "fandoavana, carte, vola", "language": "mg"},
            {"question": "Inona ny akanjo tokony ho entina ?", "answer": "Akanjo maivana, kiraro fitsangatsanganana, ary akanjo tsy lena amin'ny vanim-potoana orana.", "keywords": "akanjo, entana, valizy", "language": "mg"},
            {"question": "Ahoana ny fifandraisana amin'i MadaVoyage ?", "answer": "Amin'ny mailaka (contact@madavoyage.mg) na amin'ny chatbot antsika.", "keywords": "fifandraisana, madavoyage, fanampiana", "language": "mg"},
        ]

        # Supprimer les FAQs existantes (optionnel, commenter si tu veux conserver)
        FAQ.objects.all().delete()

        # Ajouter les FAQs
        for faq_data in faqs:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'keywords': faq_data['keywords'],
                    'language': faq_data['language']
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {FAQ.objects.count()} FAQs'))