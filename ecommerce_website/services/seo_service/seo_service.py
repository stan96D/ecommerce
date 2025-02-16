from abc import ABC, abstractmethod


class SEOServiceInterface(ABC):
    @abstractmethod
    def get_meta_object(object):
        pass


class HomeSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Goedkoopste Vloeren – PVC, Laminaat & Vinyl | NL, BE & DE",
            "keywords": "goedkoopste vloeren, pvc vloeren, laminaat, visgraat vloeren, vinyl vloeren, plinten, ondervloeren, Nederland, België, Duitsland, goedkoopste vloerenshop",
            "description": "Goedkoopste vloeren kopen? Bij GoedkoopsteVloerenShop vind je de laagste prijzen voor PVC, laminaat, visgraat, vinyl, plinten en ondervloeren in Nederland, België en Duitsland. Altijd de goedkoopste!"
        }


class TermsConditionsSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Algemene Voorwaarden – Goedkoopste Vloeren Shop | Duidelijkheid & Transparantie",
            "keywords": "algemene voorwaarden, voorwaarden vloeren, koopvoorwaarden, regels, kopen vloeren, goedkoopste vloeren, privacy, leveringsvoorwaarden",
            "description": "Lees de algemene voorwaarden van GoedkoopsteVloerenShop voor al onze regels en voorwaarden bij het kopen van vloeren in Nederland, België en Duitsland. Transparant en duidelijk."
        }


class DisclaimerSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Disclaimer – Goedkoopste Vloeren Shop | Aansprakelijkheid & Verantwoordelijkheid",
            "keywords": "disclaimer, disclaimer vloeren, juridische informatie, aansprakelijkheid, copyright, gebruiksvoorwaarden, verantwoordelijkheid",
            "description": "Lees de disclaimer van GoedkoopsteVloerenShop voor belangrijke juridische informatie over aansprakelijkheid, copyright en gebruiksvoorwaarden bij het kopen van vloeren in Nederland, België en Duitsland."
        }


class ContactSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Klantenservice – Goedkoopste Vloeren Shop | Reactie Binnen 1 Dag",
            "keywords": "klantenservice, klantenservice vloeren, contact, vraag, support, snel antwoord, e-mail ondersteuning, vloeren winkel, Nederland, België, Duitsland",
            "description": "Heb je vragen? Onze klantenservice van GoedkoopsteVloerenShop reageert binnen 1 dag via e-mail. Neem contact met ons op voor ondersteuning bij het kopen van vloeren in Nederland, België en Duitsland."
        }


class PaymentDeliverySEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Betaling en Levering – Goedkoopste Vloeren Shop | Top Levering",
            "keywords": "betaling, levering, vloeren levering, betaalmethoden, levering opties, gratis levering, levering Nederland, België, Duitsland, snelle levering",
            "description": "Bij GoedkoopsteVloerenShop bieden we veilige betaalmethoden en snelle leveringsopties. Lees alles over betalingen, leveringstermijnen en bezorginformatie in Nederland, België en Duitsland."
        }


class ReturnSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Retourneren – Goedkoopste Vloeren Shop | Geld Terug Garantie",
            "keywords": "retourneren, vloeren retourneren, retourvoorwaarden, terugbetaling, retour proces, gemakkelijk retourneren, retourneren Nederland, België, Duitsland",
            "description": "Bij GoedkoopsteVloerenShop kun je vloeren gemakkelijk retourneren. Lees alles over onze retourvoorwaarden, het retourproces en terugbetalingen in Nederland, België en Duitsland."
        }


class AboutUsSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Over Ons – Goedkoopste Vloeren Shop | 20 Jaar Ervaring & Beste Kwaliteit",
            "keywords": "over ons, vloeren winkel, bedrijf, 20 jaar ervaring, goedkope vloeren, beste kwaliteit vloeren, expert team, vloeren Nederland, België, Duitsland, ons verhaal",
            "description": "GoedkoopsteVloerenShop heeft meer dan 20 jaar ervaring in de vloerenbranche. Ons team van 4 experts biedt de goedkoopste vloeren van de beste kwaliteit. Wij leveren PVC, laminaat, visgraat en vinyl vloeren in Nederland, België en Duitsland – simpel maar effectief."
        }


class SignInSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Inloggen – Goedkoopste Vloeren Shop",
            "keywords": "inloggen, account, klantenaccount, vloeren shop account, inloggen klanten, toegang account, klantenportaal",
            "description": "Log in op je account bij GoedkoopsteVloerenShop om snel en eenvoudig je bestellingen te bekijken, je gegevens te beheren en de status van je vloerenbestelling te volgen."
        }


class StoreRatingSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Winkelbeoordeling – Goedkoopste Vloeren Shop | Open Voor Feedback!",
            "keywords": "winkelbeoordeling, klantbeoordeling, reviews, vloeren shop beoordelingen, feedback, klantenervaring, klantfeedback, store rating, vloeren Nederland, België, Duitsland",
            "description": "Deel je ervaring bij GoedkoopsteVloerenShop! Laat een beoordeling achter over onze vloeren, service en levering. Lees ook wat andere klanten zeggen over hun aankoopervaring in Nederland, België en Duitsland."
        }


class NewPasswordSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Nieuw Wachtwoord – Goedkoopste Vloeren Shop | Account Herstellen",
            "keywords": "nieuw wachtwoord, wachtwoord vergeten, account herstel, wachtwoord reset, klantenaccount, toegang herstellen, beveiliging wachtwoord",
            "description": "Vergeet je wachtwoord? Stel eenvoudig een nieuw wachtwoord in voor je account bij GoedkoopsteVloerenShop en krijg snel toegang tot je bestellingen en gegevens."
        }


class SignUpSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Registreren – Goedkoopste Vloeren Shop | Nieuw Account",
            "keywords": "registreren, account aanmaken, klantaccount, nieuwe klant, aanmelden vloeren shop, gratis account, klantenportaal, vloeren winkel",
            "description": "Maak eenvoudig een account aan bij GoedkoopsteVloerenShop en profiteer van de beste prijzen voor vloeren. Meld je aan voor toegang tot je bestellingen, aanbiedingen en sneller afrekenen."
        }


class AccountViewSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Mijn Account – Goedkoopste Vloeren Shop",
            "keywords": "mijn account, klantaccount, bestellingen bekijken, retour aanvragen, adresgegevens, account gegevens, vloeren shop account, orders bekijken",
            "description": "Bekijk je account bij GoedkoopsteVloerenShop. Hier kun je je bestellingen inzien, retouren aanvragen, je adresgegevens beheren en je accountinformatie aanpassen."
        }


class ShoppingCartSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Winkelmandje – Goedkoopste Vloeren Shop",
            "keywords": "winkelwagentje, winkelmand, vloeren winkelwagentje, vloeren kopen, bestellingen, vloeren afrekenen, producten toevoegen, winkelmand Nederland, België, Duitsland",
            "description": "Bekijk en bewerk je winkelwagentje bij GoedkoopsteVloerenShop. Voeg vloeren toe, bewerk je bestelling en ga snel door naar het afrekenen van je vloeren in Nederland, België en Duitsland."
        }


class CheckoutSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Afrekenen – Goedkoopste Vloeren Shop | Persoonlijke Gegevens",
            "keywords": "uitchecken, bestelling plaatsen, afrekenen, gegevens invullen, vloeren kopen, betaalgegevens, levering gegevens, bestelproces, vloeren winkel",
            "description": "Voltooi je bestelling bij GoedkoopsteVloerenShop. Vul je gegevens in, kies een betaalmethode en voltooi het afrekenproces om de goedkoopste vloeren te kopen in Nederland, België en Duitsland."
        }


class PaymentSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Betaling – Goedkoopste Vloeren Shop | Bestelling Compleet Maken",
            "keywords": "betaling, bestelling betalen, betaalmethode, veilig betalen, online betaling, vloeren kopen, betaalgegevens, terugbetaling, betaling opties",
            "description": "Voltooi de betaling van je bestelling bij GoedkoopsteVloerenShop. Kies je gewenste betaalmethode en betaal veilig voor je vloeren in Nederland, België en Duitsland."
        }


class OrderDetailSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Ordergegevens – Goedkoopste Vloeren Shop",
            "keywords": "bestelgegevens, orderdetails, bestelling bekijken, vloeren bestelling, bestelstatus, bestelhistorie, orderbevestiging, status bestelling",
            "description": "Bekijk de details van je bestelling bij GoedkoopsteVloerenShop. Volg de status van je vloerenbestelling en bekijk de producten, prijzen en levertijd in Nederland, België en Duitsland."
        }


class ReturnDetailSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Retourgegevens – Goedkoopste Vloeren Shop",
            "keywords": "retourgegevens, retourstatus, product retourneren, retour aanvragen, retourinformatie, vloeren retourneren, retourproces, bestelling retourneren",
            "description": "Bekijk de details van je retour bij GoedkoopsteVloerenShop. Volg de status van je retouraanvraag, bekijk de producten die je hebt geretourneerd en de terugbetaling in Nederland, België en Duitsland."
        }


class CreateReturnSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Retour Aanmaken – Goedkoopste Vloeren Shop",
            "keywords": "retour aanmaken, vloeren retourneren, retour aanvraag, product retouren, retourproces, retourverzoek, retourneren vloeren, retour Nederland, België, Duitsland",
            "description": "Wil je een product retourneren? Maak eenvoudig een retouraanvraag aan bij GoedkoopsteVloerenShop en volg het retourproces voor vloeren in Nederland, België en Duitsland."
        }


class ProductDetailSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        # Assuming 'object' is the product data that contains dynamic information.
        product_name = object.name if object and hasattr(
            object, 'name') else "Vloer Product"
        product_description = object.description if object and hasattr(
            object, 'description') else "Beschrijving van het product."

        return {
            "title": f"{product_name} – Goedkoopste Vloeren Shop",
            "keywords": "vloeren, pvc vloeren, laminaat, visgraat, vinyl, plinten",
            "description": f"{product_description} Bestel nu bij GoedkoopsteVloerenShop voor de goedkoopste prijzen in Nederland, België en Duitsland."
        }


class AssortmentSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Assortiment – Goedkoopste Vloeren Shop",
            "keywords": "assortiment, vloeren assortiment, pvc vloeren, laminaat, visgraat vloeren, vinyl vloeren, plinten, ondervloeren, vloeren kopen, goedkope vloeren",
            "description": "Bekijk het complete assortiment vloeren bij GoedkoopsteVloerenShop. Van PVC, laminaat en visgraat vloeren tot vinyl, plinten en ondervloeren, altijd de beste prijs in Nederland, België en Duitsland."
        }


class SearchSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        search_query = object.query if object and hasattr(
            object, 'query') else "vloeren zoeken"

        return {
            "title": f"Zoekresultaten voor {search_query} – Goedkoopste Vloeren Shop",
            "keywords": f"zoeken, {search_query}, vloeren zoeken, pvc vloeren, laminaat, vinyl vloeren, visgraat vloeren, plinten, ondervloeren",
            "description": f"Bekijk de zoekresultaten voor '{search_query}' bij GoedkoopsteVloerenShop. Vind de beste vloeren, van PVC, laminaat en vinyl, tot plinten en ondervloeren, altijd tegen de laagste prijs."
        }


class FavoritesSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Favorieten – Goedkoopste Vloeren Shop",
            "keywords": "favorieten, opgeslagen producten, vloeren favorieten, favoriete vloeren, plinten, vinyl, laminaat, PVC vloeren",
            "description": "Bekijk je favoriete vloeren bij GoedkoopsteVloerenShop. Van PVC, laminaat, en vinyl tot plinten en ondervloeren, altijd de beste keuze voor vloeren in Nederland, België en Duitsland."
        }


class DiscountsSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Kortingen – Goedkoopste Vloeren Shop | Nóg Goedkoper!",
            "keywords": "kortingen, vloeren korting, sale, aanbiedingen, vloeren aanbiedingen, korting op vloeren, kortingen pvc vloeren, laminaat korting, vinyl korting",
            "description": "Bekijk de nieuwste kortingen bij GoedkoopsteVloerenShop! Profiteer van geweldige aanbiedingen op vloeren zoals PVC, laminaat, vinyl, en plinten in Nederland, België en Duitsland."
        }


class RunnersSEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        return {
            "title": "Hardlopers – Goedkoopste Vloeren Shop",
            "keywords": "hardlopers, vloeren bescherming, vloeren runners, pvc hardlopers, laminaat hardlopers, vinyl hardlopers, vloerbedekking, vloer bescherming",
            "description": "Bekijk ons assortiment hardlopers bij GoedkoopsteVloerenShop. Bescherm je vloeren met de beste kwaliteit runners voor PVC, laminaat, vinyl en andere vloeren in Nederland, België en Duitsland."
        }


class CategorySEOService(SEOServiceInterface):

    @staticmethod
    def get_meta_object(object=None):
        # Assuming 'object' contains the category name and a description
        category_name = object.name if object and hasattr(
            object, 'name') else "Vloeren"
        category_description = object.description if object and hasattr(
            object, 'description') else "Bekijk ons assortiment vloeren."

        return {
            "title": f"{category_name} – Goedkoopste Vloeren Shop",
            "keywords": "vloeren, pvc vloeren, laminaat, vinyl vloeren, plinten",
            "description": f"Bekijk het assortiment {category_name} bij GoedkoopsteVloerenShop. {category_description} Van PVC, laminaat, vinyl tot plinten en meer, altijd de beste prijzen in Nederland, België en Duitsland."
        }
