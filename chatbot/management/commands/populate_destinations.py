from django.core.management.base import BaseCommand
from chatbot.models import Destination
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the Destination database with sample entries'

    def handle(self, *args, **kwargs):
        destinations = [
            {
                "name": "Nosy Be",
                "description": "Une île paradisiaque au nord-ouest, connue pour ses plages de sable blanc et ses eaux turquoise.",
                "activities": "Plongée sous-marine, observation des baleines (juillet-septembre), visite de Nosy Komba.",
                "language": "fr",
                "image": "destinations/nosy_be.jpg"
            },
            {
                "name": "Allée des Baobabs",
                "description": "Un site iconique près de Morondava, célèbre pour ses baobabs majestueux au coucher du soleil.",
                "activities": "Photographie, randonnée, découverte de la culture locale.",
                "language": "fr",
                "image": "destinations/baobabs.jpg"
            },
            {
                "name": "Parc de l'Isalo",
                "description": "Un parc national spectaculaire avec des canyons, des piscines naturelles et une faune unique.",
                "activities": "Randonnée, observation des lémuriens, baignade dans les piscines naturelles.",
                "language": "fr",
                "image": "destinations/isalo.jpg"
            },
            {
                "name": "Nosy Be",
                "description": "Nosy iray paradisa any avaratra-andrefan'i Madagasikara, malaza amin'ny moron-dranony fotsy sy rano turquoise.",
                "activities": "Fitsokosokana anaty rano, fijerena trozona (jolay-septambra), fitsidihana an'i Nosy Komba.",
                "language": "mg",
                "image": "destinations/nosy_be.jpg"
            },
            {
                "name": "Allée des Baobabs",
                "description": "Toerana manaitra akaikin'i Morondava, malaza amin'ny hazo baobab manaitra rehefa milentika ny masoandro.",
                "activities": "Sary, fitsangatsanganana, fianarana ny kolontsaina eo an-toerana.",
                "language": "mg",
                "image": "destinations/baobabs.jpg"
            },
            {
                "name": "Parc de l'Isalo",
                "description": "Valan-javaboary mahavariana miaraka amin'ny canyons, dobo voajanahary, ary biby tsy manam-paharoa.",
                "activities": "Fitsangatsanganana, fijerena varika, milomano amin'ny dobo voajanahary.",
                "language": "mg",
                "image": "destinations/isalo.jpg"
            },
        ]

        # Supprimer les destinations existantes (optionnel)
        Destination.objects.all().delete()

        # Ajouter les destinations
        for dest in destinations:
            image_path = os.path.join(settings.MEDIA_ROOT, dest['image'])
            if os.path.exists(image_path):
                Destination.objects.get_or_create(
                    name=dest['name'],
                    language=dest['language'],
                    defaults={
                        'description': dest['description'],
                        'activities': dest['activities'],
                        'image': dest['image']
                    }
                )
            else:
                self.stdout.write(self.style.WARNING(f"Image {dest['image']} not found. Skipping image for {dest['name']}."))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {Destination.objects.count()} destinations'))