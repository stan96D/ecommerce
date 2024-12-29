from decimal import Decimal


class WebShopConfig:

    @staticmethod
    def disclaimer():
        return ""

    @staticmethod
    def terms_and_conditions():
        return """
<section>
    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 1. Definities</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>1.1 Ondernemer:</strong> De partij die producten aanbiedt via de webshop.</li>
        <li><strong>1.2 Consument:</strong> De natuurlijke persoon die niet handelt in de uitoefening van een beroep of bedrijf en een overeenkomst aangaat met de ondernemer.</li>
        <li><strong>1.3 Overeenkomst:</strong> Een koopovereenkomst tussen de ondernemer en de consument.</li>
        <li><strong>1.4 Producten:</strong> Alle vloeren, accessoires en andere artikelen die via de webshop worden aangeboden.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 2. Toepasselijkheid</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>2.1</strong> Deze algemene voorwaarden zijn van toepassing op alle aanbiedingen, overeenkomsten en leveringen van de ondernemer, tenzij schriftelijk anders is overeengekomen.</li>
        <li><strong>2.2</strong> Door een bestelling te plaatsen, aanvaardt de consument deze voorwaarden.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 3. Aanbod en Prijzen</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>3.1</strong> Het aanbod bevat een volledige en nauwkeurige omschrijving van de producten. Kennelijke vergissingen of fouten in het aanbod binden de ondernemer niet.</li>
        <li><strong>3.2</strong> Alle prijzen zijn inclusief btw, tenzij anders vermeld. Eventuele bezorgkosten worden apart aangegeven.</li>
        <li><strong>3.3 Afbeeldingen en kleuren:</strong> De afbeeldingen op de website zijn indicatief. Kleuren kunnen in werkelijkheid afwijken door instellingen van beeldschermen of lichtomstandigheden.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 4. Totstandkoming van de Overeenkomst</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>4.1</strong> De overeenkomst komt tot stand op het moment dat de consument een bestelling plaatst en de ondernemer deze bestelling bevestigt.</li>
        <li><strong>4.2</strong> De ondernemer behoudt zich het recht voor een bestelling te weigeren of aanvullende voorwaarden te stellen, bijvoorbeeld bij grote bestellingen of betalingsproblemen.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 5. Levering en Uitvoering</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>5.1</strong> De ondernemer zal de grootst mogelijke zorgvuldigheid in acht nemen bij het uitvoeren van de bestelling en het leveren van producten.</li>
        <li><strong>5.2</strong> Levering vindt plaats op het door de consument opgegeven adres.</li>
        <li><strong>5.3</strong> De ondernemer streeft naar levering binnen de vermelde termijn. Bij vertraging wordt de consument hiervan tijdig op de hoogte gesteld.</li>
        <li><strong>5.4</strong> De ondernemer levert alleen de producten. Het leggen van de vloer dient door de consument zelf te worden uitgevoerd.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 6. Herroepingsrecht</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>6.1</strong> De consument heeft het recht de overeenkomst binnen 14 dagen na ontvangst van de producten zonder opgave van redenen te herroepen.</li>
        <li><strong>6.2</strong> Tijdens de herroepingstermijn zal de consument zorgvuldig omgaan met het product en de verpakking. Het product mag slechts in die mate worden uitgepakt of gebruikt als nodig is om de aard, kenmerken en werking ervan vast te stellen.</li>
        <li><strong>6.3</strong> Om het herroepingsrecht uit te oefenen, dient de consument een ondubbelzinnige verklaring binnen de herroepingstermijn aan de ondernemer te sturen.</li>
        <li><strong>6.4</strong> Retourkosten zijn voor rekening van de consument, tenzij anders overeengekomen.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 7. Garantie en Klachten</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>7.1 Garantiebepalingen:</strong> De garantie op onze vloeren is zorgvuldig samengesteld om de kwaliteit van het product te waarborgen en duidelijkheid te bieden over de voorwaarden. Hieronder vind je een overzicht van de garantievoorwaarden:
            <ul style="margin-left: 20px; line-height: 1.6;">
                <li><strong>Garantieperiode:</strong> De garantieperiode op de slijtlaag varieert per vloer en staat vermeld op de productpagina van de betreffende vloer.</li>
                <li><strong>Fabricagefouten en zichtbare schade:</strong> Garantie wordt verleend op fabricagefouten, exorbitante kleurverschillen en beschadigingen die vóór het leggen van de vloer zijn geconstateerd.</li>
                <li><strong>Uitsluitingen van de garantie:</strong>
                    <ul style="margin-left: 20px; line-height: 1.6;">
                        <li>Zelf gelegde vloeren: Er wordt geen garantie gegeven op bollingen, spleten of het loslaten van de klikverbinding als de vloer zelf is gelegd.</li>
                        <li>Slijtage en beschadigingen: Krassen, butsen en andere gebruikssporen vallen niet onder de fabrieksgarantie.</li>
                        <li>Ondeugdelijk gebruik of onderhoud: Schade door ondeugdelijk gebruik, zoals overmatig vocht, puntbelasting door stoelen, naaldhakken, of schoenen met steentjes, valt niet onder de garantie.</li>
                    </ul>
                </li>
                <li><strong>Voorkomen van schade:</strong>
                    <ul style="margin-left: 20px; line-height: 1.6;">
                        <li>Voorzie meubels en andere zware objecten van viltlappen om krassen te voorkomen.</li>
                        <li>Gebruik bij bureaustoelen extra bescherming, zoals een kleed of bureaustoelmat.</li>
                        <li>Zorg ervoor dat de stofzuiger een zachte borstelmond heeft.</li>
                    </ul>
                </li>
                <li><strong>Fabrieksgarantie:</strong> De fabrieksgarantie geldt uitsluitend voor ongeopende pakketten.</li>
            </ul>
        </li>

        <li><strong>7.2 Klachten:</strong>
            <ul style="margin-left: 20px; line-height: 1.6;">
                <li>Klachten over gebreken aan producten dienen binnen een redelijke termijn na ontdekking schriftelijk en duidelijk omschreven aan de ondernemer te worden gemeld.</li>
                <li>De ondernemer zal klachten binnen een termijn van 14 dagen afhandelen. Indien een klacht een voorzienbaar langere verwerkingstijd vraagt, wordt de consument hiervan op de hoogte gesteld.</li>
            </ul>
        </li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 8. Aansprakelijkheid</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>8.1</strong> De ondernemer is niet aansprakelijk voor schade ontstaan door ondeugdelijk gebruik van de producten.</li>
        <li><strong>8.2</strong> Behoudens opzet of grove nalatigheid van de ondernemer, is de aansprakelijkheid van de ondernemer beperkt tot het bedrag dat de consument voor het product heeft betaald.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 9. Privacy</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>9.1</strong> De ondernemer respecteert de privacy van de consument en verwerkt persoonsgegevens conform de Algemene Verordening Gegevensbescherming (AVG).</li>
        <li><strong>9.2</strong> Persoonsgegevens worden uitsluitend gebruikt voor de uitvoering van de overeenkomst en, indien toestemming is gegeven, voor marketingdoeleinden.</li>
    </ul>

    <h2 style="margin-top: 30px; font-weight: bold;">Artikel 10. Toepasselijk Recht en Geschillen</h2>
    <ul style="margin-left: 20px; line-height: 1.6;">
        <li><strong>10.1</strong> Op alle overeenkomsten tussen de ondernemer en de consument is uitsluitend Nederlands recht van toepassing.</li>
        <li><strong>10.2</strong> Geschillen worden bij voorkeur in onderling overleg opgelost. Indien dit niet mogelijk is, kan de consument het geschil voorleggen aan een bevoegde Nederlandse rechter.</li>
    </ul>
</section>


"""

    @staticmethod
    def get_hero_data():
        return {
            "hero1":
            {
                "title": "Vloeren",
                "description": "De beste topmerken",
                "url": "products/?Producttype=Vloer",
                "image_path": "hero1.jpg"
            },
            "hero2":
            {
                "title": "Click PVC",
                "description": "Makkelijk om zelf te leggen!",
                "url": "products/?Vloertype=Click",






















                "image_path": "hero2.webp"
            },
            "hero3":
            {
                "title": "Kortingen",
                "description": "Nu tijdelijk nóg goedkoper",
                "url": "/discounts",

                "image_path": "hero3.jpg"
            },
        }

    @staticmethod
    def tax_high():
        return Decimal('21.00')

    @staticmethod





















    def tax_low():
        return Decimal('9.00')

    @staticmethod
    def excluded_filters():
        return [
            "Afmeting",
            "Type",
            "SKU",
            "Producttype",
            "Omschrijving",
            "Leverancier",
            "Weekmakervrij",
            "Garantie commercieel",
            "Beschikbaarheid",
            "Kant-en-klaar",
            "Garantie huishoudelijk",





















            "Links",
            "Garantie periode",
            "Eenheid",
            "Overlap",
            "Oppervlakte",
            "Pakinhoud",
            "Productcode van de fabrikant"
        ]

    @staticmethod
    def slider_filters():
        return [
            "Dikte",
            "Lengte",
            "Breedte",
            "Toplaagdikte",
            "Dikte toplaag",
            "Warmteweerstand (m²K/W)",
            "Dikte onderlaag",
            "Dikte tussenlaag",
            "Slijtlaag",

        ]

    @staticmethod
    def search_filters():
        return [
            "Vloertype",
            "Type",
            "Merk",
            "Model",
            "Kleur",
            "Collectie",
        ]

    @staticmethod
    def shipping_margin():
        return Decimal('1.05')

    @staticmethod
    def gain_margin():
        return Decimal('1.30')

    @staticmethod
    def return_days():
        return 14

    @staticmethod
    def contact_email():
        return "info@goedkoopstevloerenshop.com"

    @staticmethod
    def address():
        return ""

    @staticmethod
    def postal_code():
        return ""

    @staticmethod
    def coc_number():
        return ""

    @staticmethod
    def vat_number():
        return ""

    @staticmethod
    def opening_time_week():
        return "10:00-17:00"

    @staticmethod
    def opening_time_weekend():
        return "Gesloten"
